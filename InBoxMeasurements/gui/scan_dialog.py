"""Confirmation dialog for the file-scan auto-populate feature.

Shows a grouped, checkable list of measurements found on disk.
User can deselect individual items before committing.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from .file_scanner import ScanResult


# Phase display order and human-readable names
_PHASE_ORDER = ["dats", "h_polar", "v_polar", "nearfield", "distortion"]
_PHASE_LABELS = {
    "dats":       "DATS Impedance",
    "h_polar":    "Horizontal Polars",
    "v_polar":    "Vertical Polars",
    "nearfield":  "Nearfield",
    "distortion": "Distortion",
}


class ScanDialog(QDialog):
    """Shows scan results; returns the user-selected ScanResults on accept."""

    def __init__(
        self,
        results: list[ScanResult],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Auto-Populate from Files")
        self.setModal(True)
        self.setMinimumSize(560, 480)
        self._results = results
        self._checkboxes: list[tuple[QCheckBox, ScanResult]] = []
        self._build_ui()

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setSpacing(12)
        root.setContentsMargins(20, 16, 20, 16)

        # Header
        header = QLabel("Found measurements on disk")
        header.setStyleSheet("font-size: 12pt; font-weight: bold; color: #89b4fa;")
        root.addWidget(header)

        if not self._results:
            msg = QLabel(
                "No new measurements found on disk.\n\n"
                "Expected locations:\n"
                "  • DATS .zma files in  dats/\n"
                "  • Acoustic .frd files in  rew/  or  rew/frd/"
            )
            msg.setStyleSheet("color: #7f849c; font-size: 10pt;")
            msg.setWordWrap(True)
            root.addWidget(msg)
            btn = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
            btn.rejected.connect(self.reject)
            root.addWidget(btn)
            return

        count = len(self._results)
        sub = QLabel(
            f"{count} measurement{'s' if count != 1 else ''} found that "
            f"{'are' if count != 1 else 'is'} not yet marked done. "
            f"Check the ones you want to mark done now."
        )
        sub.setWordWrap(True)
        sub.setStyleSheet("color: #cdd6f4;")
        root.addWidget(sub)

        # Select All / None row
        ctrl_row = QHBoxLayout()
        select_all_btn = QPushButton("Select All")
        select_all_btn.setFixedWidth(100)
        select_all_btn.clicked.connect(self._select_all)
        select_none_btn = QPushButton("Select None")
        select_none_btn.setFixedWidth(100)
        select_none_btn.clicked.connect(self._select_none)
        ctrl_row.addWidget(select_all_btn)
        ctrl_row.addWidget(select_none_btn)
        ctrl_row.addStretch()
        root.addLayout(ctrl_row)

        # Scrollable checklist grouped by phase
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: #252535; border: 1px solid #44445a; border-radius: 4px;")

        list_widget = QWidget()
        list_widget.setStyleSheet("background: #252535;")
        list_layout = QVBoxLayout(list_widget)
        list_layout.setContentsMargins(8, 8, 8, 8)
        list_layout.setSpacing(2)

        # Group by phase in display order
        by_phase: dict[str, list[ScanResult]] = {}
        for r in self._results:
            by_phase.setdefault(r.phase, []).append(r)

        for phase in _PHASE_ORDER:
            items = by_phase.get(phase, [])
            if not items:
                continue

            # Phase group header
            phase_label = QLabel(_PHASE_LABELS.get(phase, phase))
            phase_label.setStyleSheet(
                "color: #89b4fa; font-size: 9pt; font-weight: bold; "
                "padding: 8px 4px 4px 4px; text-transform: uppercase;"
            )
            list_layout.addWidget(phase_label)

            for result in items:
                cb = QCheckBox(f"{result.name}")
                cb.setChecked(True)
                cb.setToolTip(str(result.found_path))
                cb.setStyleSheet("color: #cdd6f4; padding: 2px 8px;")
                list_layout.addWidget(cb)
                self._checkboxes.append((cb, result))

        list_layout.addStretch()
        scroll.setWidget(list_widget)
        root.addWidget(scroll)

        # Button row
        btn_box = QDialogButtonBox()
        self._mark_btn = QPushButton(f"Mark {count} Done")
        self._mark_btn.setObjectName("accept_btn")
        self._mark_btn.setDefault(True)
        btn_box.addButton(self._mark_btn, QDialogButtonBox.ButtonRole.AcceptRole)
        cancel_btn = btn_box.addButton(QDialogButtonBox.StandardButton.Cancel)

        self._mark_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        # Keep button label in sync with checkbox count
        for cb, _ in self._checkboxes:
            cb.toggled.connect(self._update_mark_btn)

        root.addWidget(btn_box)

    # ------------------------------------------------------------------
    # Result extraction
    # ------------------------------------------------------------------

    def selected_results(self) -> list[ScanResult]:
        """Return only the results whose checkbox is checked."""
        return [r for cb, r in self._checkboxes if cb.isChecked()]

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _select_all(self) -> None:
        for cb, _ in self._checkboxes:
            cb.setChecked(True)

    def _select_none(self) -> None:
        for cb, _ in self._checkboxes:
            cb.setChecked(False)

    def _update_mark_btn(self) -> None:
        n = sum(1 for cb, _ in self._checkboxes if cb.isChecked())
        self._mark_btn.setText(f"Mark {n} Done" if n else "Mark Done")
        self._mark_btn.setEnabled(n > 0)
