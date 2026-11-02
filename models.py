from dataclasses import dataclass, field
from typing import Optional
import json
from pathlib import Path


@dataclass
class ButtonConfig:
    server: str = ""
    port: int = 1883
    username: Optional[str] = None
    password: Optional[str] = None
    topic: str = ""
    message: str = ""
    qos: int = 0
    retain: bool = False
    label: str = "New Button"
    button_color: str = "#4CAF50"

    def to_dict(self) -> dict:
        return {
            "server": self.server,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "topic": self.topic,
            "message": self.message,
            "qos": self.qos,
            "retain": self.retain,
            "label": self.label,
            "button_color": self.button_color,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ButtonConfig":
        return cls(
            server=data.get("server", ""),
            port=data.get("port", 1883),
            username=data.get("username"),
            password=data.get("password"),
            topic=data.get("topic", ""),
            message=data.get("message", ""),
            qos=data.get("qos", 0),
            retain=data.get("retain", False),
            label=data.get("label", "New Button"),
            button_color=data.get("button_color", "#4CAF50"),
        )


def save_button_configs(configs: list[ButtonConfig], file_path: Path) -> None:
    data = [config.to_dict() for config in configs]
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def load_button_configs(file_path: Path) -> list[ButtonConfig]:
    if not file_path.exists():
        return []
    with open(file_path, "r") as f:
        data = json.load(f)
    return [ButtonConfig.from_dict(item) for item in data]
