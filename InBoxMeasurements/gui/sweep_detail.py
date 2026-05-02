"""Right-panel detail view for a single acoustic sweep.

Shows:
  - Driver name + angle (phase header)
  - Sweep counter (e.g. "Sweep 23 of 60")
  - Setup instructions
  - Frequency / level / sweep-length summary
  - MEASURE / SKIP / CANCEL buttons
  - ValidationPanel (hidden until after a sweep)
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import Optional

from PyQt6.QtCore import QObject, Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from measurement_matrix import AcousticSweep
from rew_api import MeasureResult, RewApi

from .safety_dialog import SafetyDialog
from .validation_panel import ValidationPanel


# ---------------------------------------------------------------------------
# Background worker for REW measurement
# ---------------------------------------------------------------------------

class _MeasureWorker(QObject):
    finished = pyqtSignal(object)   # MeasureResult

    def __init__(self, api: RewApi, sweep: AcousticSweep) -> None:
        super().__init__()
        self._api = api
        self._sweep = sweep

    def run(self) -> None:
        result = self._api.measure(self._sweep)
        self.finished.emit(result)


# ---------------------------------------------------------------------------
# Detail panel
# ---------------------------------------------------------------------------

class SweepDetailPanel(QWidget):
    """Right-hand panel showing current measurement detail and controls."""

    measure_accepted = pyqtSignal(str, float)   # (name, duration_s)
    measure_skipped  = pyqtSignal(str)          # name
    cancelled        = pyqtSignal()

    def __init__(
        self,
        api: RewApi,
        export_dir: Path,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._api = api
        self._export_dir = export_dir
        self._current_sweep: Optional[AcousticSweep] = None
        self._measure_start: float = 0.0
        self._thread: Optional[QThread] = None
        self._worker: Optional[_MeasureWorker] = None
        self._last_result: Optional[MeasureResult] = None
        self._build_ui()

    def _build_ui(self) -> None:
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        scroll.setWidget(content)

        root_outer = QVBoxLayout(self)
        root_outer.setContentsMargins(0, 0, 0, 0)
        root_outer.addWidget(scroll)

        root = QVBoxLayout(content)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(10)

        # Phase / driver header
        self._header = QLabel("")
        self._header.setObjectName("phase_header")
        self._header.setWordWrap(True)
        root.addWidget(self._header)

        # Sweep counter
        self._counter = QLabel("")
        self._counter.setObjectName("sweep_counter")
        root.addWidget(self._counter)

        # Separator
        line = QFrame()
        line.setObjectName("separator")
        root.addWidget(line)

        # Setup instructions label
        setup_lbl = QLabel("Setup")
        setup_lbl.setObjectName("section_label")
        root.addWidget(setup_lbl)

        self._instructions = QLabel("")
        self._instructions.setWordWrap(True)
        self._instructions.setStyleSheet(
            "color: #cdd6f4; font-size: 10pt; padding: 4px 0; line-height: 1.6;"
        )
        root.addWidget(self._instructions)

        # Sweep parameters summary
        self._params_label = QLabel("")
        self._params_label.setStyleSheet(
            "color: #7f849c; font-size: 9pt; font-family: 'Consolas', monospace;"
        )
        root.addWidget(self._params_label)

        root.addSpacing(8)

        # MEASURE button
        self._measure_btn = QPushButton("MEASURE")
        self._measure_btn.setObjectName("measure_btn")
        self._measure_btn.clicked.connect(self._on_measure)
        root.addWidget(self._measure_btn)

        # Status label (shown during sweep)
        self._status_label = QLabel("")
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status_label.setStyleSheet("color: #89b4fa; font-style: italic;")
        self._status_label.hide()
        root.addWidget(self._status_label)

        # Skip / Cancel row
        btn_row = QHBoxLayout()
        self._skip_btn = QPushButton("Skip")
        self._skip_btn.clicked.connect(self._on_skip)
        self._cancel_btn = QPushButton("Cancel")
        self._cancel_btn.clicked.connect(self.cancelled.emit)
        btn_row.addWidget(self._skip_btn)
        btn_row.addWidget(self._cancel_btn)
        btn_row.addStretch()
        root.addLayout(btn_row)

        root.addSpacing(4)

        # Validation panel (hidden until sweep done)
        self._validation = ValidationPanel()
        self._validation.accepted.connect(self._on_accepted)
        self._validation.redo_requested.connect(self._on_redo)
        root.addWidget(self._validation)

        root.addStretch()

        # Placeholder shown when no sweep is selected
        self._placeholder = QLabel("Select a measurement from the list.")
        self._placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._placeholder.setStyleSheet("color: #585b70; font-size: 11pt;")
        self._placeholder.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        root_outer.addWidget(self._placeholder)

        self._show_placeholder(True)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load_sweep(
        self,
        sweep: AcousticSweep,
        index_in_phase: int,
        total_in_phase: int,
        already_done: bool,
    ) -> None:
        self._current_sweep = sweep
        self._last_result = None
        self._validation.hide_results()
        self._status_label.hide()
        self._show_placeholder(False)

        self._header.setText(f"{sweep.driver_tag}-{sweep.driver_name}  —  {sweep.angle_desc}")
        self._counter.setText(f"Sweep {index_in_phase} of {total_in_phase}")
        self._instructions.setText(_format_instructions(sweep))
        self._params_label.setText(
            f"{sweep.start_freq_hz:,} Hz – {sweep.end_freq_hz:,} Hz  "
            f"•  {sweep.sweep_length // 1024} k  "
            f"•  {sweep.level_dbfs:+.0f} dBFS"
        )

        enabled = not already_done
        self._measure_btn.setEnabled(enabled)
        self._skip_btn.setEnabled(enabled)
        if already_done:
            self._measure_btn.setText("REDO")
            self._measure_btn.setEnabled(True)

    def clear(self) -> None:
        self._current_sweep = None
        self._show_placeholder(True)

    # ------------------------------------------------------------------
    # Slot handlers
    # ------------------------------------------------------------------

    def _on_measure(self) -> None:
        sweep = self._current_sweep
        if sweep is None:
            return

        # Safety confirmation if required
        if sweep.require_confirm:
            dlg = SafetyDialog(
                title="Setup Confirmation Required",
                instruction=sweep.require_confirm,
                parent=self,
            )
            if dlg.exec() != SafetyDialog.DialogCode.Accepted:
                return

        # Safety note (tweeter etc.) as a separate dialog
        if sweep.safety_note:
            dlg = SafetyDialog(
                title="Safety Check",
                instruction=sweep.safety_note,
                parent=self,
            )
            if dlg.exec() != SafetyDialog.DialogCode.Accepted:
                return

        self._start_measurement(sweep)

    def _start_measurement(self, sweep: AcousticSweep) -> None:
        self._measure_btn.setEnabled(False)
        self._skip_btn.setEnabled(False)
        self._cancel_btn.setEnabled(False)
        self._status_label.setText("Measuring…  (REW sweep in progress)")
        self._status_label.show()
        self._validation.hide_results()
        self._measure_start = time.monotonic()

        self._thread = QThread()
        self._worker = _MeasureWorker(self._api, sweep)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_measure_finished)
        self._worker.finished.connect(self._thread.quit)
        self._thread.start()

    def _on_measure_finished(self, result: MeasureResult) -> None:
        self._last_result = result
        self._status_label.hide()
        self._cancel_btn.setEnabled(True)

        if not result.ok:
            self._status_label.setText(
                f"REW API failed ({result.error}). Mark done manually:"
            )
            self._status_label.show()
            self._measure_btn.setEnabled(True)
            self._skip_btn.setEnabled(True)
            # Still show validation panel so user can Accept manually
            self._validation.show_results(
                overload=False,
                frd_path=None,
                sweep_name=self._current_sweep.name if self._current_sweep else "",
                driver_name=self._current_sweep.driver_tag if self._current_sweep else "",
            )
            return

        # Try per-measurement FRD export
        frd_path = None
        if result.measurement_id is not None or True:
            exp = self._api.export_latest(
                self._export_dir / "frd",
                measurement_id=result.measurement_id,
            )
            if exp.ok and exp.frd_path:
                frd_path = exp.frd_path

        sweep = self._current_sweep
        self._validation.show_results(
            overload=result.overload,
            frd_path=frd_path,
            sweep_name=sweep.name if sweep else "",
            driver_name=sweep.driver_tag if sweep else "",
        )

    def _on_accepted(self) -> None:
        if self._current_sweep is None:
            return
        duration = (
            self._last_result.duration_s
            if self._last_result and self._last_result.duration_s is not None
            else 0.0
        )
        self.measure_accepted.emit(self._current_sweep.name, duration)
        self._validation.hide_results()
        self._measure_btn.setText("MEASURE")
        self._measure_btn.setEnabled(False)  # list will reload next sweep

    def _on_redo(self) -> None:
        self._validation.hide_results()
        self._measure_btn.setEnabled(True)
        self._skip_btn.setEnabled(True)
        self._measure_btn.setText("MEASURE")

    def _on_skip(self) -> None:
        if self._current_sweep is None:
            return
        self.measure_skipped.emit(self._current_sweep.name)
        self._validation.hide_results()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _show_placeholder(self, show: bool) -> None:
        # The scroll area holds all content widgets; placeholder is stacked below
        widgets = [
            self._header, self._counter, self._instructions,
            self._params_label, self._measure_btn, self._skip_btn,
            self._cancel_btn, self._validation, self._status_label,
        ]
        for w in widgets:
            w.setVisible(not show)
        self._placeholder.setVisible(show)


# ---------------------------------------------------------------------------
# Helper: format setup instructions from an AcousticSweep
# ---------------------------------------------------------------------------

def _format_instructions(sweep: AcousticSweep) -> str:
    lines = []
    # Action text from matrix (first sentence/phrase)
    if sweep.action:
        lines.append(f"1.  {sweep.action}")
    # Derive mic position from angle description
    if "deg" in sweep.angle_desc.lower() or "°" in sweep.angle_desc:
        lines.append(f"2.  Position mic at {sweep.angle_desc}, 1 m distance from baffle.")
    else:
        lines.append(f"2.  {sweep.angle_desc}")
    lines.append("3.  Ensure room is quiet; HVAC/fan off if possible.")
    if sweep.require_confirm:
        lines.append(f"\n⚠  {sweep.require_confirm}")
    return "\n".join(lines)
