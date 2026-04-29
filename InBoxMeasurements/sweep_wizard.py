"""
sweep_wizard.py
===============

Main entry point for the WMTMW in-box measurement session. Orchestrates,
in order:

  0. Pre-check        -- probe REW API, restate tweeter-safety rules,
                         print resume summary from sweep_log.csv.
  1. DATS impedance   -- guide the user through 7 manual DATS sweeps
                         (individual drivers + pairs). No API.
  2. 2.83 V calibration -- DMM at the upper woofer terminals, tweeter
                         physically disconnected. Records -12 dBFS anchor.
  3. Timing-ref verify -- confirm REW's Acoustic Timing Reference is
                         using the small desk speaker on Arcam Front-Left.
  4. Acoustic sweeps  -- the 65-sweep matrix (H polar / V polar /
                         nearfield / distortion). API-automated when
                         possible, manual fallback otherwise.
  5. Export           -- trigger REW batch export (best-effort), or
                         walk the user through File -> Export.
  6. Sanity check     -- final coverage report vs the expected matrix.

Run:  python sweep_wizard.py
Optional:
      --base-url http://host:port  (default http://localhost:4735)
      --phase pre|dats|cal|ref|acoustic|export|sanity|all (default all)
      --log-path <path>            (default ./sweep_log.csv)
      --out-dir <path>             (default ./export)
      --manual                     force manual mode (skip API entirely)

Windows: tested on Python 3.10+. Requires no 3rd-party packages.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from measurement_matrix import (
    ACOUSTIC_SWEEPS,
    AcousticSweep,
    DATS_SWEEPS,
    DatsSweep,
    EXPECTED_COUNTS,
)
from prompts import (
    Action,
    ProgressLog,
    banner,
    dim,
    error,
    header_with_progress,
    info,
    ok,
    pause,
    print_log_summary,
    prompt_action,
    prompt_yn,
    safety,
    section,
    setup_console,
    subsection,
    warn,
)
from rew_api import RewApi


# ---------------------------------------------------------------------------
# Paths & defaults
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_LOG_PATH = SCRIPT_DIR / "sweep_log.csv"
DEFAULT_OUT_DIR = SCRIPT_DIR / "rew"

PHASES = ("pre", "dats", "cal", "ref", "acoustic", "export", "sanity", "all")


# ---------------------------------------------------------------------------
# Phase 0: pre-check
# ---------------------------------------------------------------------------

def phase_pre_check(api: RewApi, log: ProgressLog, manual: bool) -> bool:
    """Return True if we should proceed (user didn't quit)."""
    section("Phase 0: Pre-check")

    safety("TWEETER SAFETY — non-negotiable:")
    print("   - Tweeter sweeps use start=300 Hz, length=256 k, level=-12 dBFS.")
    print("   - Tweeter is PHYSICALLY DISCONNECTED during 2.83 V calibration.")
    print("   - Tweeter distortion sweep drops to -21 dBFS (~1 V).")
    print("   - If you hear tick/buzz/stress, stop the sweep immediately.")

    if not prompt_yn("Confirm tweeter-safety rules above", default=True):
        warn("Tweeter-safety not confirmed. Aborting.")
        return False

    subsection("REW API probe")
    if manual:
        warn("--manual flag set: skipping API probe. Running in guided-prompt mode.")
    else:
        res = api.probe()
        if res.reachable:
            ok(f"REW API reachable at {res.base_url} (version: {res.version}).")
            if res.openapi_available:
                dim("    OpenAPI spec available at /doc.json.")
        else:
            warn(f"REW API not reachable: {res.error}")
            dim("    Debug:")
            for line in res.debug_log:
                dim(f"      {line}")
            if not prompt_yn("Continue in manual guided-prompt mode?", default=True):
                return False

    subsection("Resume state")
    print_log_summary(log, total_expected=EXPECTED_COUNTS["grand_total"])

    info("Pre-check complete.")
    return True


# ---------------------------------------------------------------------------
# Phase 1: DATS impedance sweeps (guided only)
# ---------------------------------------------------------------------------

def phase_dats(log: ProgressLog) -> None:
    section("Phase 1: DATS impedance (7 sweeps)")
    info("DATS V3 sweeps are low-level and safe for all drivers, tweeter included.")
    info("Output: save each as <name>.zma and <name>.tzz (DATS 'Save Project') -> dats/ subfolder.")

    done = log.done_names()
    total = len(DATS_SWEEPS)
    for idx, sweep in enumerate(DATS_SWEEPS, 1):
        header_with_progress(f"DATS: {sweep.label}", idx, total)

        if sweep.name in done:
            dim(f"Already done: {sweep.name}. Skipping (use --phase dats and 'r' to redo).")
            continue

        print(f"  File stem: {sweep.name}")
        print(f"  Action:    {sweep.action}")
        if sweep.expected_fc_hz is not None:
            print(f"  Expect:    Fc ~= {sweep.expected_fc_hz:.1f} Hz, "
                  f"Qtc ~= {sweep.expected_qtc:.2f}" if sweep.expected_qtc
                  else f"  Expect:    Fc ~= {sweep.expected_fc_hz:.1f} Hz")
        if sweep.expected_fs_hz is not None:
            print(f"  Expect:    Fs ~= {sweep.expected_fs_hz:.0f} Hz")

        action = prompt_action("After saving in DATS: [Enter]=done  [s]=skip  [r]=redo  [q]=quit")
        if action is Action.QUIT:
            info("Quit requested; DATS phase ending.")
            return
        if action is Action.SKIP:
            log.record("dats", sweep.name, "skipped")
            warn(f"Skipped {sweep.name}.")
            continue
        if action is Action.REDO:
            log.record("dats", sweep.name, "redo-requested")
            warn("Redo requested. Re-run DATS for this entry, then press Enter.")
            pause()
        log.record("dats", sweep.name, "done")
        ok(f"Logged {sweep.name} as done.")

    ok("DATS phase complete.")


# ---------------------------------------------------------------------------
# Phase 2: 2.83 V calibration
# ---------------------------------------------------------------------------

def phase_calibration(log: ProgressLog) -> None:
    section("Phase 2: 2.83 V calibration (woofer only)")
    safety("TWEETER MUST BE PHYSICALLY DISCONNECTED at the wall for this step.")

    steps = [
        "Confirm tweeter wires are DISCONNECTED at the wall terminals.",
        "Connect W1 (upper woofer) to Arcam Front-Right output.",
        "Set Arcam volume to a known reference (e.g., -20 dB). Do not change after.",
        "Put DMM probes on the W1 terminals, set to AC Volts, 20 V range.",
        "In REW: generator tab, select 60 Hz sine, start at -20 dBFS.",
        "Play tone; raise generator level until DMM reads 2.83 V AC (+/- 0.05 V).",
        "Record the REW generator dBFS value — this is the calibrated -12 dBFS anchor.",
        "Stop the tone. Tweeter stays disconnected until polar phase starts.",
    ]
    for i, text in enumerate(steps, 1):
        print(f"  {i}. {text}")

    if prompt_yn("Calibration complete and DMM reads 2.83 V at the dBFS you recorded?",
                 default=True):
        log.record("calibration", "2V83-anchor", "done",
                   notes="2.83 V at recorded REW generator dBFS")
        ok("Calibration anchor recorded.")
    else:
        log.record("calibration", "2V83-anchor", "skipped")
        warn("Calibration skipped or failed. Acoustic SPL scaling will be approximate.")


# ---------------------------------------------------------------------------
# Phase 3: timing-reference verification
# ---------------------------------------------------------------------------

def phase_timing_ref(log: ProgressLog) -> None:
    section("Phase 3: Acoustic Timing Reference verify")
    info("REW's Acoustic Timing Reference lets the single-channel UMIK-1 "
         "produce minimum-phase-preserving FRD files across multiple drivers.")
    print()
    print("  Signal chain:")
    print("    Laptop 3.5 mm -> splitter -> Arcam 7.1 multichannel input")
    print("    Left channel  -> Arcam Front-Left  -> small desk speaker (timing ref)")
    print("    Right channel -> Arcam Front-Right -> DUT (driver under test)")
    print("    UMIK-1 USB    -> laptop (measurement mic)")
    print()
    print("  In REW:")
    print("    Preferences > Analysis > 'Use acoustic timing reference' = ON")
    print("    Generator   > Reference output = Left (the desk speaker on Arcam FL)")
    print("    Reference pilot tone at a modest level (audible at mic, not loud).")

    if not prompt_yn("Run a test sweep and confirm REW shows a timing-reference peak?",
                     default=True):
        log.record("timing_ref", "verify", "skipped")
        warn("Timing reference not verified. Polars may lack coherent phase between drivers.")
        return

    if prompt_yn("Did REW see the timing-reference peak and lock on?", default=True):
        log.record("timing_ref", "verify", "done")
        ok("Timing reference verified.")
    else:
        log.record("timing_ref", "verify", "failed")
        warn("Timing reference failed. Troubleshoot before acoustic sweeps.")
        print("  Likely causes: desk speaker muted, wrong Arcam input, splitter polarity,")
        print("  REW reference channel set wrong, pilot level too low for room noise.")


# ---------------------------------------------------------------------------
# Phase 4: acoustic sweeps
# ---------------------------------------------------------------------------

def phase_acoustic(api: RewApi, log: ProgressLog, manual: bool) -> None:
    section("Phase 4: Acoustic sweeps (65 total)")

    done = log.done_names()
    remaining = [s for s in ACOUSTIC_SWEEPS if s.name not in done]
    total = len(ACOUSTIC_SWEEPS)
    already = total - len(remaining)
    if already:
        info(f"{already} of {total} already logged 'done'. Resuming with {len(remaining)} remaining.")
    if not remaining:
        ok("No acoustic sweeps remaining. Skipping phase.")
        return

    current_phase: Optional[str] = None
    for idx, sweep in enumerate(remaining, 1):
        if sweep.phase != current_phase:
            current_phase = sweep.phase
            subsection(f"Sub-phase: {current_phase}")

        global_idx = ACOUSTIC_SWEEPS.index(sweep) + 1
        header_with_progress(
            f"{sweep.name}  ({sweep.angle_desc})",
            global_idx, total,
        )
        print(f"  Phase:   {sweep.phase}")
        print(f"  Sweep:   {sweep.start_freq_hz}-{sweep.end_freq_hz} Hz, "
              f"{sweep.sweep_length // 1024} k, {sweep.level_dbfs} dBFS")
        print(f"  Action:  {sweep.action}")
        if sweep.safety_note:
            safety(sweep.safety_note)

        action = prompt_action(
            "Ready to measure? [Enter]=go  [s]=skip  [r]=redo-previous  [q]=quit",
        )
        if action is Action.QUIT:
            info("Quit requested; acoustic phase ending.")
            return
        if action is Action.SKIP:
            log.record("acoustic", sweep.name, "skipped")
            warn(f"Skipped {sweep.name}.")
            continue
        if action is Action.REDO:
            warn("Redo re-runs the current sweep. Press Enter when mic/wires are ready.")
            pause()

        _run_one_sweep(api, sweep, log, manual=manual)

    ok("Acoustic phase complete.")


def _run_one_sweep(
    api: RewApi, sweep: AcousticSweep, log: ProgressLog, manual: bool,
) -> None:
    """Measure one sweep. API-automated if possible, manual fallback otherwise."""
    if manual:
        _run_sweep_manual(sweep, log)
        return

    info(f"Starting REW measurement for {sweep.name} ...")
    result = api.measure(sweep)

    if result.ok:
        notes = []
        if result.duration_s is not None:
            notes.append(f"{result.duration_s:.1f}s")
        if result.measurement_id is not None:
            notes.append(f"id={result.measurement_id}")
        if result.overload:
            notes.append("OVERLOAD")
        log.record(
            "acoustic", sweep.name, "done",
            duration_s=result.duration_s,
            notes=",".join(notes),
        )
        if result.overload:
            warn(f"{sweep.name}: REW reported OVERLOAD. Lower level or redo.")
        else:
            ok(f"{sweep.name}: done ({','.join(notes) or 'ok'}).")
        return

    # API failed — fall back to manual.
    warn(f"REW API could not run sweep automatically: {result.error}")
    dim("    Debug:")
    for line in result.debug_log:
        dim(f"      {line}")
    _run_sweep_manual(sweep, log)


def _run_sweep_manual(sweep: AcousticSweep, log: ProgressLog) -> None:
    """Walk the user through a manual REW sweep when the API can't help."""
    warn("Manual mode: trigger the sweep yourself in REW.")
    print(f"    1. In REW, set generator: {sweep.start_freq_hz}-{sweep.end_freq_hz} Hz,")
    print(f"       length={sweep.sweep_length // 1024} k, level={sweep.level_dbfs} dBFS,")
    print(f"       acoustic timing reference ON.")
    print(f"    2. Name the measurement: {sweep.name}")
    print(f"    3. Start the sweep and wait for it to finish.")

    action = prompt_action(
        "When the sweep finishes: [Enter]=done  [s]=skip  [r]=redo  [q]=quit",
        allow_redo=True,
    )
    if action is Action.QUIT:
        raise KeyboardInterrupt
    if action is Action.SKIP:
        log.record("acoustic", sweep.name, "skipped", notes="manual")
        warn(f"Skipped {sweep.name}.")
        return
    if action is Action.REDO:
        warn("Redo requested. Run the sweep again, then press Enter.")
        pause()
    log.record("acoustic", sweep.name, "done", notes="manual")
    ok(f"{sweep.name}: logged as done (manual).")


# ---------------------------------------------------------------------------
# Phase 5: export
# ---------------------------------------------------------------------------

def phase_export(api: RewApi, log: ProgressLog, out_dir: Path, manual: bool) -> None:
    section("Phase 5: Export measurements")
    out_dir.mkdir(parents=True, exist_ok=True)
    info(f"Target directory: {out_dir}")

    print("  Desired per-sweep outputs:")
    print("    - .frd  (3-col: freq, SPL, phase)  -- loudspeakerlab + VituixCAD")
    print("    - .txt  (REW text export)          -- fallback / inspection")
    print("    - .wav  (impulse response)         -- optional, re-gate later")
    print("  Plus one master REW session file (.mdat) covering every sweep.")

    if not manual:
        info("Attempting REW batch export via API ...")
        result = api.export_all(out_dir)
        if result.ok:
            ok(f"API export succeeded. Files reported: {len(result.files_written)}.")
            for f in result.files_written[:10]:
                dim(f"    {f}")
            if len(result.files_written) > 10:
                dim(f"    ... and {len(result.files_written) - 10} more")
            log.record("export", "batch", "done",
                       notes=f"api, {len(result.files_written)} files")
            return
        warn(f"Batch export via API failed: {result.error}")
        dim("    Debug:")
        for line in result.debug_log:
            dim(f"      {line}")

    # Manual fallback
    warn("Falling back to manual export.")
    print("  In REW:")
    print("    1. Select ALL measurements in the left panel.")
    print(f"    2. File > Export > Measurement as text  ->  {out_dir}/frd/")
    print(f"    3. File > Export > Impulse response as WAV  ->  {out_dir}/wav/")
    print(f"    4. File > Save As  ->  {out_dir}/WMTMW_session.mdat")
    pause("Press Enter when manual export is complete.")
    log.record("export", "batch", "done", notes="manual")
    ok("Export phase logged.")


# ---------------------------------------------------------------------------
# Phase 6: sanity check
# ---------------------------------------------------------------------------

def phase_sanity(log: ProgressLog) -> None:
    section("Phase 6: Sanity check")

    latest = log._latest_status_by_name()

    expected_names = {s.name for s in ACOUSTIC_SWEEPS} | {s.name for s in DATS_SWEEPS}
    done_names = {n for n, s in latest.items() if s == "done"}
    missing = sorted(expected_names - done_names)
    extras = sorted(done_names - expected_names)  # calibration/ref entries show up here

    counts = log.counts_by_status()
    info(f"Final counts by status: {counts}")
    info(f"Expected acoustic+DATS matrix: {len(expected_names)} entries.")
    info(f"Matrix entries marked 'done':  {len(done_names & expected_names)}.")

    if missing:
        warn(f"Missing {len(missing)} entries from the matrix:")
        for n in missing[:20]:
            print(f"    - {n}")
        if len(missing) > 20:
            print(f"    ... and {len(missing) - 20} more")
    else:
        ok("All 72 matrix entries have a 'done' row. Session is complete.")

    if extras:
        dim("Non-matrix entries also logged (calibration / timing ref / etc):")
        for n in extras:
            dim(f"    - {n} [{latest[n]}]")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="sweep_wizard",
        description="WMTMW in-box measurement orchestrator.",
    )
    p.add_argument("--base-url", default="http://localhost:4735",
                   help="REW HTTP API base URL.")
    p.add_argument("--phase", choices=PHASES, default="all",
                   help="Run a single phase, or 'all' (default).")
    p.add_argument("--log-path", type=Path, default=DEFAULT_LOG_PATH,
                   help="CSV progress log path.")
    p.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR,
                   help="Export target directory.")
    p.add_argument("--manual", action="store_true",
                   help="Force manual guided-prompt mode (skip REW API).")
    return p.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])

    setup_console()
    banner()

    log = ProgressLog(args.log_path)
    api = RewApi(base_url=args.base_url)

    run = args.phase
    try:
        if run in ("pre", "all"):
            if not phase_pre_check(api, log, manual=args.manual):
                return 1
        if run in ("dats", "all"):
            phase_dats(log)
        if run in ("cal", "all"):
            phase_calibration(log)
        if run in ("ref", "all"):
            phase_timing_ref(log)
        if run in ("acoustic", "all"):
            phase_acoustic(api, log, manual=args.manual)
        if run in ("export", "all"):
            phase_export(api, log, args.out_dir, manual=args.manual)
        if run in ("sanity", "all"):
            phase_sanity(log)
    except KeyboardInterrupt:
        print()
        warn("Interrupted by user. Progress is saved in the CSV; rerun to resume.")
        return 130

    section("Wizard complete")
    info(f"Log:    {args.log_path}")
    info(f"Export: {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
