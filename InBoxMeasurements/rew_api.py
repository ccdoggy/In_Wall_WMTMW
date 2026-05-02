"""
rew_api.py
==========

Thin adapter for REW's HTTP API (available in REW 5.20+, enabled in
Preferences → API or via the `-api` launch flag). Default base URL is
http://localhost:4735; an OpenAPI spec is served at /doc.json.

The REW API is a work-in-progress and endpoint names/schemas have shifted
between releases. This adapter is written to be resilient to that:

  * Every call catches every exception and returns a structured result.
    Callers never see urllib errors — they check result.ok / .manual_required.
  * Multiple candidate endpoints are tried in order; the first 2xx wins.
  * All HTTP attempts are recorded to an in-memory debug log so the wizard
    can print a trace when something looks wrong.

Public interface:
  * probe()                  -> ProbeResult
  * measure(sweep)           -> MeasureResult
  * export_all(out_dir)      -> ExportResult

Intended failure mode: when anything goes wrong (API not running, wrong
REW version, endpoint moved, etc.) the adapter returns a result with
manual_required=True and a short error string. The wizard falls back to
guided-prompt mode.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from measurement_matrix import AcousticSweep


# ---------------------------------------------------------------------------
# Result dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ProbeResult:
    reachable: bool
    base_url: str
    version: Optional[str] = None
    openapi_available: bool = False
    error: Optional[str] = None
    debug_log: list[str] = field(default_factory=list)


@dataclass
class MeasureResult:
    ok: bool
    measurement_id: Optional[int] = None
    duration_s: Optional[float] = None
    overload: bool = False
    error: Optional[str] = None
    manual_required: bool = False
    debug_log: list[str] = field(default_factory=list)


@dataclass
class ExportResult:
    ok: bool
    files_written: list[str] = field(default_factory=list)
    error: Optional[str] = None
    manual_required: bool = False
    debug_log: list[str] = field(default_factory=list)


@dataclass
class ExportLatestResult:
    ok: bool
    frd_path: Optional[Path] = None
    error: Optional[str] = None
    manual_required: bool = False
    debug_log: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Adapter
# ---------------------------------------------------------------------------

# Tuning knobs
_DEFAULT_BASE_URL = "http://localhost:4735"
_DEFAULT_PROBE_TIMEOUT_S = 2.0
_DEFAULT_MEASURE_TIMEOUT_S = 180.0   # full 512 k sweep + overhead
_DEFAULT_POLL_INTERVAL_S = 0.75

# Candidate endpoint patterns. If REW moves things, add the new path here and
# keep the old one for backward compat — first 2xx wins.
_VERSION_PATHS = ("/version", "/application/version")
_OPENAPI_PATHS = ("/doc.json", "/openapi.json")
_MEASURE_START_PATHS = ("/measure", "/measurements/measure", "/measurements")
_MEASURE_STATUS_PATHS = ("/measure/status", "/measurements/{id}/status", "/measurements/{id}")
_EXPORT_ALL_PATHS = ("/measurements/export-all", "/measurements/export", "/export/all")
_EXPORT_LATEST_PATHS = (
    "/measurements/{id}/export",
    "/measurements/last/export",
    "/measurements/export-last",
)


class RewApi:
    """Best-effort adapter. Never raises to the caller."""

    def __init__(
        self,
        base_url: str = _DEFAULT_BASE_URL,
        probe_timeout_s: float = _DEFAULT_PROBE_TIMEOUT_S,
        measure_timeout_s: float = _DEFAULT_MEASURE_TIMEOUT_S,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.probe_timeout_s = probe_timeout_s
        self.measure_timeout_s = measure_timeout_s
        self._debug: list[str] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def probe(self) -> ProbeResult:
        """Quick health check. Never raises."""
        self._debug = []
        version = None
        for path in _VERSION_PATHS:
            status, body, err = self._get(path, timeout=self.probe_timeout_s)
            if status and 200 <= status < 300:
                if isinstance(body, dict):
                    version = body.get("version") or body.get("REW") or str(body)
                elif isinstance(body, str):
                    version = body
                break
        if version is None:
            return ProbeResult(
                reachable=False,
                base_url=self.base_url,
                error="No REW API response on any known version endpoint.",
                debug_log=list(self._debug),
            )
        openapi_ok = False
        for path in _OPENAPI_PATHS:
            status, _, _ = self._get(path, timeout=self.probe_timeout_s)
            if status and 200 <= status < 300:
                openapi_ok = True
                break
        return ProbeResult(
            reachable=True,
            base_url=self.base_url,
            version=version,
            openapi_available=openapi_ok,
            debug_log=list(self._debug),
        )

    def measure(self, sweep: AcousticSweep) -> MeasureResult:
        """Run one sweep via REW API. Never raises."""
        self._debug = []
        payload = _build_measure_payload(sweep)
        t_start = time.monotonic()

        # Start measurement
        start_status, start_body, start_err = self._try_post_any(
            _MEASURE_START_PATHS, payload, timeout=self.measure_timeout_s,
        )
        if not (start_status and 200 <= start_status < 300):
            return MeasureResult(
                ok=False,
                manual_required=True,
                error=f"Could not start measurement via API: {start_err or start_status}",
                debug_log=list(self._debug),
            )

        # Extract measurement id if the response included one
        meas_id = _extract_id(start_body)

        # Poll for completion. If we can't poll, trust the start call was
        # synchronous and treat it as done.
        overload = False
        if meas_id is not None:
            ok, overload, poll_err = self._poll_until_done(meas_id)
            if not ok:
                return MeasureResult(
                    ok=False,
                    measurement_id=meas_id,
                    manual_required=True,
                    error=f"Measurement started but polling failed: {poll_err}",
                    debug_log=list(self._debug),
                )

        elapsed = time.monotonic() - t_start
        return MeasureResult(
            ok=True,
            measurement_id=meas_id,
            duration_s=elapsed,
            overload=overload,
            debug_log=list(self._debug),
        )

    def export_all(self, out_dir: Path) -> ExportResult:
        """Ask REW to export every measurement in the session to out_dir.

        This is best-effort. If the installed REW version doesn't expose a
        batch-export endpoint, the caller should fall back to manual
        File → Export within REW's UI.
        """
        self._debug = []
        out_dir = Path(out_dir)
        payload = {
            "directory": str(out_dir.resolve()),
            "formats": ["frd", "txt", "wav"],
            "includePhase": True,
        }
        status, body, err = self._try_post_any(
            _EXPORT_ALL_PATHS, payload, timeout=60.0,
        )
        if not (status and 200 <= status < 300):
            return ExportResult(
                ok=False,
                manual_required=True,
                error=f"Could not trigger batch export via API: {err or status}",
                debug_log=list(self._debug),
            )
        files = []
        if isinstance(body, dict):
            raw = body.get("files") or body.get("exported") or []
            if isinstance(raw, list):
                files = [str(x) for x in raw]
        return ExportResult(
            ok=True,
            files_written=files,
            debug_log=list(self._debug),
        )

    def export_latest(
        self,
        out_dir: Path,
        measurement_id: Optional[int] = None,
    ) -> "ExportLatestResult":
        """Export the most recent measurement as FRD. Best-effort.

        Tries several endpoint patterns. On success, scans out_dir for the
        most recently modified .frd file and returns its path. If the API
        doesn't support per-measurement export, returns manual_required=True.
        """
        self._debug = []
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        payload = {
            "directory": str(out_dir.resolve()),
            "formats": ["frd"],
            "includePhase": True,
        }

        # Try ID-based path, then "last", then generic last-export
        id_str = str(measurement_id) if measurement_id is not None else "last"
        candidate_paths = tuple(
            p.replace("{id}", id_str) for p in _EXPORT_LATEST_PATHS
        )
        status, body, err = self._try_post_any(candidate_paths, payload, timeout=30.0)

        if not (status and 200 <= status < 300):
            return ExportLatestResult(
                ok=False,
                manual_required=True,
                error=f"Per-measurement export not available: {err or status}",
                debug_log=list(self._debug),
            )

        # Find the most recently modified .frd file in out_dir
        frd_files = sorted(out_dir.glob("*.frd"), key=lambda p: p.stat().st_mtime)
        frd_path = frd_files[-1] if frd_files else None

        return ExportLatestResult(
            ok=True,
            frd_path=frd_path,
            debug_log=list(self._debug),
        )

    # ------------------------------------------------------------------
    # HTTP plumbing (private)
    # ------------------------------------------------------------------

    def _get(
        self, path: str, timeout: float,
    ) -> tuple[Optional[int], Any, Optional[str]]:
        return self._request("GET", path, None, timeout)

    def _post(
        self, path: str, body: dict, timeout: float,
    ) -> tuple[Optional[int], Any, Optional[str]]:
        return self._request("POST", path, body, timeout)

    def _put(
        self, path: str, body: dict, timeout: float,
    ) -> tuple[Optional[int], Any, Optional[str]]:
        return self._request("PUT", path, body, timeout)

    def _request(
        self,
        method: str,
        path: str,
        body: Optional[dict],
        timeout: float,
    ) -> tuple[Optional[int], Any, Optional[str]]:
        url = self.base_url + path
        data = json.dumps(body).encode("utf-8") if body is not None else None
        headers = {"Accept": "application/json"}
        if data is not None:
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                try:
                    parsed = json.loads(raw.decode("utf-8")) if raw else None
                except (UnicodeDecodeError, json.JSONDecodeError):
                    parsed = raw.decode("utf-8", errors="replace")
                self._debug.append(f"{method} {path} -> {resp.status}")
                return resp.status, parsed, None
        except urllib.error.HTTPError as e:
            err_body = ""
            try:
                err_body = e.read().decode("utf-8", errors="replace")
            except Exception:
                pass
            self._debug.append(f"{method} {path} -> HTTP {e.code} {err_body[:80]}")
            return e.code, None, f"HTTP {e.code}"
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            self._debug.append(f"{method} {path} -> {type(e).__name__}: {e}")
            return None, None, f"{type(e).__name__}: {e}"

    def _try_post_any(
        self,
        paths: tuple[str, ...],
        body: dict,
        timeout: float,
    ) -> tuple[Optional[int], Any, Optional[str]]:
        """Try each candidate path, return the first 2xx response."""
        last_err = None
        for path in paths:
            status, resp_body, err = self._post(path, body, timeout=timeout)
            if status and 200 <= status < 300:
                return status, resp_body, None
            last_err = err or (f"HTTP {status}" if status else "unreachable")
        return None, None, last_err

    def _poll_until_done(
        self, meas_id: int,
    ) -> tuple[bool, bool, Optional[str]]:
        """Poll measurement status until done or timeout. Returns (ok, overload, err)."""
        deadline = time.monotonic() + self.measure_timeout_s
        while time.monotonic() < deadline:
            for pattern in _MEASURE_STATUS_PATHS:
                path = pattern.replace("{id}", str(meas_id))
                status, body, _ = self._get(path, timeout=5.0)
                if status and 200 <= status < 300 and isinstance(body, dict):
                    state = str(body.get("state") or body.get("status") or "").lower()
                    overload = bool(body.get("overload") or body.get("clipped"))
                    if state in ("done", "complete", "completed", "finished", "idle"):
                        return True, overload, None
                    if state in ("error", "failed", "aborted"):
                        return False, overload, f"REW reported state={state}"
                    break  # got a valid status endpoint, keep polling this one
            time.sleep(_DEFAULT_POLL_INTERVAL_S)
        return False, False, f"Timed out after {self.measure_timeout_s:.0f} s"


# ---------------------------------------------------------------------------
# Helpers (module-private)
# ---------------------------------------------------------------------------

def _build_measure_payload(sweep: AcousticSweep) -> dict:
    """Map an AcousticSweep into a REW-API JSON payload.

    Field names are a best guess against the REW OpenAPI spec. If REW renames
    things, update here — every endpoint call funnels through this function.
    """
    return {
        "title": sweep.name,
        "name": sweep.name,
        "startFrequency": sweep.start_freq_hz,
        "endFrequency": sweep.end_freq_hz,
        "sweepLength": sweep.sweep_length,
        "level": sweep.level_dbfs,
        "outputChannel": "LEFT",
        "stimulus": "LOG_SWEEP",
        "useAcousticTimingReference": True,
    }


def _extract_id(body: Any) -> Optional[int]:
    """Pull a measurement id out of whatever shape REW returned."""
    if not isinstance(body, dict):
        return None
    for key in ("id", "measurementId", "measurement_id", "measurementID"):
        val = body.get(key)
        if isinstance(val, int):
            return val
        if isinstance(val, str) and val.isdigit():
            return int(val)
    # Sometimes REW wraps in {"measurement": {"id": ...}}
    inner = body.get("measurement")
    if isinstance(inner, dict):
        return _extract_id(inner)
    return None


# ---------------------------------------------------------------------------
# Smoke test (run as: python rew_api.py)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    api = RewApi()
    print(f"Probing REW at {api.base_url} ...")
    result = api.probe()
    if result.reachable:
        print(f"  reachable: True")
        print(f"  version:   {result.version}")
        print(f"  openapi:   {result.openapi_available}")
    else:
        print(f"  reachable: False")
        print(f"  error:     {result.error}")
    print("  debug log:")
    for line in result.debug_log:
        print(f"    - {line}")
