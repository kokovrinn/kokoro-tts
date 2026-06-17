import json
import os
from pathlib import Path
from typing import Any

CONFIG_DIR = Path.home() / ".kokoro-tts"
CONFIG_FILE = CONFIG_DIR / "config.json"
OUTPUT_DIR = Path.home() / "Kokoro TTS Outputs"
MODEL_DIR = CONFIG_DIR / "models"

DEFAULT_CONFIG = {
    "language": "a",
    "voice": "af_heart",
    "speed": 1.0,
    "theme": "dark",
    "output_dir": str(OUTPUT_DIR),
    "output_format": "wav",
    "first_run": True,
    "model_downloaded": False,
}


class Config:
    def __init__(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self._data: dict[str, Any] = {}
        self.load()

    def load(self):
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
            except (json.JSONDecodeError, IOError):
                loaded = {}
            self._data = {**DEFAULT_CONFIG, **loaded}
        else:
            self._data = dict(DEFAULT_CONFIG)
            self.save()

    def save(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any):
        self._data[key] = value
        self.save()

    @property
    def language(self) -> str:
        return self._data["language"]

    @property
    def voice(self) -> str:
        return self._data["voice"]

    @property
    def speed(self) -> float:
        return self._data["speed"]

    @property
    def theme(self) -> str:
        return self._data["theme"]

    @property
    def output_dir(self) -> str:
        return self._data["output_dir"]

    @property
    def output_format(self) -> str:
        return self._data["output_format"]

    @property
    def first_run(self) -> bool:
        return self._data["first_run"]

    @property
    def model_downloaded(self) -> bool:
        return self._data["model_downloaded"]

    @language.setter
    def language(self, value: str):
        self.set("language", value)

    @voice.setter
    def voice(self, value: str):
        self.set("voice", value)

    @speed.setter
    def speed(self, value: float):
        self.set("speed", value)

    @theme.setter
    def theme(self, value: str):
        self.set("theme", value)

    @output_dir.setter
    def output_dir(self, value: str):
        self.set("output_dir", value)

    @output_format.setter
    def output_format(self, value: str):
        self.set("output_format", value)

    @first_run.setter
    def first_run(self, value: bool):
        self.set("first_run", value)

    @model_downloaded.setter
    def model_downloaded(self, value: bool):
        self.set("model_downloaded", value)


config = Config()
