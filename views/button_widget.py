from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from models import ButtonConfig


class ButtonWidget(QWidget):
    button_pressed = pyqtSignal(ButtonConfig)

    def __init__(self, config: ButtonConfig, parent=None):
        super().__init__(parent)
        self.config = config
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)

        self.button = QPushButton(self.config.label)
        button_color = self.config.button_color
        lighten_color = self._lighten_color(button_color, 20)
        darken_color = self._darken_color(button_color, 20)
        
        self.button.setStyleSheet(
            f"QPushButton {{\n"
            f"    background-color: {button_color};\n"
            f"    color: white;\n"
            f"    border: none;\n"
            f"    border-radius: 8px;\n"
            f"    padding: 10px;\n"
            f"    font-size: 14px;\n"
            f"    min-height: 60px;\n"
            f"}}\n"
            f"QPushButton:hover {{\n"
            f"    background-color: {lighten_color};\n"
            f"}}\n"
            f"QPushButton:pressed {{\n"
            f"    background-color: {darken_color};\n"
            f"}}"
        )
        self.button.clicked.connect(self.on_button_click)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #666; font-size: 12px;")
        self.status_label.setVisible(False)

        layout.addWidget(self.button)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

    def on_button_click(self):
        self.button_pressed.emit(self.config)
        self.status_label.setText("Sending...")
        self.status_label.setVisible(True)

    def set_status(self, success: bool, message: str):
        if success:
            self.status_label.setText("Sent!")
            self.status_label.setStyleSheet("color: #4CAF50; font-size: 12px;")
        else:
            self.status_label.setText(f"Error: {message}")
            self.status_label.setStyleSheet("color: #F44336; font-size: 12px;")
        self.status_label.setVisible(True)

    def clear_status(self):
        self.status_label.setVisible(False)

    @staticmethod
    def _lighten_color(color: str, percent: int) -> str:
        return ButtonWidget._adjust_color(color, 1.0 + percent / 100.0)

    @staticmethod
    def _darken_color(color: str, percent: int) -> str:
        return ButtonWidget._adjust_color(color, 1.0 - percent / 100.0)

    @staticmethod
    def _adjust_color(color: str, factor: float) -> str:
        if color.startswith("#"):
            color = color[1:]
        if len(color) == 3:
            color = "".join([c * 2 for c in color])
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        return f"#{r:02x}{g:02x}{b:02x}"
