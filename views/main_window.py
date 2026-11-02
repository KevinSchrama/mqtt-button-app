from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QToolBar,
    QStatusBar,
    QMessageBox,
    QFileDialog,
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QAction
from models import ButtonConfig, save_button_configs, load_button_configs
from views.button_widget import ButtonWidget
from views.config_dialog import ConfigDialog
from mqtt_client import MQTTClientWrapper
from pathlib import Path
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MQTT Button App")
        self.setMinimumSize(800, 600)
        self.config_file = Path("config/buttons.json")
        self.button_configs: list[ButtonConfig] = []
        self.mqtt_client = MQTTClientWrapper()
        self.init_ui()
        self.load_configs()

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.button_container = QWidget()
        self.button_container_layout = QVBoxLayout()
        self.button_container_layout.setContentsMargins(10, 10, 10, 10)
        self.button_container_layout.setSpacing(10)
        self.button_container.setLayout(self.button_container_layout)
        self.scroll_area.setWidget(self.button_container)

        layout.addWidget(self.scroll_area)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.create_toolbar()
        self.create_status_bar()

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        add_button_action = QAction("Add Button", self)
        add_button_action.triggered.connect(self.add_button)
        toolbar.addAction(add_button_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_configs)
        toolbar.addAction(save_action)

        load_action = QAction("Load", self)
        load_action.triggered.connect(self.load_configs)
        toolbar.addAction(load_action)

        toolbar.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        toolbar.addAction(exit_action)

    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def add_button(self):
        dialog = ConfigDialog(parent=self)
        if dialog.exec() == 1:
            config = dialog.get_config()
            self.button_configs.append(config)
            self.add_button_to_ui(config)
            self.save_configs()

    def add_button_to_ui(self, config: ButtonConfig):
        button_widget = ButtonWidget(config)
        button_widget.button_pressed.connect(self.on_button_pressed)
        self.button_container_layout.addWidget(button_widget)

    def on_button_pressed(self, config: ButtonConfig):
        def callback(success: bool, message: str):
            self.status_bar.showMessage(message)
            for i in range(self.button_container_layout.count()):
                widget = self.button_container_layout.itemAt(i).widget()
                if isinstance(widget, ButtonWidget) and widget.config == config:
                    widget.set_status(success, message)
                    QTimer.singleShot(3000, widget.clear_status)
                    break

        self.mqtt_client.publish_message(config, timeout=10, callback=callback)

    def save_configs(self):
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            save_button_configs(self.button_configs, self.config_file)
            self.status_bar.showMessage("Configuration saved")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save configuration: {str(e)}")

    def load_configs(self):
        try:
            self.button_configs = load_button_configs(self.config_file)
            while self.button_container_layout.count():
                item = self.button_container_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            for config in self.button_configs:
                self.add_button_to_ui(config)
            self.status_bar.showMessage("Configuration loaded")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load configuration: {str(e)}")
