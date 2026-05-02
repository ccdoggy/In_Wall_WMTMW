"""REW-driven measurement tab: left list + right detail panel.

Used for H-Polar, V-Polar, Nearfield, and Distortion phases.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from measurement_matrix import ACOUSTIC_SWEEPS, AcousticSweep
from rew_api import RewApi

from .session_state import SessionState
from .sweep_detail import SweepDetailPanel
from . import theme


# Phase literal → display info
_PHASE_META: dict[str, tuple[str, str]] = {
    "h_polar":    ("H-Polar",    "Horizontal polar sweeps (10 angles × drivers)"),
    "v_polar":    ("V-Polar",    "Vertical polar sweeps (2 angles × drivers)"),
    "nearfield":  ("Nearfield",  "Nearfield sweeps (<5 mm from dust cap)"),
    "distortion": ("Distortion", "Harmonic distortion sweeps"),
}


class SweepTab(QWidget):
    """One tab for a single acoustic phase (e.g. h_polar)."""

    def __init__(
        self,
        phase: str,
        session: SessionState,
        api: RewApi,
        export_dir: Path,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._phase = phase
        self._session = session
        self._api = api
        self._export_dir = export_dir

        # Sweeps for this phase in matrix order
        self._sweeps: list[AcousticSweep] = [
            s for s in ACOUSTIC_SWEEPS if s.phase == phase
        ]

        self._build_ui()
        self._refresh_list()

        session.progress_changed.connect(self._refresh_list)

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left: measurement list
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(8, 8, 4, 8)
        left_layout.setSpacing(6)

        list_header = QLabel(_PHASE_META.get(self._phase, (self._phase, ""))[1])
        list_header.setObjectName("section_label")
        left_layout.addWidget(list_header)

        self._list = QListWidget()
        self._list.setMinimumWidth(220)
        self._list.currentRowChanged.connect(self._on_row_changed)
        left_layout.addWidget(self._list)

        splitter.addWidget(left)

        # Right: detail panel
        self._detail = SweepDetailPanel(self._api, self._export_dir)
        self._detail.measure_accepted.connect(self._on_accepted)
        self._detail.measure_skipped.connect(self._on_skipped)
        self._detail.cancelled.connect(self._detail.clear)
        splitter.addWidget(self._detail)

        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 5)
        splitter.setSizes([240, 600])

        outer.addWidget(splitter)

    # ------------------------------------------------------------------
    # List management
    # ------------------------------------------------------------------

    def _refresh_list(self) -> None:
        done = self._session.done_names()
        current_row = self._list.currentRow()

        self._list.blockSignals(True)
        self._list.clear()
        for sweep in self._sweeps:
            status = self._session.latest_status(sweep.name)
            item = QListWidgetItem(_item_text(sweep))
            item.setData(Qt.ItemDataRole.UserRole, sweep.name)
            _apply_status_color(item, status)
            self._list.addItem(item)
        self._list.blockSignals(False)

        # Restore or advance selection to first pending
        if 0 <= current_row < self._list.count():
            self._list.setCurrentRow(current_row)
        else:
            self._select_first_pending()

    def _select_first_pending(self) -> None:
        done = self._session.done_names()
        for i, sweep in enumerate(self._sweeps):
            if sweep.name not in done:
                self._list.setCurrentRow(i)
                return

    def _on_row_changed(self, row: int) -> None:
        if row < 0 or row >= len(self._sweeps):
            self._detail.clear()
            return
        sweep = self._sweeps[row]
        already_done = self._session.latest_status(sweep.name) == "done"
        self._detail.load_sweep(
            sweep,
            index_in_phase=row + 1,
            total_in_phase=len(self._sweeps),
            already_done=already_done,
        )

    # ------------------------------------------------------------------
    # Outcome handlers (connected to SweepDetailPanel signals)
    # ------------------------------------------------------------------

    def _on_accepted(self, name: str, duration_s: float) -> None:
        self._session.mark_done(self._phase, name, duration_s=duration_s)
        # Advance to next row
        row = self._list.currentRow()
        next_row = row + 1
        if next_row < self._list.count():
            self._list.setCurrentRow(next_row)

    def _on_skipped(self, name: str) -> None:
        self._session.mark_skipped(self._phase, name)
        row = self._list.currentRow()
        next_row = row + 1
        if next_row < self._list.count():
            self._list.setCurrentRow(next_row)

    # ------------------------------------------------------------------
    # Public: count of done measurements for badge
    # ------------------------------------------------------------------

    def done_count(self) -> int:
        done = self._session.done_names()
        return sum(1 for s in self._sweeps if s.name in done)

    def total_count(self) -> int:
        return len(self._sweeps)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _item_text(sweep: AcousticSweep) -> str:
    return f"{sweep.driver_tag}  {sweep.angle_desc}"


def _apply_status_color(item: QListWidgetItem, status: Optional[str]) -> None:
    if status == "done":
        item.setForeground(Qt.GlobalColor.white)
        item.setBackground(Qt.GlobalColor.transparent)
        item.setText("✓  " + item.text())
        item.setForeground(__color(theme.STATUS_DONE))
    elif status == "skipped":
        item.setForeground(__color(theme.STATUS_SKIPPED))
        item.setText("—  " + item.text())
    elif status == "failed":
        item.setForeground(__color(theme.STATUS_ERROR))
        item.setText("✕  " + item.text())
    else:
        item.setForeground(__color(theme.STATUS_PENDING))


def __color(hex_str: str):
    from PyQt6.QtGui import QColor
    return QColor(hex_str)
