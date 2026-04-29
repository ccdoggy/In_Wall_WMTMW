# InBoxMeasurements — wizard usage

Python wizard that walks the WMTMW prototype through its full in-box
characterization session. Pairs with the printable runbook
(`Measurement_Runbook.md` / `.html`) — the runbook is the source of truth for
physical setup, the wizard drives the software.

## Files in this folder

| File | Role |
|------|------|
| `Measurement_Runbook.md` | Printable runbook. Equipment, signal chain, arc geometry, safety, full matrix. |
| `measurement_matrix.py`  | Pure data: 77 acoustic sweeps + 7 DATS sweeps as structured records. |
| `rew_api.py`             | Thin adapter for the REW HTTP API (REW 5.20+). Never raises. |
| `prompts.py`             | UI helpers (banner, section headers, progress log, yes/no, action prompt). |
| `sweep_wizard.py`        | **Main entry point.** Orchestrates all phases. |
| `sweep_log.csv`          | Written at runtime. Append-only CSV; latest row per name wins for resume. |
| `export/`                | Written at runtime. REW batch-export target. |

## Requirements

* Windows laptop (Linux/macOS also fine) with Python 3.10+.
* No third-party Python packages — stdlib only.
* REW 5.20 or newer with the HTTP API enabled:
  `Preferences > API > Enable API`, or launch REW with `-api`.
  Default URL is `http://localhost:4735`.
* UMIK-1, DATS V3, multimeter, Arcam AVR350, small desk speaker for timing
  reference. See `Measurement_Runbook.md` for the full signal chain.

## Quick start

From this folder:

```
python sweep_wizard.py
```

That runs every phase in order. On a fresh session, expect ~2 hours of
acoustic sweeps plus time for DATS and calibration.

### Common invocations

```
# Force guided-prompt mode (skip the REW API entirely).
python sweep_wizard.py --manual

# Run just one phase (useful after a break).
python sweep_wizard.py --phase dats
python sweep_wizard.py --phase acoustic
python sweep_wizard.py --phase sanity

# Point at a REW on another machine.
python sweep_wizard.py --base-url http://10.0.0.42:4735

# Put the log and exports somewhere else.
python sweep_wizard.py --log-path D:\wmtmw\sweep_log.csv --out-dir D:\wmtmw\export
```

Available phases: `pre`, `dats`, `cal`, `ref`, `acoustic`, `export`, `sanity`,
`all` (default).

## What the wizard does

1. **Pre-check** — probes the REW API, restates tweeter-safety rules, and
   prints a resume summary from `sweep_log.csv`.
2. **DATS** — walks you through the 7 impedance sweeps (5 individual drivers
   + 2 parallel pairs). Prints expected Fc/Qtc/Fs per driver. DATS is manual
   (no API) — the wizard just prompts and logs.
3. **Calibration** — 2.83 V anchor at the upper woofer terminals with the
   tweeter physically disconnected. Records the REW generator dBFS that gives
   2.83 V AC at 60 Hz.
4. **Timing-reference verify** — confirms REW's Acoustic Timing Reference is
   using the desk speaker on Arcam Front-Left.
5. **Acoustic sweeps** — 77 sweeps in order: horizontal polars (60) → vertical
   polars (8) → nearfield (4) → distortion (5). Polars include 12 `Pair-Mids`
   sweeps where M3 and M4 are driven in parallel — the operationally accurate
   measurement for a symmetric WMTMW. For sweeps that drive only one mid, the
   wizard requires a blocking yes/no confirmation that the **other mid's wall
   terminals are shorted** (jumper + to −) so its cone doesn't passively radiate
   in the shared chamber. Tries the REW API first; falls back to manual prompts.
6. **Export** — triggers REW batch export to `export/`. Falls back to a manual
   File → Export walkthrough.
7. **Sanity check** — compares logged 'done' names against the expected 84
   entries and lists anything missing.

## Interactive prompts

At every measurement step you get four choices:

| Key | Action |
|-----|--------|
| `Enter` (or `g`, `y`) | Run the sweep / mark as done |
| `s` | Skip (logs 'skipped' and moves on) |
| `r` | Redo (repeat this step, then prompt again) |
| `q` | Quit cleanly (progress is saved; rerun to resume) |

`Ctrl-C` behaves like `q`: state is saved, exit code 130.

## Resume logic

Every attempt appends one row to `sweep_log.csv` with a timestamp. The wizard
uses the **latest** row per name to decide status, so:

* Re-running with the same log skips anything whose most-recent status is
  `done`.
* A redo just appends a new `done` row — the previous one is effectively
  overridden.
* A `skipped` row can be overridden later by running the sweep and choosing
  `Enter` when prompted.

The CSV is human-readable; you can open it in Excel if you want to audit or
manually edit statuses.

## Tweeter safety (baked into the matrix)

All tweeter entries use `start=300 Hz, length=256 k, level=-12 dBFS`. The
distortion sweep drops the tweeter to `-21 dBFS` (~1 V). The 2.83 V
calibration phase requires the tweeter to be physically disconnected at the
wall terminals. These are enforced in the data, not just in the prompts.

## If the REW API doesn't work

The adapter in `rew_api.py` tries multiple candidate endpoints for every
operation (REW's API is still evolving and paths shift between releases).
If none respond, the wizard **does not fail** — it drops into manual
guided-prompt mode for that step and keeps going. You can also force manual
mode from the start with `--manual`.

When the API fails, the wizard prints a debug log showing the exact HTTP
attempts. If REW has moved an endpoint, update the `_*_PATHS` tuples at the
top of `rew_api.py` and rerun.

## Outputs after a full session

```
InBoxMeasurements/
├── sweep_log.csv                   # one row per measurement attempt
├── rew/                            # REW acoustic measurements
│   ├── WMTMW_session.mdat          # REW master session
│   ├── frd/   *.frd                # freq, SPL, phase — for VituixCAD / loudspeakerlab.io
│   ├── txt/   *.txt                # REW text export fallback
│   └── wav/   *.wav                # impulse responses (re-gate later if needed)
└── dats/                           # DATS impedance measurements
    ├── *.zma                       # primary impedance file (3-col: freq, |Z|, phase)
    └── *.tzz                       # DATS project file (re-export without re-sweeping)
```

Files are named by driver-role + angle/kind, e.g. `W1-UpperWoofer-H000deg.frd`,
`T-Tweeter-V015deg.frd`, `M3-UpperMid-NearField.frd`,
`Pair-Woofers-InBox.zma`. Naming is defined in `measurement_matrix.py` and
documented in `Measurement_Runbook.md`.

## Smoke tests

Each module runs as a script for a quick self-check:

```
python measurement_matrix.py    # prints count totals; asserts fire on drift
python rew_api.py               # probes REW at localhost:4735
python prompts.py               # exercises visual helpers + ProgressLog
python sweep_wizard.py --help   # CLI parse only
```
