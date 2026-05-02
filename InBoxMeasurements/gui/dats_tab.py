"""Guided DATS impedance tab (7 manual sweeps, no API)."""
from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from measurement_matrix import DATS_SWEEPS, DatsSweep

from .session_state import SessionState
from . import theme


class DatsTab(QWidget):
    """Tab for Phase 1: DATS V3 impedance sweeps."""

    PHASE = "dats"

    def __init__(self, session: SessionState, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._session = session
        self._sweeps = list(DATS_SWEEPS)
        self._current_idx: int = -1
        self._build_ui()
        self._refresh()
        session.progress_changed.connect(self._refresh)

    def done_count(self) -> int:
        done = self._session.done_names()
        return sum(1 for s in self._sweeps if s.name in done)

    def total_count(self) -> int:
        return len(self._sweeps)

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left: sweep list
        left = QWidget()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(8, 8, 4, 8)
        ll.setSpacing(6)

        hdr = QLabel("DATS V3 impedance sweeps (7 total)")
        hdr.setObjectName("section_label")
        ll.addWidget(hdr)

        self._item_btns: list[QPushButton] = []
        for i, sweep in enumerate(self._sweeps):
            btn = QPushButton(_sweep_btn_label(sweep))
            btn.setCheckable(True)
            btn.setProperty("sweep_idx", i)
            btn.clicked.connect(lambda checked, idx=i: self._select(idx))
            btn.setStyleSheet(_item_btn_style("pending"))
            self._item_btns.append(btn)
            ll.addWidget(btn)

        ll.addStretch()
        splitter.addWidget(left)

        # Right: detail panel
        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setFrameShape(QFrame.Shape.NoFrame)

        self._right = QWidget()
        rl = QVBoxLayout(self._right)
        rl.setContentsMargins(16, 16, 16, 16)
        rl.setSpacing(10)

        self._detail_header = QLabel("")
        self._detail_header.setObjectName("phase_header")
        self._detail_header.setWordWrap(True)
        rl.addWidget(self._detail_header)

        self._detail_counter = QLabel("")
        self._detail_counter.setObjectName("sweep_counter")
        rl.addWidget(self._detail_counter)

        line = QFrame()
        line.setObjectName("separator")
        rl.addWidget(line)

        action_lbl = QLabel("Action")
        action_lbl.setObjectName("section_label")
        rl.addWidget(action_lbl)

        self._detail_action = QLabel("")
        self._detail_action.setWordWrap(True)
        self._detail_action.setStyleSheet(
            "color: #cdd6f4; font-size: 10pt; padding: 4px 0; line-height: 1.6;"
        )
        rl.addWidget(self._detail_action)

        self._detail_expect = QLabel("")
        self._detail_expect.setStyleSheet("color: #7f849c; font-size: 9pt;")
        self._detail_expect.setWordWrap(True)
        rl.addWidget(self._detail_expect)

        rl.addSpacing(12)

        # Mark Done / Skip / Redo buttons
        btn_row = QHBoxLayout()
        self._done_btn = QPushButton("Mark Done")
        self._done_btn.setObjectName("accept_btn")
        self._done_btn.clicked.connect(self._on_done)

        self._skip_btn = QPushButton("Skip")
        self._skip_btn.clicked.connect(self._on_skip)

        self._redo_btn = QPushButton("Redo")
        self._redo_btn.setObjectName("redo_btn")
        self._redo_btn.clicked.connect(self._on_redo)

        btn_row.addWidget(self._done_btn)
        btn_row.addWidget(self._skip_btn)
        btn_row.addWidget(self._redo_btn)
        btn_row.addStretch()
        rl.addLayout(btn_row)

        rl.addStretch()

        self._placeholder = QLabel("Select a DATS sweep from the list.")
        self._placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._placeholder.setStyleSheet("color: #585b70; font-size: 11pt;")
        rl.addWidget(self._placeholder)

        right_scroll.setWidget(self._right)
        splitter.addWidget(right_scroll)

        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 5)
        splitter.setSizes([240, 600])
        outer.addWidget(splitter)

        self._show_detail(False)

    # ------------------------------------------------------------------
    # Selection
    # ------------------------------------------------------------------

    def _select(self, idx: int) -> None:
        self._current_idx = idx
        for i, btn in enumerate(self._item_btns):
            btn.setChecked(i == idx)

        sweep = self._sweeps[idx]
        self._detail_header.setText(f"{sweep.label}")
        self._detail_counter.setText(f"Sweep {idx + 1} of {len(self._sweeps)}")
        self._detail_action.setText(sweep.action)

        expect_parts = []
        if sweep.expected_fc_hz is not None:
            part = f"Expected: Fc ≈ {sweep.expected_fc_hz:.1f} Hz"
            if sweep.expected_qtc is not None:
                part += f",  Qtc ≈ {sweep.expected_qtc:.2f}"
            expect_parts.append(part)
        if sweep.expected_fs_hz is not None:
            expect_parts.append(f"Expected: Fs ≈ {sweep.expected_fs_hz:.0f} Hz")
        self._detail_expect.setText("  ".join(expect_parts))

        status = self._session.latest_status(sweep.name)
        already_done = status == "done"
        self._done_btn.setEnabled(not already_done)
        self._skip_btn.setEnabled(not already_done)
        self._redo_btn.setVisible(already_done)

        self._show_detail(True)

    def _show_detail(self, visible: bool) -> None:
        for w in [
            self._detail_header, self._detail_counter, self._detail_action,
            self._detail_expect, self._done_btn, self._skip_btn, self._redo_btn,
        ]:
            w.setVisible(visible)
        self._placeholder.setVisible(not visible)

    # ------------------------------------------------------------------
    # Outcomes
    # ------------------------------------------------------------------

    def _on_done(self) -> None:
        if self._current_idx < 0:
            return
        sweep = self._sweeps[self._current_idx]
        self._session.mark_done(self.PHASE, sweep.name)
        # Advance
        next_idx = self._current_idx + 1
        if next_idx < len(self._sweeps):
            self._select(next_idx)

    def _on_skip(self) -> None:
        if self._current_idx < 0:
            return
        sweep = self._sweeps[self._current_idx]
        self._session.mark_skipped(self.PHASE, sweep.name)
        next_idx = self._current_idx + 1
        if next_idx < len(self._sweeps):
            self._select(next_idx)

    def _on_redo(self) -> None:
        if self._current_idx < 0:
            return
        sweep = self._sweeps[self._current_idx]
        # Reset to pending by recording a redo-request (won't count as done)
        self._session._log.record(self.PHASE, sweep.name, "redo-requested")
        self._session.progress_changed.emit()
        self._done_btn.setEnabled(True)
        self._skip_btn.setEnabled(True)
        self._redo_btn.setVisible(False)

    # ------------------------------------------------------------------
    # Refresh list button styles from session state
    # ------------------------------------------------------------------

    def _refresh(self) -> None:
        for i, (btn, sweep) in enumerate(zip(self._item_btns, self._sweeps)):
            status = self._session.latest_status(sweep.name) or "pending"
            btn.setStyleSheet(_item_btn_style(status))
            btn.setText(_sweep_btn_label(sweep, status))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sweep_btn_label(sweep: DatsSweep, status: str = "pending") -> str:
    icon = {"done": "✓  ", "skipped": "—  ", "failed": "✕  "}.get(status, "   ")
    return icon + sweep.label


def _item_btn_style(status: str) -> str:
    colors = {
        "done":    f"color: {theme.STATUS_DONE}; border-color: {theme.STATUS_DONE};",
        "skipped": f"color: {theme.STATUS_SKIPPED}; border-color: {theme.STATUS_SKIPPED};",
        "failed":  f"color: {theme.STATUS_ERROR}; border-color: {theme.STATUS_ERROR};",
        "pending": f"color: {theme.STATUS_PENDING};",
    }
    base = (
        "QPushButton { text-align: left; padding: 6px 10px; border-radius: 4px;"
        " background: #252535; border: 1px solid #44445a; "
    )
    return base + colors.get(status, colors["pending"]) + "}"
