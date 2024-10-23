from typing import Any, Dict

class Settings:
    def __init__(self):
        self._settings: Dict[str, Any] = {
            "notification_enabled": True,
            "language": "en",
            "timezone": "UTC"
        }

    def get(self, key: str) -> Any:
        return self._settings.get(key)

    def set(self, key: str, value: Any) -> None:
        if key in self._settings:
            self._settings[key] = value

    def display(self) -> str:
        return "\n".join(f"{k}: {v}" for k, v in self._settings.items())