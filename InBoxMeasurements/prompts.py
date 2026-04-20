"""
prompts.py
==========

UI helpers, user-input prompts, and resume-friendly CSV progress logging
for the WMTMW measurement wizard.

Windows-friendly:
  * ASCII-only visual decoration (no fancy Unicode box drawing).
  * ANSI colors auto-detected and enabled on Windows 10+ when possible;
    silently degraded to plain text when not supported or NO_COLOR is set.
  * UTF-8 console reconfigure for the degree symbol in sweep names.

Public surface:
  * setup_console()                 -- call once at program start
  * banner(), section(), subsection()
  * info(), ok(), warn(), error(), dim()
  * Action enum (GO / SKIP / REDO / QUIT)
  * prompt_action(), prompt_yn(), pause()
  * ProgressLog class (CSV; done_names(), counts_by_status(), record())
  * print_log_summary()
"""
from __future__ import annotations

import csv
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Iterable, Optional


# ---------------------------------------------------------------------------
# Console setup: UTF-8 + ANSI colors
# ---------------------------------------------------------------------------

_ANSI = {
    "reset":  "\033[0m",
    "bold":   "\033[1m",
    "dim":    "\033[2m",
    "red":    "\033[31m",
    "green":  "\033[32m",
    "yellow": "\033[33m",
    "cyan":   "\033[36m",
    "magenta": "\033[35m",
}

_USE_COLOR = False


def setup_console() -> None:
    """One-time console setup. Safe to call repeatedly."""
    global _USE_COLOR

    # UTF-8 on Windows so the degree symbol in sweep names renders correctly.
    if sys.platform == "win32":
        for stream in (sys.stdout, sys.stderr):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except (AttributeError, OSError):
                pass

        # Enable ANSI virtual terminal processing on older Windows consoles.
        # Windows Terminal already has this on; this is insurance for cmd.exe.
        try:
            import ctypes
            k32 = ctypes.windll.kernel32
            handle = k32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            mode = ctypes.c_ulong()
            if k32.GetConsoleMode(handle, ctypes.byref(mode)):
                k32.SetConsoleMode(handle, mode.value | 0x0004)  # ENABLE_VT
        except Exception:
            pass

    _USE_COLOR = _ansi_supported()


def _ansi_supported() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    try:
        return bool(sys.stdout.isatty())
    except (AttributeError, ValueError):
        return False


def _color(text: str, code: str) -> str:
    return _ANSI[code] + text + _ANSI["reset"] if _USE_COLOR else text


# ---------------------------------------------------------------------------
# Headers and message helpers
# ---------------------------------------------------------------------------

_WIDTH = 72


def banner() -> None:
    line = "=" * _WIDTH
    print()
    print(_color(line, "cyan"))
    print(_color("  WMTMW In-Wall Measurement Wizard", "bold"))
    print(_color("  Tweeter safety: start=300 Hz, length=256 k. Calibration woofer only.",
                 "yellow"))
    print(_color(line, "cyan"))
    print()


def section(title: str) -> None:
    print()
    print(_color("=" * _WIDTH, "cyan"))
    print(_color(f"  {title}", "bold"))
    print(_color("=" * _WIDTH, "cyan"))


def subsection(title: str) -> None:
    print()
    pad = max(0, _WIDTH - len(title) - 4)
    print(_color(f"-- {title} " + "-" * pad, "dim"))


def header_with_progress(title: str, current: int, total: int) -> None:
    """Section header tagged with a [N/M] progress counter."""
    section(f"[{current:>3d}/{total}] {title}")


def info(msg: str) -> None:
    print(_color(f"[INFO] {msg}", "cyan"))


def ok(msg: str) -> None:
    print(_color(f"[ OK ] {msg}", "green"))


def warn(msg: str) -> None:
    print(_color(f"[WARN] {msg}", "yellow"))


def error(msg: str) -> None:
    print(_color(f"[ERR ] {msg}", "red"))


def dim(msg: str) -> None:
    print(_color(msg, "dim"))


def safety(msg: str) -> None:
    """Prominent red/yellow callout for tweeter-safety notes."""
    print(_color(f"[SAFETY] {msg}", "red"))


# ---------------------------------------------------------------------------
# User-input prompts
# ---------------------------------------------------------------------------

class Action(Enum):
    GO = "go"
    SKIP = "skip"
    REDO = "redo"
    QUIT = "quit"


_DEFAULT_ACTION_PROMPT = "Ready? [Enter]=go  [s]=skip  [r]=redo  [q]=quit"


def prompt_action(
    prompt: str = _DEFAULT_ACTION_PROMPT,
    allow_skip: bool = True,
    allow_redo: bool = True,
) -> Action:
    """Block until the user picks GO / SKIP / REDO / QUIT.

    Empty input or 'g' returns GO. 's' / 'skip' returns SKIP (if allowed).
    'r' / 'redo' returns REDO (if allowed). 'q' / 'quit' / Ctrl-C returns QUIT.
    """
    while True:
        try:
            raw = input(prompt + " > ").strip().lower()
        except EOFError:
            return Action.QUIT
        except KeyboardInterrupt:
            print()
            return Action.QUIT

        if raw in ("", "g", "go", "y", "yes"):
            return Action.GO
        if raw in ("s", "skip") and allow_skip:
            return Action.SKIP
        if raw in ("r", "redo") and allow_redo:
            return Action.REDO
        if raw in ("q", "quit", "exit"):
            return Action.QUIT

        error(f"Unrecognized input: {raw!r}. Try Enter / s / r / q.")


