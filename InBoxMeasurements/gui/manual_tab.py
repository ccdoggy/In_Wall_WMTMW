"""Reusable step-through guide tab for Calibration and Timing-ref phases.

Each phase is a fixed ordered list of steps. The user works through them
one at a time and marks each done or skipped.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from .session_state import SessionState
from .safety_dialog import SafetyDialog


@dataclass
class Step:
    key: str          # used as name in progress log
    title: str        # short label for the step button
    body: str         # full instruction text
    safety: str = "" # if non-empty, show a SafetyDialog before marking done


# ---------------------------------------------------------------------------
# Calibration steps
# ---------------------------------------------------------------------------

CALIBRATION_STEPS: list[Step] = [
    Step(
        key="cal-tweeter-disconnect",
        title="1. Disconnect tweeter",
        body=(
            "PHYSICALLY DISCONNECT the tweeter wires at the wall terminals before proceeding.\n\n"
            "This step is non-negotiable: driving any woofer below the tweeter's Fs with "
            "the tweeter connected risks exceeding its Xmax."
        ),
        safety=(
            "Tweeter wires must be PHYSICALLY DISCONNECTED at the wall terminals "
            "before any 2.83 V calibration tone is applied."
        ),
    ),
    Step(
        key="cal-connect-w1",
        title="2. Connect W1 to Arcam Front-Right",
        body=(
            "Connect the upper woofer (W1) cable to the Arcam Front-Right speaker output.\n\n"
            "This is the reference load for the 2.83 V calibration."
        ),
    ),
    Step(
        key="cal-set-arcam-volume",
        title="3. Set Arcam reference volume",
        body=(
            "Set the Arcam volume to a fixed reference (e.g. −20 dB).\n\n"
            "Write this down. Do NOT change the Arcam volume again after this point — "
            "all acoustic sweeps depend on this reference level."
        ),
    ),
    Step(
        key="cal-dmm-2v83",
        title="4. DMM: measure 2.83 V",
        body=(
            "Put DMM probes on the W1 wall terminals, set to AC Volts, 20 V range.\n\n"
            "In REW: Generator tab → select 60 Hz sine → start at −20 dBFS.\n"
            "Play the tone and raise the REW generator level until the DMM reads 2.83 V AC (±0.05 V).\n\n"
            "Record the REW generator dBFS value — this is the calibrated −12 dBFS anchor.\n"
            "Stop the tone when done."
        ),
    ),
    Step(
        key="cal-done",
        title="5. Confirm calibration",
        body=(
            "Verify:\n"
            "  • DMM read 2.83 V at the recorded generator level.\n"
            "  • Arcam volume is locked at the reference setting.\n"
            "  • Tweeter is still disconnected.\n\n"
            "The tweeter will remain disconnected until the polar sweep phase begins."
        ),
    ),
]

# ---------------------------------------------------------------------------
# Timing-ref steps
# ---------------------------------------------------------------------------

TIMING_REF_STEPS: list[Step] = [
    Step(
        key="ref-signal-chain",
        title="1. Verify signal chain",
        body=(
            "Confirm the measurement rig signal chain:\n\n"
            "  Laptop 3.5 mm → splitter → Arcam 7.1 multichannel input\n"
            "  Left channel  → Arcam Front-Left  → small desk speaker (timing ref)\n"
            "  Right channel → Arcam Front-Right → DUT (driver under test)\n"
            "  UMIK-1 USB    → Laptop (measurement mic)\n\n"
            "The desk speaker on Front-Left provides the Acoustic Timing Reference "
            "that lets REW produce phase-coherent FRD files across multiple drivers."
        ),
    ),
    Step(
        key="ref-rew-settings",
        title="2. Configure REW",
        body=(
            "In REW:\n"
            "  Preferences → Analysis → 'Use acoustic timing reference' = ON\n"
            "  Generator → Reference output = Left (the desk speaker on Arcam FL)\n\n"
            "Set the reference pilot tone to a modest level (audible at mic, not loud)."
        ),
    ),
    Step(
        key="ref-test-sweep",
        title="3. Run a test sweep",
        body=(
            "Run a short test sweep (any driver) and verify:\n"
            "  • REW shows a timing-reference peak in the impulse response.\n"
            "  • The peak is clearly identifiable and stable across repeated sweeps.\n\n"
            "If REW does NOT show a timing-reference peak, troubleshoot before proceeding:\n"
            "  - Desk speaker muted?\n"
            "  - Wrong Arcam input selected?\n"
            "  - Splitter polarity issue?\n"
            "  - REW reference channel set to Right instead of Left?\n"
            "  - Pilot level too low relative to room noise?"
        ),
    ),
    Step(
        key="ref-verified",
        title="4. Confirm reference locked",
        body=(
            "Confirm that REW's Acoustic Timing Reference is locked and stable.\n\n"
            "The reference peak should appear at the same time offset in every sweep. "
            "Mark this step done to confirm timing reference is verified and you are "
            "ready to begin polar sweeps."
        ),
    ),
]


# ---------------------------------------------------------------------------
# ManualTab widget
# ---------------------------------------------------------------------------

class ManualTab(QWidget):
    """Generic step-guide tab for Cal and Timing-ref."""

    def __init__(
        self,
        phase: str,
        steps: list[Step],
        title: str,
        session: SessionState,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._phase = phase
        self._steps = steps
        self._title = title
        self._session = session
        self._current_idx: int = -1
        self._build_ui()
        self._refresh()
        session.progress_changed.connect(self._refresh)

    def done_count(self) -> int:
        done = self._session.done_names()
        return sum(1 for s in self._steps if s.key in done)

    def total_count(self) -> int:
        return len(self._steps)

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        from PyQt6.QtWidgets import QSplitter
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left: step list
        left = QWidget()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(8, 8, 4, 8)
        ll.setSpacing(4)

        hdr = QLabel(self._title)
        hdr.setObjectName("section_label")
        ll.addWidget(hdr)

        self._step_btns: list[QPushButton] = []
        for i, step in enumerate(self._steps):
            btn = QPushButton(step.title)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, idx=i: self._select(idx))
            btn.setStyleSheet(_step_btn_style("pending"))
            self._step_btns.append(btn)
            ll.addWidget(btn)

        ll.addStretch()
        splitter.addWidget(left)

        # Right: instruction panel
        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setFrameShape(QFrame.Shape.NoFrame)

        self._right = QWidget()
        rl = QVBoxLayout(self._right)
        rl.setContentsMargins(16, 16, 16, 16)
        rl.setSpacing(10)

        self._step_header = QLabel("")
        self._step_header.setObjectName("phase_header")
        self._step_header.setWordWrap(True)
        rl.addWidget(self._step_header)

        line = QFrame()
        line.setObjectName("separator")
        rl.addWidget(line)

        self._step_body = QLabel("")
        self._step_body.setWordWrap(True)
        self._step_body.setStyleSheet(
            "color: #cdd6f4; font-size: 10pt; line-height: 1.8; padding: 4px 0;"
        )
        self._step_body.setTextFormat(Qt.TextFormat.PlainText)
        rl.addWidget(self._step_body)

        rl.addSpacing(12)

        btn_row = QHBoxLayout()
        self._done_btn = QPushButton("Mark Done")
        self._done_btn.setObjectName("accept_btn")
        self._done_btn.clicked.connect(self._on_done)

        self._skip_btn = QPushButton("Skip")
        self._skip_btn.clicked.connect(self._on_skip)

        btn_row.addWidget(self._done_btn)
        btn_row.addWidget(self._skip_btn)
        btn_row.addStretch()
        rl.addLayout(btn_row)

        rl.addStretch()

        self._placeholder = QLabel("Select a step from the list.")
        self._placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._placeholder.setStyleSheet("color: #585b70; font-size: 11pt;")
        rl.addWidget(self._placeholder)

        right_scroll.setWidget(self._right)
        splitter.addWidget(right_scroll)

        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 5)
        splitter.setSizes([220, 600])
        outer.addWidget(splitter)

        self._show_detail(False)

    def _select(self, idx: int) -> None:
        self._current_idx = idx
        for i, btn in enumerate(self._step_btns):
            btn.setChecked(i == idx)
        step = self._steps[idx]
        self._step_header.setText(step.title)
        self._step_body.setText(step.body)
        status = self._session.latest_status(step.key)
        self._done_btn.setEnabled(status != "done")
        self._skip_btn.setEnabled(status != "done")
        self._show_detail(True)

    def _show_detail(self, visible: bool) -> None:
        for w in [self._step_header, self._step_body, self._done_btn, self._skip_btn]:
            w.setVisible(visible)
        self._placeholder.setVisible(not visible)

    # ------------------------------------------------------------------
    # Outcomes
    # ------------------------------------------------------------------

    def _on_done(self) -> None:
        if self._current_idx < 0:
            return
        step = self._steps[self._current_idx]

        # Safety confirmation if required
        if step.safety:
            dlg = SafetyDialog(
                title="Safety Check",
                instruction=step.safety,
                parent=self,
            )
            if dlg.exec() != SafetyDialog.DialogCode.Accepted:
                return

        self._session.mark_done(self._phase, step.key)
        next_idx = self._current_idx + 1
        if next_idx < len(self._steps):
            self._select(next_idx)

    def _on_skip(self) -> None:
        if self._current_idx < 0:
            return
        step = self._steps[self._current_idx]
        self._session.mark_skipped(self._phase, step.key)
        next_idx = self._current_idx + 1
        if next_idx < len(self._steps):
            self._select(next_idx)

    def _refresh(self) -> None:
        for btn, step in zip(self._step_btns, self._steps):
            status = self._session.latest_status(step.key) or "pending"
            btn.setStyleSheet(_step_btn_style(status))
        # Re-render current step if visible (update button enable states)
        if self._current_idx >= 0:
            step = self._steps[self._current_idx]
            status = self._session.latest_status(step.key)
            self._done_btn.setEnabled(status != "done")
            self._skip_btn.setEnabled(status != "done")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _step_btn_style(status: str) -> str:
    from . import theme
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
