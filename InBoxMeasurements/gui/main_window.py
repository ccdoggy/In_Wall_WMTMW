"""Main application window."""
from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import QObject, Qt, QThread, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QLabel,
    QMainWindow,
    QPushButton,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from rew_api import RewApi

from .session_state import SessionState
from .phase_tabs import PhaseTabs
from .file_scanner import scan
from .scan_dialog import ScanDialog


class _ProbeWorker(QObject):
    """Runs RewApi.probe() on a background thread; never blocks the main thread."""
    finished = pyqtSignal(object)  # ProbeResult

    def __init__(self, api: RewApi) -> None:
        super().__init__()
        self._api = api

    def run(self) -> None:
        self.finished.emit(self._api.probe())


class MainWindow(QMainWindow):
    def __init__(
        self,
        session: SessionState,
        api: RewApi,
        export_dir: Path,
    ) -> None:
        super().__init__()
        self._session = session
        self._api = api
        self._export_dir = export_dir

        self.setWindowTitle("WMTMW Measurement Wizard")
        self.resize(1100, 720)
        self.setMinimumSize(800, 560)

        self._probe_thread: QThread | None = None
        self._probe_worker: _ProbeWorker | None = None  # keeps worker alive until thread finishes

        self._build_ui()
        self._probe_rew()  # initial probe (non-blocking; spins up a thread)

        # Re-probe REW every 15 s so the status indicator stays current
        self._rew_timer = QTimer(self)
        self._rew_timer.timeout.connect(self._probe_rew)
        self._rew_timer.start(15_000)

        session.progress_changed.connect(self._update_progress_label)

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Toolbar row
        toolbar_widget = QWidget()
        toolbar_widget.setFixedHeight(42)
        toolbar_widget.setStyleSheet(
            "background: #181825; border-bottom: 1px solid #44445a;"
        )
        toolbar_layout = _hbox(toolbar_widget)

        title = QLabel("WMTMW Measurement Wizard")
        title.setStyleSheet("color: #cdd6f4; font-size: 11pt; font-weight: bold; padding-left: 12px;")
        toolbar_layout.addWidget(title)
        toolbar_layout.addStretch()

        self._progress_label = QLabel("")
        self._progress_label.setStyleSheet("color: #7f849c; padding-right: 16px;")
        toolbar_layout.addWidget(self._progress_label)

        scan_btn = QPushButton("⟳  Scan Files")
        scan_btn.setToolTip(
            "Scan dats/ and rew/ for existing measurement files\n"
            "and offer to mark matching measurements as done."
        )
        scan_btn.setStyleSheet(
            "QPushButton { background: #252535; color: #89b4fa; border: 1px solid #44445a;"
            " border-radius: 4px; padding: 4px 12px; margin-right: 8px; }"
            "QPushButton:hover { background: #313145; border-color: #89b4fa; }"
        )
        scan_btn.setFixedHeight(28)
        scan_btn.clicked.connect(self._on_scan_files)
        toolbar_layout.addWidget(scan_btn)

        self._rew_indicator = QLabel("● REW: checking…")
        self._rew_indicator.setStyleSheet("color: #7f849c; padding-right: 16px;")
        toolbar_layout.addWidget(self._rew_indicator)

        layout.addWidget(toolbar_widget)

        # Phase tabs
        self._tabs = PhaseTabs(self._session, self._api, self._export_dir)
        layout.addWidget(self._tabs)

        # Status bar
        status = QStatusBar()
        status.setStyleSheet("background: #181825; color: #7f849c;")
        self.setStatusBar(status)

        self._status_session = QLabel(f"Session: {self._session.log_path.name}")
        self._status_rew = QLabel("REW: checking…")
        self._status_phase = QLabel("")

        status.addWidget(self._status_session)
        status.addWidget(_separator())
        status.addWidget(self._status_rew)
        status.addWidget(_separator())
        status.addPermanentWidget(self._status_phase)

        self._update_progress_label()

    # ------------------------------------------------------------------
    # REW probe (non-blocking)
    # ------------------------------------------------------------------

    def _probe_rew(self) -> None:
        """Kick off a background probe. Skips silently if one is already in flight."""
        if self._probe_thread is not None and self._probe_thread.isRunning():
            return

        # No parent on QThread — we own lifetime via self._probe_thread.
        # self._probe_worker must be stored as an instance attribute; if it
        # were a local variable Python's GC could collect it before the thread
        # calls run(), silently dropping the probe.
        self._probe_thread = QThread()
        self._probe_worker = _ProbeWorker(self._api)
        self._probe_worker.moveToThread(self._probe_thread)

        self._probe_thread.started.connect(self._probe_worker.run)
        self._probe_worker.finished.connect(self._on_probe_finished)
        self._probe_worker.finished.connect(self._probe_thread.quit)

        self._probe_thread.start()

    def _on_probe_finished(self, result: object) -> None:
        if result.reachable:
            ver = result.version or "connected"
            self._rew_indicator.setText(f"● REW: {ver}")
            self._rew_indicator.setStyleSheet(
                "color: #a6e3a1; padding-right: 16px; font-weight: bold;"
            )
            self._status_rew.setText(f"REW: Connected ({ver})")
        else:
            self._rew_indicator.setText("● REW: offline")
            self._rew_indicator.setStyleSheet("color: #f38ba8; padding-right: 16px;")
            self._status_rew.setText("REW: Not connected — manual mode")

    # ------------------------------------------------------------------
    # Scan Files
    # ------------------------------------------------------------------

    def _on_scan_files(self) -> None:
        script_dir = self._session.log_path.parent
        dats_dir   = script_dir / "dats"
        frd_dir    = self._export_dir          # e.g. InBoxMeasurements/rew/

        already_done = self._session.done_names()
        results = scan(dats_dir, frd_dir, already_done)

        dlg = ScanDialog(results, parent=self)
        if dlg.exec() != ScanDialog.DialogCode.Accepted:
            return

        selected = dlg.selected_results()
        if not selected:
            return

        items = [(r.phase, r.name) for r in selected]
        n = self._session.bulk_mark_done(items, notes="file-scan")

        self._status_session.setText(
            f"Session: {self._session.log_path.name}  (+{n} from file scan)"
        )

    # ------------------------------------------------------------------
    # Progress label
    # ------------------------------------------------------------------

    def _update_progress_label(self) -> None:
        done  = self._tabs.grand_total_done()
        total = self._tabs.grand_total()
        self._progress_label.setText(f"{done} / {total} done")


# ---------------------------------------------------------------------------
# Layout helpers
# ---------------------------------------------------------------------------

def _hbox(parent: QWidget):
    from PyQt6.QtWidgets import QHBoxLayout
    layout = QHBoxLayout(parent)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    return layout


def _separator() -> QWidget:
    sep = QWidget()
    sep.setFixedWidth(1)
    sep.setFixedHeight(14)
    sep.setStyleSheet("background: #44445a;")
    sep.setContentsMargins(8, 0, 8, 0)
    w = QWidget()
    h = _hbox(w)
    h.addSpacing(8)
    h.addWidget(sep)
    h.addSpacing(8)
    return w