def prompt_yn(question: str, default: bool = True) -> bool:
    """Yes/no prompt. Empty input returns the default."""
    suffix = "[Y/n]" if default else "[y/N]"
    while True:
        try:
            raw = input(f"{question} {suffix} > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return default
        if raw == "":
            return default
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        error("Please answer y or n.")


def pause(message: str = "Press Enter to continue...") -> None:
    """Blocking wait for Enter, no branching."""
    try:
        input(message)
    except (EOFError, KeyboardInterrupt):
        print()


# ---------------------------------------------------------------------------
# CSV progress log (resume-friendly)
# ---------------------------------------------------------------------------

CSV_FIELDS = ("timestamp", "phase", "name", "status", "duration_s", "notes")


@dataclass
class LogEntry:
    timestamp: str
    phase: str
    name: str
    status: str
    duration_s: str
    notes: str


class ProgressLog:
    """Append-only CSV of measurement attempts.

    One row per attempt. Resume logic uses the LATEST row per name, so
    redoing a previously-done sweep just appends a new 'done' row (or a
    'failed'/'skipped' row) and the most-recent status wins.
    """

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self._ensure_header()

    def _ensure_header(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists() or self.path.stat().st_size == 0:
            with self.path.open("w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(CSV_FIELDS)

    def record(
        self,
        phase: str,
        name: str,
        status: str,
        duration_s: Optional[float] = None,
        notes: str = "",
    ) -> None:
        """Append one row. `status` is typically 'done', 'skipped', or 'failed'."""
        row = (
            datetime.now().isoformat(timespec="seconds"),
            phase,
            name,
            status,
            f"{duration_s:.2f}" if duration_s is not None else "",
            notes,
        )
        with self.path.open("a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(row)

    def _latest_status_by_name(self) -> dict[str, str]:
        """Walk the CSV, return {name: most-recent-status}."""
        latest: dict[str, str] = {}
        if not self.path.exists():
            return latest
        try:
            with self.path.open("r", newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    name = row.get("name", "").strip()
                    status = row.get("status", "").strip()
                    if name and status:
                        latest[name] = status
        except (OSError, csv.Error) as e:
            warn(f"Could not read progress log ({e}); treating as empty.")
        return latest

    def done_names(self) -> set[str]:
        """Names whose most-recent status is 'done'."""
        return {n for n, s in self._latest_status_by_name().items() if s == "done"}

    def counts_by_status(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for s in self._latest_status_by_name().values():
            counts[s] = counts.get(s, 0) + 1
        return counts


def print_log_summary(log: ProgressLog, total_expected: Optional[int] = None) -> None:
    """Print a compact resume summary at session start."""
    counts = log.counts_by_status()
    if not counts:
        dim(f"No prior progress in {log.path.name}. Fresh session.")
        return
    info(f"Resume state (from {log.path.name}):")
    for status in ("done", "skipped", "failed"):
        n = counts.get(status, 0)
        if n:
            print(f"    {status:>8}: {n}")
    # Other states, if any
    for status, n in counts.items():
        if status not in ("done", "skipped", "failed"):
            print(f"    {status:>8}: {n}")
    if total_expected is not None:
        done = counts.get("done", 0)
        remaining = max(0, total_expected - done)
        dim(f"    pending: {remaining} of {total_expected}")


# ---------------------------------------------------------------------------
# Smoke test (run as: python prompts.py)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    setup_console()
    banner()
    section("Smoke test: visual helpers")
    info("this is info")
    ok("this is ok")
    warn("this is a warn")
    error("this is an error (not a real error)")
    safety("tweeter safety callout renders here")
    dim("dim text for secondary info")
    subsection("subsection header")
    header_with_progress("Horizontal polars", 23, 65)

    section("Smoke test: progress log")
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        log = ProgressLog(Path(td) / "sweep_log.csv")
        log.record("h_polar", "W1-UpperWoofer-H000deg", "done", duration_s=4.2)
        log.record("h_polar", "W2-LowerWoofer-H000deg", "skipped", notes="toddler interrupt")
        log.record("h_polar", "W1-UpperWoofer-H000deg", "done", duration_s=4.5)
        print("done_names:", sorted(log.done_names()))
        print("counts:    ", log.counts_by_status())
        print_log_summary(log, total_expected=65)

    # Interactive prompts only when stdin is a TTY (skip in CI)
    if sys.stdin.isatty():
        section("Smoke test: interactive prompts")
        print("Answer the next two prompts to test inputs, or Ctrl-C to abort.")
        a = prompt_action()
        print(f"  prompt_action returned: {a}")
        y = prompt_yn("Is this working?", default=True)
        print(f"  prompt_yn returned: {y}")
    else:
        dim("(stdin is not a TTY — skipping interactive prompt smoke test)")
