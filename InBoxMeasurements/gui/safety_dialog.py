"""Modal blocking safety confirmation dialog."""
from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class SafetyDialog(QDialog):
    """Blocks until the user checks the confirmation box.

    Cannot be dismissed with Escape or the window close button until
    the checkbox is checked.
    """

    def __init__(self, title: str, instruction: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Safety Check")
        self.setModal(True)
        self.setMinimumWidth(460)
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(20, 20, 20, 20)

        # Red header
        header = QLabel(f"⚠  {title}")
        header.setObjectName("safety_header")
        header.setWordWrap(True)
        layout.addWidget(header)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #f38ba8;")
        layout.addWidget(line)

        # Instruction text
        body = QLabel(instruction)
        body.setWordWrap(True)
        body.setStyleSheet("color: #cdd6f4; font-size: 10pt; padding: 4px 0;")
        layout.addWidget(body)

        layout.addSpacing(6)

        # Confirmation checkbox
        self._check = QCheckBox("I have completed the above step and it is safe to proceed.")
        self._check.setStyleSheet("font-weight: bold;")
        self._check.toggled.connect(self._on_toggle)
        layout.addWidget(self._check)

        layout.addSpacing(4)

        # OK button (disabled until checked)
        self._ok_btn = QPushButton("Proceed")
        self._ok_btn.setEnabled(False)
        self._ok_btn.setMinimumHeight(36)
        self._ok_btn.setStyleSheet(
            "background: #1e6b3a; color: #a6e3a1; border-color: #a6e3a1;"
            "font-weight: bold;"
        )
        self._ok_btn.clicked.connect(self.accept)
        layout.addWidget(self._ok_btn)

    def _on_toggle(self, checked: bool) -> None:
        self._ok_btn.setEnabled(checked)

    def keyPressEvent(self, event) -> None:  # type: ignore[override]
        # Block Escape so the dialog cannot be dismissed without confirming
        if event.key() == Qt.Key.Key_Escape:
            return
        super().keyPressEvent(event)

    def closeEvent(self, event) -> None:  # type: ignore[override]
        # Prevent closing via Alt+F4 etc. unless confirmed
        if not self._check.isChecked():
            event.ignore()
        else:
            super().closeEvent(event)
