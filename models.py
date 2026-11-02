from dataclasses import dataclass, asdict
from typing import Optional
from pathlib import Path
import json


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
        return asdict(self)

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


class ButtonConfigManager:
    def __init__(self, config_path: Optional[Path] = None):
        if config_path is None:
            config_path = Path("config/buttons.json")
        self.config_path = config_path
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, buttons: list[ButtonConfig]) -> None:
        data = [btn.to_dict() for btn in buttons]
        with open(self.config_path, "w") as f:
            json.dump(data, f, indent=2)

    def load(self) -> list[ButtonConfig]:
        if not self.config_path.exists():
            return []
        with open(self.config_path, "r") as f:
            data = json.load(f)
        return [ButtonConfig.from_dict(btn) for btn in data]


def save_button_configs(configs: list[ButtonConfig], file_path: Path) -> None:
    ButtonConfigManager(file_path).save(configs)


def load_button_configs(file_path: Path) -> list[ButtonConfig]:
    return ButtonConfigManager(file_path).load()
