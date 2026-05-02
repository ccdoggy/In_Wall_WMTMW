"""Session state: wraps ProgressLog and emits Qt signals on changes."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from PyQt6.QtCore import QObject, pyqtSignal

# Import from the parent package (InBoxMeasurements/)
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from prompts import ProgressLog


class SessionState(QObject):
    """Central state object for the GUI session.

    Wraps ProgressLog for CSV persistence and emits progress_changed
    whenever a measurement is recorded, so all widgets can update.
    """

    progress_changed = pyqtSignal()

    def __init__(self, log_path: Path, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.log_path = log_path
        self._log = ProgressLog(log_path)

    # ------------------------------------------------------------------
    # Mutations — call these to record measurement outcomes
    # ------------------------------------------------------------------

    def mark_done(
        self,
        phase: str,
        name: str,
        duration_s: Optional[float] = None,
        notes: str = "",
    ) -> None:
        self._log.record(phase, name, "done", duration_s=duration_s, notes=notes)
        self.progress_changed.emit()

    def mark_skipped(self, phase: str, name: str) -> None:
        self._log.record(phase, name, "skipped")
        self.progress_changed.emit()

    def mark_failed(self, phase: str, name: str, notes: str = "") -> None:
        self._log.record(phase, name, "failed", notes=notes)
        self.progress_changed.emit()

    def bulk_mark_done(self, items: list[tuple[str, str]], notes: str = "") -> int:
        """Mark multiple (phase, name) pairs as done in one shot.

        Emits progress_changed once at the end (not once per item).
        Returns the number of items written.
        """
        for phase, name in items:
            self._log.record(phase, name, "done", notes=notes)
        if items:
            self.progress_changed.emit()
        return len(items)

    # ------------------------------------------------------------------
    # Queries — delegate to ProgressLog
    # ------------------------------------------------------------------

    def done_names(self) -> set[str]:
        return self._log.done_names()

    def latest_status(self, name: str) -> Optional[str]:
        return self._log._latest_status_by_name().get(name)

    def counts(self) -> dict[str, int]:
        return self._log.counts_by_status()

    def total_done(self) -> int:
        latest = self._log._latest_status_by_name()
        return sum(1 for s in latest.values() if s == "done")
