"""Post-sweep validation panel: badges + embedded matplotlib FRD chart."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import matplotlib
matplotlib.use("QtAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

# Expected passbands per driver type (for shape-sanity shading + check)
_PASSBANDS: dict[str, tuple[float, float]] = {
    "W": (80.0,   1_500.0),
    "M": (200.0,  6_000.0),
    "T": (800.0, 20_000.0),
}
_PASSBAND_SPL_FLOOR = 60.0   # dBSPL — below this in passband → shape warning
_SILENCE_THRESHOLD  = 50.0   # dBSPL — max SPL below this → "No signal"
_NOISE_VARIANCE_WARN = 10.0  # dB variance in out-of-band region → noise warning


# ---------------------------------------------------------------------------
# FRD parsing
# ---------------------------------------------------------------------------

def _parse_frd(path: Path) -> tuple[list[float], list[float]]:
    """Return (freqs_hz, spl_db). Skips comment/header lines."""
    freqs, spls = [], []
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(("#", "*", ";")):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            try:
                freqs.append(float(parts[0]))
                spls.append(float(parts[1]))
            except ValueError:
                continue
    return freqs, spls


def _driver_type(driver_name: str) -> str:
    """Return 'W', 'M', or 'T' from a name like 'W1-UpperWoofer'."""
    name_upper = driver_name.upper()
    if name_upper.startswith("W") or "WOOF" in name_upper:
        return "W"
    if name_upper.startswith("T") or "TWEET" in name_upper:
        return "T"
    return "M"


# ---------------------------------------------------------------------------
# Badge widget
# ---------------------------------------------------------------------------

_BADGE_STYLES = {
    "ok":   ("✓", "#a6e3a1", "#1e3a25"),
    "warn": ("⚠", "#f9e2af", "#3a2e1e"),
    "err":  ("✕", "#f38ba8", "#3a1e25"),
    "info": ("●", "#89b4fa", "#1e2a3a"),
}


class _Badge(QLabel):
    def __init__(self, kind: str, text: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        icon, fg, bg = _BADGE_STYLES.get(kind, _BADGE_STYLES["info"])
        self.setText(f"  {icon}  {text}  ")
        self.setStyleSheet(
            f"color: {fg}; background: {bg}; border-radius: 4px; "
            f"padding: 3px 6px; font-size: 9pt;"
        )
        self.setFixedHeight(24)


# ---------------------------------------------------------------------------
# Matplotlib chart
# ---------------------------------------------------------------------------

class _FrdChart(FigureCanvasQTAgg):
    def __init__(self, parent: QWidget | None = None) -> None:
        fig = Figure(figsize=(5, 2.2), facecolor="#252535", tight_layout=True)
        super().__init__(fig)
        self.setParent(parent)
        self._ax = fig.add_subplot(111, facecolor="#252535")
        self._style_axes()

    def _style_axes(self) -> None:
        ax = self._ax
        ax.set_xscale("log")
        ax.set_xlim(20, 20_000)
        ax.set_xlabel("Frequency (Hz)", color="#7f849c", fontsize=8)
        ax.set_ylabel("SPL (dB)", color="#7f849c", fontsize=8)
        ax.tick_params(colors="#7f849c", labelsize=7)
        for spine in ax.spines.values():
            spine.set_edgecolor("#44445a")
        ax.grid(True, which="both", color="#313145", linewidth=0.5, linestyle="--")
        ax.set_ylim(40, 110)

    def plot(
        self,
        freqs: list[float],
        spls: list[float],
        driver_type: str = "M",
        sweep_name: str = "",
    ) -> None:
        ax = self._ax
        ax.cla()
        self._style_axes()

        # Passband shading
        lo, hi = _PASSBANDS.get(driver_type, (80.0, 20_000.0))
        ax.axvspan(lo, hi, alpha=0.08, color="#89b4fa")

        # Response curve
        ax.plot(freqs, spls, color="#89b4fa", linewidth=1.5, label=sweep_name)
        if sweep_name:
            ax.set_title(sweep_name, color="#cdd6f4", fontsize=8, pad=4)

        self.draw()


# ---------------------------------------------------------------------------
# Main panel
# ---------------------------------------------------------------------------

class ValidationPanel(QWidget):
    """Shown after a sweep completes.

    Signals:
        accepted — user clicked Accept
        redo_requested — user clicked Redo
    """

    accepted = pyqtSignal()
    redo_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._build_ui()
        self.hide()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 8, 0, 0)
        root.setSpacing(8)

        # Section divider
        line = QFrame()
        line.setObjectName("separator")
        root.addWidget(line)

        header = QLabel("Validation")
        header.setObjectName("section_label")
        root.addWidget(header)

        # Badge row
        self._badge_row = QHBoxLayout()
        self._badge_row.setSpacing(6)
        self._badge_row.setAlignment(Qt.AlignmentFlag.AlignLeft)
        root.addLayout(self._badge_row)

        # Chart (hidden if no FRD)
        self._chart = _FrdChart(self)
        self._chart.setMinimumHeight(180)
        root.addWidget(self._chart)

        # No-chart notice (shown when export_latest failed)
        self._no_chart_label = QLabel(
            "Visual validation unavailable — check REW directly."
        )
        self._no_chart_label.setStyleSheet("color: #7f849c; font-style: italic;")
        self._no_chart_label.hide()
        root.addWidget(self._no_chart_label)

        # Accept / Redo buttons
        btn_row = QHBoxLayout()
        self._accept_btn = QPushButton("Accept")
        self._accept_btn.setObjectName("accept_btn")
        self._accept_btn.clicked.connect(self.accepted.emit)
        self._redo_btn = QPushButton("Redo")
        self._redo_btn.setObjectName("redo_btn")
        self._redo_btn.clicked.connect(self.redo_requested.emit)
        btn_row.addWidget(self._accept_btn)
        btn_row.addWidget(self._redo_btn)
        btn_row.addStretch()
        root.addLayout(btn_row)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def show_results(
        self,
        *,
        overload: bool,
        frd_path: Optional[Path],
        sweep_name: str,
        driver_name: str,
    ) -> None:
        """Populate and show the panel.

        Args:
            overload: whether REW reported an overload/clipping event
            frd_path: path to the exported .frd file (None if export failed)
            sweep_name: display name of the measurement
            driver_name: used to determine driver type for validation
        """
        self._clear_badges()
        dtype = _driver_type(driver_name)

        # Overload badge (always available — from MeasureResult)
        if overload:
            self._add_badge("err", "OVERLOAD — lower level and redo")
        else:
            self._add_badge("ok", "No overload")

        if frd_path is not None and frd_path.exists():
            freqs, spls = _parse_frd(frd_path)
            self._run_frd_checks(freqs, spls, dtype)
            self._chart.plot(freqs, spls, driver_type=dtype, sweep_name=sweep_name)
            self._chart.show()
            self._no_chart_label.hide()
        else:
            self._add_badge("info", "Visual validation unavailable — check REW directly")
            self._chart.hide()
            self._no_chart_label.show()

        self.show()

    def hide_results(self) -> None:
        self.hide()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _clear_badges(self) -> None:
        while self._badge_row.count():
            item = self._badge_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _add_badge(self, kind: str, text: str) -> None:
        self._badge_row.addWidget(_Badge(kind, text))

    def _run_frd_checks(
        self, freqs: list[float], spls: list[float], driver_type: str
    ) -> None:
        if not freqs:
            self._add_badge("err", "No data in FRD file")
            return

        max_spl = max(spls)

        # Silence check
        if max_spl < _SILENCE_THRESHOLD:
            self._add_badge("err", f"No signal detected (max {max_spl:.0f} dB)")
        else:
            self._add_badge("ok", "Signal detected")

        # Shape sanity: mean SPL in passband
        lo, hi = _PASSBANDS.get(driver_type, (80.0, 20_000.0))
        band_spls = [s for f, s in zip(freqs, spls) if lo <= f <= hi]
        if band_spls:
            mean_passband = sum(band_spls) / len(band_spls)
            if mean_passband < _PASSBAND_SPL_FLOOR:
                self._add_badge(
                    "warn",
                    f"Low passband response ({mean_passband:.0f} dB mean in {lo:.0f}–{hi:.0f} Hz)",
                )
            else:
                self._add_badge("ok", f"Passband response OK ({mean_passband:.0f} dB mean)")

        # Noise floor: variance in out-of-band region (above passband hi or below 50 Hz)
        oob_spls = [s for f, s in zip(freqs, spls) if f < 30.0 or f > hi * 2]
        if len(oob_spls) >= 5:
            mean_oob = sum(oob_spls) / len(oob_spls)
            variance = (sum((s - mean_oob) ** 2 for s in oob_spls) / len(oob_spls)) ** 0.5
            if variance > _NOISE_VARIANCE_WARN:
                self._add_badge("warn", f"High noise floor (±{variance:.0f} dB OOB variance)")
            else:
                self._add_badge("ok", f"Noise floor OK (±{variance:.0f} dB OOB variance)")
