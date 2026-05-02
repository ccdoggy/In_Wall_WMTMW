"""Scan existing output files and map them back to measurement names.

Returns which measurements are already covered by files on disk,
so the GUI can offer to bulk-mark them done without re-measuring.

Mapping rules:
  DATS    → dats/{name}.zma              (canonical DATS output)
  Acoustic → any of:
               {frd_dir}/{name}.frd      (primary; frd_dir = out_dir/frd or out_dir)
               {frd_dir}/{name}.txt      (REW text export)
               {frd_dir}/{name}.wav      (impulse response)

The check is case-insensitive (Windows filesystems are case-insensitive but
Python's Path.glob is not, so we lower-case everything).
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from measurement_matrix import ACOUSTIC_SWEEPS, DATS_SWEEPS, AcousticSweep, DatsSweep


# Extensions to treat as "file exists" evidence, in priority order
_DATS_EXTS    = (".zma", ".tzz", ".txt")
_ACOUSTIC_EXTS = (".frd", ".txt", ".wav")


@dataclass
class ScanResult:
    """One measurement that has a matching file on disk."""
    name: str           # sweep.name (used as the progress-log key)
    phase: str          # "dats" | "h_polar" | "v_polar" | "nearfield" | "distortion"
    label: str          # human-readable label for the dialog
    found_path: Path    # the file that proved this measurement exists


def scan(
    dats_dir: Path,
    frd_dir: Path,
    already_done: set[str],
) -> list[ScanResult]:
    """Scan directories and return measurements found on disk that aren't yet logged done.

    Args:
        dats_dir:     directory containing .zma files (typically InBoxMeasurements/dats/)
        frd_dir:      directory containing .frd/.txt/.wav files from REW export
                      (typically rew/ or rew/frd/ — we search both)
        already_done: set of names already marked done in sweep_log.csv
    """
    results: list[ScanResult] = []

    # Build case-insensitive stem→path index for each directory we'll search
    dats_index   = _build_index(dats_dir, _DATS_EXTS)
    frd_index    = _build_index(frd_dir, _ACOUSTIC_EXTS)
    # Also try frd_dir/frd/ as a subdirectory (REW sometimes creates this)
    frd_sub_index = _build_index(frd_dir / "frd", _ACOUSTIC_EXTS)
    frd_combined = {**frd_sub_index, **frd_index}  # frd_index wins on collision

    # --- DATS sweeps ---
    for sweep in DATS_SWEEPS:
        if sweep.name in already_done:
            continue
        path = _lookup(sweep.name, dats_index)
        if path:
            results.append(ScanResult(
                name=sweep.name,
                phase="dats",
                label=f"DATS: {sweep.label}",
                found_path=path,
            ))

    # --- Acoustic sweeps ---
    for sweep in ACOUSTIC_SWEEPS:
        if sweep.name in already_done:
            continue
        path = _lookup(sweep.name, frd_combined)
        if path:
            results.append(ScanResult(
                name=sweep.name,
                phase=sweep.phase,
                label=f"{sweep.driver_tag}  {sweep.angle_desc}  [{sweep.phase}]",
                found_path=path,
            ))

    return results


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_index(directory: Path, exts: tuple[str, ...]) -> dict[str, Path]:
    """Return {lower-case stem: path} for every file in directory with a matching ext."""
    index: dict[str, Path] = {}
    if not directory.is_dir():
        return index
    for ext in exts:
        for path in directory.iterdir():
            if path.suffix.lower() == ext and path.stem.lower() not in index:
                index[path.stem.lower()] = path
    return index


def _lookup(name: str, index: dict[str, Path]) -> Optional[Path]:
    return index.get(name.lower())
