"""
measurement_matrix.py
=====================

Data module: the full 72-measurement matrix for the WMTMW in-wall session.
No logic, no I/O, no API calls — just structured records the wizard consumes.

Counts (must match Measurement_Runbook.md):
  Horizontal polars:  50  (10 angles × 5 drivers)
  Vertical polars:     6  (2 angles × 3 drivers: T/M3/M4)
  Nearfield:           4  (W1/W2/M3/M4; tweeter excluded)
  Distortion:          5  (all drivers; tweeter at 1 V)
  Acoustic total:     65
  DATS impedance:      7  (5 individual + 2 pair)
  Grand total:        72 measurements
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional


# ---------------------------------------------------------------------------
# Type definitions
# ---------------------------------------------------------------------------

Phase = Literal["h_polar", "v_polar", "nearfield", "distortion"]


@dataclass(frozen=True)
class DriverInfo:
    tag: str               # short key used in filenames, e.g. "W1"
    name: str              # human-readable CamelCase, e.g. "UpperWoofer"
    kind: str              # "woofer" | "mid" | "tweeter"
    description: str       # plain English for prompts, e.g. "upper woofer"


@dataclass(frozen=True)
class AcousticSweep:
    """One REW acoustic measurement: driver × angle × phase."""
    name: str              # filename stem, e.g. "W1-UpperWoofer-H000deg"
    driver_tag: str        # "W1"
    driver_name: str       # "UpperWoofer"
    phase: Phase
    angle_desc: str        # "0° horizontal" | "+15° vertical" | "on-axis nearfield"
    start_freq_hz: int
    end_freq_hz: int
    sweep_length: int      # samples (power of 2): 524_288 = 512 k, 262_144 = 256 k
    level_dbfs: float      # REW generator level (−12 dBFS = 2.83 V calibrated)
    action: str            # instruction text printed by the wizard
    safety_note: str = ""
    is_tweeter: bool = False


@dataclass(frozen=True)
class DatsSweep:
    """One DATS V3 impedance measurement (guided-only, no API)."""
    name: str              # filename stem, e.g. "W1-UpperWoofer-InBox"
    label: str             # short label, e.g. "Upper woofer alone"
    action: str            # step-by-step instruction for user at DATS
    expected_fc_hz: Optional[float] = None   # sealed-box resonance (woofer/mid in-box)
    expected_qtc: Optional[float] = None     # sealed alignment Q (woofer)
    expected_fs_hz: Optional[float] = None   # tweeter / pair resonance


# ---------------------------------------------------------------------------
# Driver catalog
# ---------------------------------------------------------------------------

DRIVERS: dict[str, DriverInfo] = {
    "W1": DriverInfo("W1", "UpperWoofer", "woofer",  "upper woofer"),
    "W2": DriverInfo("W2", "LowerWoofer", "woofer",  "lower woofer"),
    "M3": DriverInfo("M3", "UpperMid",    "mid",     "upper mid"),
    "M4": DriverInfo("M4", "LowerMid",    "mid",     "lower mid"),
    "T":  DriverInfo("T",  "Tweeter",     "tweeter", "tweeter"),
}


# ---------------------------------------------------------------------------
# Angle and driver groupings
# ---------------------------------------------------------------------------

HORIZONTAL_ANGLES = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]  # one-sided (horizontal symmetry)
VERTICAL_ANGLES_UP = [15, 30]                                 # upward only (vertical symmetry)
VERTICAL_DRIVERS = ["T", "M3", "M4"]                          # woofers are omni at XO freqs
NEARFIELD_DRIVERS = ["W1", "W2", "M3", "M4"]                  # tweeter nearfield is meaningless
DISTORTION_DRIVERS = ["W1", "W2", "M3", "M4", "T"]            # all; tweeter at 1 V

# Geometry labels for the vertical mic offsets (from 1 m on-axis reference)
VERTICAL_GEOMETRY: dict[int, str] = {
    15: "mic ~97 cm out from baffle, ~26 cm above tweeter height",
    30: "mic ~87 cm out from baffle, ~50 cm above tweeter height",
}


# ---------------------------------------------------------------------------
# Sweep parameter presets
# ---------------------------------------------------------------------------

# Calibrated 2.83 V → -12 dBFS per the calibration step
CALIBRATED_DBFS_2_83V = -12.0

# -21 dBFS = 9 dB below 2.83 V ≈ 1.00 V (for tweeter distortion)
CALIBRATED_DBFS_1V = -21.0

FULL_RANGE = dict(
    start_freq_hz=20,
    end_freq_hz=20_000,
    sweep_length=524_288,          # 512 k
    level_dbfs=CALIBRATED_DBFS_2_83V,
)

TWEETER_SAFE = dict(
    start_freq_hz=300,
    end_freq_hz=20_000,
    sweep_length=262_144,          # 256 k (shorter thermal dose)
    level_dbfs=CALIBRATED_DBFS_2_83V,
)

TWEETER_DISTORTION_1V = dict(
    start_freq_hz=300,
    end_freq_hz=20_000,
    sweep_length=262_144,
    level_dbfs=CALIBRATED_DBFS_1V,
)


# ---------------------------------------------------------------------------
# Safety text blocks
# ---------------------------------------------------------------------------

TWEETER_SAFETY = (
    "TWEETER SWEEP. Verify REW generator: start=300 Hz, length=256 k, "
    "level=-12 dBFS. Wear hearing protection. If you hear any tick, buzz, "
    "or stress during the sweep, STOP immediately."
)

TWEETER_1V_SAFETY = (
    "TWEETER DISTORTION AT 1 V. Drop REW generator level by 9 dB "
    "(−12 dBFS → −21 dBFS). Start=300 Hz, length=256 k. Filename suffix "
    "'-1V' records the level. Wear hearing protection."
)

NEARFIELD_NOTE = (
    "Mic tip <5 mm from dust cap center, pointed axially into the driver. "
    "No gate applied. Timing reference remains active."
)


# ---------------------------------------------------------------------------
# Horizontal polar sweeps (50)
# ---------------------------------------------------------------------------

H_POLAR_SWEEPS: list[AcousticSweep] = []
for _angle in HORIZONTAL_ANGLES:
    _angle_desc = f"{_angle}° horizontal"
    for _tag in ["W1", "W2", "M3", "M4"]:
        _drv = DRIVERS[_tag]
        H_POLAR_SWEEPS.append(AcousticSweep(
            name=f"{_tag}-{_drv.name}-H{_angle:03d}deg",
            driver_tag=_tag,
            driver_name=_drv.name,
            phase="h_polar",
            angle_desc=_angle_desc,
            action=(
                f"Mic at the {_angle}° H tape mark, 1.00 m from tweeter, tweeter height. "
                f"At the wall: disconnect previous driver, connect the {_drv.description} "
                f"to Arcam FR. All other drivers stay disconnected."
            ),
            **FULL_RANGE,
        ))
    # Tweeter row — tweeter-safe params
    H_POLAR_SWEEPS.append(AcousticSweep(
        name=f"T-Tweeter-H{_angle:03d}deg",
        driver_tag="T",
        driver_name="Tweeter",
        phase="h_polar",
        angle_desc=_angle_desc,
        action=(
            f"Mic at the {_angle}° H tape mark. Confirm REW: start=300 Hz, length=256 k. "
            f"Connect the tweeter to Arcam FR; all others disconnected. Ear protection on."
        ),
        safety_note=TWEETER_SAFETY,
        is_tweeter=True,
        **TWEETER_SAFE,
    ))


# ---------------------------------------------------------------------------
# Vertical polar sweeps (6) — upward only, vertically symmetric
# ---------------------------------------------------------------------------

V_POLAR_SWEEPS: list[AcousticSweep] = []
for _angle in VERTICAL_ANGLES_UP:
    _angle_desc = f"+{_angle}° vertical"
    _geom = VERTICAL_GEOMETRY[_angle]
    for _tag in VERTICAL_DRIVERS:
        _drv = DRIVERS[_tag]
        _action = (
            f"Move mic to {_geom}. Verify 1 m string from tweeter to mic tip. "
            f"Connect the {_drv.description} to Arcam FR; all others disconnected."
        )
        if _tag == "T":
            V_POLAR_SWEEPS.append(AcousticSweep(
                name=f"T-Tweeter-V{_angle:03d}deg",
                driver_tag="T",
                driver_name="Tweeter",
                phase="v_polar",
                angle_desc=_angle_desc,
                action=_action + " Confirm REW: start=300 Hz, length=256 k. Ear protection on.",
                safety_note=TWEETER_SAFETY,
                is_tweeter=True,
                **TWEETER_SAFE,
            ))
        else:
            V_POLAR_SWEEPS.append(AcousticSweep(
                name=f"{_tag}-{_drv.name}-V{_angle:03d}deg",
                driver_tag=_tag,
                driver_name=_drv.name,
                phase="v_polar",
                angle_desc=_angle_desc,
                action=_action,
                **FULL_RANGE,
            ))


# ---------------------------------------------------------------------------
# Nearfield sweeps (4) — W1, W2, M3, M4 only
# ---------------------------------------------------------------------------

NEARFIELD_SWEEPS: list[AcousticSweep] = [
    AcousticSweep(
        name=f"{_tag}-{DRIVERS[_tag].name}-NearField",
        driver_tag=_tag,
        driver_name=DRIVERS[_tag].name,
        phase="nearfield",
        angle_desc="on-axis nearfield",
        action=(
            f"Position mic tip <5 mm from the center of the {DRIVERS[_tag].description}'s "
            f"dust cap, pointed axially into the cone. No gating. "
            f"Connect the {DRIVERS[_tag].description} to Arcam FR; all others disconnected."
        ),
        safety_note=NEARFIELD_NOTE,
        **FULL_RANGE,
    )
    for _tag in NEARFIELD_DRIVERS
]


# ---------------------------------------------------------------------------
# Distortion sweeps (5) — on-axis, stepped sine or long log
# ---------------------------------------------------------------------------

DISTORTION_SWEEPS: list[AcousticSweep] = []
for _tag in DISTORTION_DRIVERS:
    _drv = DRIVERS[_tag]
    if _tag == "T":
        DISTORTION_SWEEPS.append(AcousticSweep(
            name=f"T-Tweeter-Distortion-1V",
            driver_tag="T",
            driver_name="Tweeter",
            phase="distortion",
            angle_desc="on-axis distortion at 1 V",
            action=(
                "Mic back at 0° H tape mark, 1 m on-axis. "
                "REW: switch to Distortion measurement, set level to -21 dBFS (1 V), "
                "start=300 Hz, length=256 k. Connect tweeter to Arcam FR. "
                "Ear protection on."
            ),
            safety_note=TWEETER_1V_SAFETY,
            is_tweeter=True,
            **TWEETER_DISTORTION_1V,
        ))
    else:
        DISTORTION_SWEEPS.append(AcousticSweep(
            name=f"{_tag}-{_drv.name}-Distortion",
            driver_tag=_tag,
            driver_name=_drv.name,
            phase="distortion",
            angle_desc="on-axis distortion at 2.83 V",
            action=(
                f"Mic back at 0° H tape mark, 1 m on-axis. "
                f"REW: Distortion measurement, full range 20 Hz–20 kHz, level -12 dBFS (2.83 V). "
                f"Connect the {_drv.description} to Arcam FR; all others disconnected."
            ),
            **FULL_RANGE,
        ))


# ---------------------------------------------------------------------------
# Unified acoustic matrix (65 sweeps) — the wizard walks this in order
# ---------------------------------------------------------------------------

ACOUSTIC_SWEEPS: list[AcousticSweep] = (
    H_POLAR_SWEEPS + V_POLAR_SWEEPS + NEARFIELD_SWEEPS + DISTORTION_SWEEPS
)


# ---------------------------------------------------------------------------
# DATS impedance sweeps (7) — guided, no API
# ---------------------------------------------------------------------------

DATS_SWEEPS: list[DatsSweep] = [
    DatsSweep(
        name="W1-UpperWoofer-InBox",
        label="Upper woofer alone (in-box)",
        action=(
            "At the wall: disconnect everything. Connect only W1 (upper woofer) to DATS. "
            "Run impedance sweep. Save as W1-UpperWoofer-InBox.zma in zma/ subfolder. "
            "Also Save Project (.tzz). Note Fc and Qtc."
        ),
        expected_fc_hz=56.0,
        expected_qtc=0.71,
    ),
    DatsSweep(
        name="W2-LowerWoofer-InBox",
        label="Lower woofer alone (in-box)",
        action=(
            "Disconnect W1. Connect only W2 (lower woofer) to DATS. "
            "Run sweep. Save as W2-LowerWoofer-InBox.zma (+ .tzz). Note Fc and Qtc."
        ),
        expected_fc_hz=55.0,
        expected_qtc=0.67,
    ),
    DatsSweep(
        name="M3-UpperMid-InBox",
        label="Upper mid alone (in-box)",
        action=(
            "Disconnect W2. Connect only M3 (upper mid) to DATS. "
            "Run sweep. Save as M3-UpperMid-InBox.zma (+ .tzz)."
        ),
        expected_fs_hz=130.0,  # shared chamber, in-box rise from 52.7 Hz free-air Fs
    ),
    DatsSweep(
        name="M4-LowerMid-InBox",
        label="Lower mid alone (in-box)",
        action=(
            "Disconnect M3. Connect only M4 (lower mid) to DATS. "
            "Run sweep. Save as M4-LowerMid-InBox.zma (+ .tzz)."
        ),
        expected_fs_hz=130.0,
    ),
    DatsSweep(
        name="T-Tweeter-InBox",
        label="Tweeter alone (in-box)",
        action=(
            "Disconnect M4. Connect only T (tweeter) to DATS. "
            "Run sweep. Save as T-Tweeter-InBox.zma (+ .tzz). "
            "DATS sweeps are low-level, safe for tweeters."
        ),
        expected_fs_hz=650.0,
    ),
    DatsSweep(
        name="Pair-Woofers-InBox",
        label="Woofer pair (W1 + W2) in parallel",
        action=(
            "Wire W1 and W2 in parallel at the DATS terminals (both + to +, both − to −). "
            "Run sweep. Save as Pair-Woofers-InBox.zma (+ .tzz). "
            "Expected: ~half the impedance magnitude of one woofer alone."
        ),
    ),
    DatsSweep(
        name="Pair-Mids-InBox",
        label="Mid pair (M3 + M4) in parallel",
        action=(
            "Wire M3 and M4 in parallel at the DATS terminals. "
            "Run sweep. Save as Pair-Mids-InBox.zma (+ .tzz)."
        ),
    ),
]


# ---------------------------------------------------------------------------
# Expected totals (asserted at import time as a sanity check)
# ---------------------------------------------------------------------------

EXPECTED_COUNTS = {
    "h_polar":    50,
    "v_polar":     6,
    "nearfield":   4,
    "distortion":  5,
    "acoustic":   65,
    "dats":        7,
    "grand_total": 72,
}

assert len(H_POLAR_SWEEPS)    == EXPECTED_COUNTS["h_polar"],   "H polar count drift"
assert len(V_POLAR_SWEEPS)    == EXPECTED_COUNTS["v_polar"],   "V polar count drift"
assert len(NEARFIELD_SWEEPS)  == EXPECTED_COUNTS["nearfield"], "Nearfield count drift"
assert len(DISTORTION_SWEEPS) == EXPECTED_COUNTS["distortion"], "Distortion count drift"
assert len(ACOUSTIC_SWEEPS)   == EXPECTED_COUNTS["acoustic"],  "Acoustic total drift"
assert len(DATS_SWEEPS)       == EXPECTED_COUNTS["dats"],      "DATS count drift"
assert (len(ACOUSTIC_SWEEPS) + len(DATS_SWEEPS)
        == EXPECTED_COUNTS["grand_total"]),                    "Grand total drift"


# ---------------------------------------------------------------------------
# Verification helper (optional — run as `python measurement_matrix.py`)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("WMTMW Measurement Matrix")
    print("=" * 60)
    print(f"Horizontal polar sweeps : {len(H_POLAR_SWEEPS):3d}")
    print(f"Vertical polar sweeps   : {len(V_POLAR_SWEEPS):3d}")
    print(f"Nearfield sweeps        : {len(NEARFIELD_SWEEPS):3d}")
    print(f"Distortion sweeps       : {len(DISTORTION_SWEEPS):3d}")
    print(f"Acoustic total          : {len(ACOUSTIC_SWEEPS):3d}")
    print(f"DATS impedance sweeps   : {len(DATS_SWEEPS):3d}")
    print(f"Grand total             : {len(ACOUSTIC_SWEEPS) + len(DATS_SWEEPS):3d}")
    print()
    print("First 3 acoustic sweeps:")
    for s in ACOUSTIC_SWEEPS[:3]:
        print(f"  {s.name}  [{s.phase}, {s.start_freq_hz}-{s.end_freq_hz} Hz, "
              f"{s.sweep_length // 1024}k, {s.level_dbfs} dBFS]")
    print()
    print("All tweeter sweeps (should all have start_freq_hz=300):")
    for s in ACOUSTIC_SWEEPS:
        if s.is_tweeter:
            print(f"  {s.name}  start={s.start_freq_hz} Hz  level={s.level_dbfs} dBFS")
