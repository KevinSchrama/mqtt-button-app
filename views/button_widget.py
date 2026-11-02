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
        self.button.setStyleSheet(
            f"background-color: {self.config.button_color}; "
            f"color: white; "
            f"border: none; "
            f"border-radius: 5px; "
            f"padding: 10px; "
            f"font-size: 14px; "
            f"min-height: 60px;"
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
