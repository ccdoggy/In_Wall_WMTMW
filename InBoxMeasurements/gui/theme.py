"""Dark theme for the WMTMW measurement GUI."""
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication

# Palette colors
BG          = QColor("#1e1e2e")
BG_ALT      = QColor("#2a2a3e")
BG_PANEL    = QColor("#252535")
BORDER      = QColor("#44445a")
TEXT        = QColor("#cdd6f4")
TEXT_DIM    = QColor("#7f849c")
ACCENT      = QColor("#89b4fa")
GREEN       = QColor("#a6e3a1")
YELLOW      = QColor("#f9e2af")
RED         = QColor("#f38ba8")
ORANGE      = QColor("#fab387")

# Status colors (for list items)
STATUS_DONE    = "#a6e3a1"
STATUS_ACTIVE  = "#89b4fa"
STATUS_PENDING = "#585b70"
STATUS_SKIPPED = "#f9e2af"
STATUS_ERROR   = "#f38ba8"

STYLESHEET = """
QMainWindow, QWidget {
    background-color: #1e1e2e;
    color: #cdd6f4;
    font-family: "Segoe UI", sans-serif;
    font-size: 10pt;
}
QTabWidget::pane {
    border: 1px solid #44445a;
    background: #1e1e2e;
}
QTabBar::tab {
    background: #2a2a3e;
    color: #7f849c;
    padding: 6px 14px;
    border: 1px solid #44445a;
    border-bottom: none;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background: #1e1e2e;
    color: #cdd6f4;
    border-bottom: 2px solid #89b4fa;
}
QTabBar::tab:hover {
    color: #cdd6f4;
}
QListWidget {
    background: #252535;
    border: 1px solid #44445a;
    outline: none;
}
QListWidget::item {
    padding: 6px 8px;
    border-bottom: 1px solid #2a2a3e;
}
QListWidget::item:selected {
    background: #313145;
    color: #cdd6f4;
}
QListWidget::item:hover {
    background: #2d2d42;
}
QPushButton {
    background: #313145;
    color: #cdd6f4;
    border: 1px solid #44445a;
    border-radius: 4px;
    padding: 6px 18px;
    min-height: 28px;
}
QPushButton:hover {
    background: #3d3d55;
    border-color: #89b4fa;
}
QPushButton:pressed {
    background: #89b4fa;
    color: #1e1e2e;
}
QPushButton:disabled {
    color: #585b70;
    border-color: #313145;
    background: #252535;
}
QPushButton#measure_btn {
    background: #1e6b3a;
    color: #a6e3a1;
    border-color: #a6e3a1;
    font-size: 12pt;
    font-weight: bold;
    min-height: 44px;
    padding: 10px 28px;
}
QPushButton#measure_btn:hover {
    background: #27854a;
}
QPushButton#measure_btn:disabled {
    background: #252535;
    color: #585b70;
    border-color: #313145;
}
QPushButton#accept_btn {
    background: #1e6b3a;
    color: #a6e3a1;
    border-color: #a6e3a1;
}
QPushButton#redo_btn {
    background: #5a3a1e;
    color: #fab387;
    border-color: #fab387;
}
QLabel#phase_header {
    font-size: 14pt;
    font-weight: bold;
    color: #89b4fa;
}
QLabel#sweep_counter {
    color: #7f849c;
    font-size: 9pt;
}
QLabel#section_label {
    font-size: 9pt;
    font-weight: bold;
    color: #7f849c;
    text-transform: uppercase;
    letter-spacing: 1px;
}
QLabel#safety_header {
    font-size: 12pt;
    font-weight: bold;
    color: #f38ba8;
    padding: 8px;
}
QFrame#separator {
    background: #44445a;
    max-height: 1px;
    min-height: 1px;
}
QStatusBar {
    background: #181825;
    color: #7f849c;
    border-top: 1px solid #44445a;
}
QStatusBar::item {
    border: none;
}
QScrollBar:vertical {
    background: #252535;
    width: 8px;
}
QScrollBar::handle:vertical {
    background: #44445a;
    border-radius: 4px;
    min-height: 20px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QCheckBox {
    spacing: 8px;
    color: #cdd6f4;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #44445a;
    border-radius: 3px;
    background: #252535;
}
QCheckBox::indicator:checked {
    background: #89b4fa;
    border-color: #89b4fa;
}
QTextEdit {
    background: #252535;
    color: #cdd6f4;
    border: 1px solid #44445a;
    border-radius: 4px;
}
"""


def apply(app: QApplication) -> None:
    app.setStyle("Fusion")
    pal = QPalette()
    pal.setColor(QPalette.ColorRole.Window,          BG)
    pal.setColor(QPalette.ColorRole.WindowText,      TEXT)
    pal.setColor(QPalette.ColorRole.Base,            BG_PANEL)
    pal.setColor(QPalette.ColorRole.AlternateBase,   BG_ALT)
    pal.setColor(QPalette.ColorRole.ToolTipBase,     BG_ALT)
    pal.setColor(QPalette.ColorRole.ToolTipText,     TEXT)
    pal.setColor(QPalette.ColorRole.Text,            TEXT)
    pal.setColor(QPalette.ColorRole.Button,          BG_ALT)
    pal.setColor(QPalette.ColorRole.ButtonText,      TEXT)
    pal.setColor(QPalette.ColorRole.BrightText,      QColor("#ffffff"))
    pal.setColor(QPalette.ColorRole.Highlight,       ACCENT)
    pal.setColor(QPalette.ColorRole.HighlightedText, BG)
    pal.setColor(QPalette.ColorRole.Link,            ACCENT)
    app.setPalette(pal)
    app.setStyleSheet(STYLESHEET)
