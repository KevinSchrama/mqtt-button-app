from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QComboBox,
    QCheckBox,
    QDialogButtonBox,
    QColorDialog,
    QPushButton,
    QHBoxLayout,
    QLabel,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from models import ButtonConfig


class ConfigDialog(QDialog):
    def __init__(self, config: ButtonConfig = None, parent=None):
        super().__init__(parent)
        self.config = config if config else ButtonConfig()
        self.setWindowTitle("Add/Edit Button")
        self.setMinimumWidth(400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.label_input = QLineEdit(self.config.label)
        self.server_input = QLineEdit(self.config.server)
        self.port_input = QSpinBox()
        self.port_input.setRange(1, 65535)
        self.port_input.setValue(self.config.port)

        self.username_input = QLineEdit(self.config.username or "")
        self.password_input = QLineEdit(self.config.password or "")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.topic_input = QLineEdit(self.config.topic)
        self.message_input = QLineEdit(self.config.message)

        self.qos_input = QComboBox()
        self.qos_input.addItems(["0", "1", "2"])
        self.qos_input.setCurrentIndex(self.config.qos)

        self.retain_input = QCheckBox()
        self.retain_input.setChecked(self.config.retain)

        self.color_button = QPushButton()
        self.color_button.setStyleSheet(
            f"background-color: {self.config.button_color}; "
            f"min-width: 30px; min-height: 30px;"
        )
        self.color_button.clicked.connect(self.choose_color)

        form_layout.addRow("Label:", self.label_input)
        form_layout.addRow("Server:", self.server_input)
        form_layout.addRow("Port:", self.port_input)
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)
        form_layout.addRow("Topic:", self.topic_input)
        form_layout.addRow("Message:", self.message_input)
        form_layout.addRow("QoS:", self.qos_input)
        form_layout.addRow("Retain:", self.retain_input)

        color_layout = QHBoxLayout()
        color_layout.addWidget(self.color_button)
        color_layout.addWidget(QLabel("Button Color"))
        form_layout.addRow("Color:", color_layout)

        layout.addLayout(form_layout)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def choose_color(self):
        color = QColorDialog.getColor(
            QColor(self.config.button_color), self, "Choose Button Color"
        )
        if color.isValid():
            self.config.button_color = color.name()
            self.color_button.setStyleSheet(
                f"background-color: {self.config.button_color}; "
                f"min-width: 30px; min-height: 30px;"
            )

    def accept(self):
        self.config.label = self.label_input.text()
        self.config.server = self.server_input.text()
        self.config.port = self.port_input.value()
        self.config.username = self.username_input.text() or None
        self.config.password = self.password_input.text() or None
        self.config.topic = self.topic_input.text()
        self.config.message = self.message_input.text()
        self.config.qos = int(self.qos_input.currentText())
        self.config.retain = self.retain_input.isChecked()
        super().accept()

    def get_config(self) -> ButtonConfig:
        return self.config
