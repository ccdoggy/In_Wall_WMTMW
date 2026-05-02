"""QTabWidget containing all 7 measurement phase tabs."""
from __future__ import annotations

from pathlib import Path

from PyQt6.QtWidgets import QTabWidget, QWidget

from .session_state import SessionState
from .dats_tab import DatsTab
from .manual_tab import ManualTab, CALIBRATION_STEPS, TIMING_REF_STEPS
from .sweep_tab import SweepTab

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from rew_api import RewApi


class PhaseTabs(QTabWidget):
    """The central tab widget. Creates one tab per measurement phase."""

    def __init__(
        self,
        session: SessionState,
        api: RewApi,
        export_dir: Path,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._session = session

        # Create all tabs
        self._dats = DatsTab(session)
        self._cal  = ManualTab("calibration", CALIBRATION_STEPS,
                               "2.83 V Calibration steps", session)
        self._ref  = ManualTab("timing_ref",  TIMING_REF_STEPS,
                               "Timing reference verification steps", session)
        self._h_polar    = SweepTab("h_polar",    session, api, export_dir)
        self._v_polar    = SweepTab("v_polar",    session, api, export_dir)
        self._nearfield  = SweepTab("nearfield",  session, api, export_dir)
        self._distortion = SweepTab("distortion", session, api, export_dir)

        self.addTab(self._dats,      "DATS")
        self.addTab(self._cal,       "Calibration")
        self.addTab(self._ref,       "Timing Ref")
        self.addTab(self._h_polar,   "H-Polar")
        self.addTab(self._v_polar,   "V-Polar")
        self.addTab(self._nearfield, "Nearfield")
        self.addTab(self._distortion,"Distortion")

        self._update_badges()
        session.progress_changed.connect(self._update_badges)

    # ------------------------------------------------------------------
    # Badge updates
    # ------------------------------------------------------------------

    def _update_badges(self) -> None:
        badges = [
            (self._dats,      "DATS"),
            (self._cal,       "Calibration"),
            (self._ref,       "Timing Ref"),
            (self._h_polar,   "H-Polar"),
            (self._v_polar,   "V-Polar"),
            (self._nearfield, "Nearfield"),
            (self._distortion,"Distortion"),
        ]
        for i, (tab, label) in enumerate(badges):
            if hasattr(tab, "done_count") and hasattr(tab, "total_count"):
                done  = tab.done_count()
                total = tab.total_count()
                self.setTabText(i, f"{label}  {done}/{total}")
            else:
                self.setTabText(i, label)

    # ------------------------------------------------------------------
    # Grand total for the toolbar
    # ------------------------------------------------------------------

    def grand_total_done(self) -> int:
        tabs = [
            self._dats, self._cal, self._ref,
            self._h_polar, self._v_polar, self._nearfield, self._distortion,
        ]
        return sum(
            t.done_count() for t in tabs if hasattr(t, "done_count")
        )

    def grand_total(self) -> int:
        tabs = [
            self._dats, self._cal, self._ref,
            self._h_polar, self._v_polar, self._nearfield, self._distortion,
        ]
        return sum(
            t.total_count() for t in tabs if hasattr(t, "total_count")
        )
