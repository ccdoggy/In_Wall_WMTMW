"""
sweep_gui.py
============

GUI entry point for the WMTMW in-box measurement session.
Replaces sweep_wizard.py as the primary interface.
The CLI wizard is still available as a fallback: python sweep_wizard.py

Usage:
    python sweep_gui.py
    python sweep_gui.py --base-url http://10.0.0.42:4735
    python sweep_gui.py --log-path /path/to/sweep_log.csv
    python sweep_gui.py --out-dir  /path/to/export

Requirements:
    pip install PyQt6 matplotlib
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

# Ensure InBoxMeasurements/ is on sys.path so sibling modules resolve
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from rew_api import RewApi
from gui.session_state import SessionState
from gui.main_window import MainWindow
from gui import theme


_DEFAULT_LOG  = _HERE / "sweep_log.csv"
_DEFAULT_EXPORT = _HERE / "rew"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="sweep_gui",
        description="WMTMW in-box measurement GUI.",
    )
    p.add_argument(
        "--base-url", default="http://localhost:4735",
        help="REW HTTP API base URL (default: http://localhost:4735)",
    )
    p.add_argument(
        "--log-path", type=Path, default=_DEFAULT_LOG,
        help=f"CSV progress log (default: {_DEFAULT_LOG.name})",
    )
    p.add_argument(
        "--out-dir", type=Path, default=_DEFAULT_EXPORT,
        help=f"Export directory for FRD/WAV/TXT files (default: {_DEFAULT_EXPORT.name}/)",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()

    app = QApplication(sys.argv)
    app.setApplicationName("WMTMW Measurement Wizard")
    theme.apply(app)

    session = SessionState(args.log_path)
    api = RewApi(base_url=args.base_url)

    window = MainWindow(session, api, args.out_dir)
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
