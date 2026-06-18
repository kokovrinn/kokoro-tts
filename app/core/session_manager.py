import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from app.core.config import CONFIG_DIR, config

SESSIONS_FILE = CONFIG_DIR / "sessions.json"
TEXTS_DIR = CONFIG_DIR / "texts"


class SessionManager:

    def __init__(self):
        self._sessions: list[dict] = []
        self._current_id: str | None = None
        TEXTS_DIR.mkdir(parents=True, exist_ok=True)
        self._load()

    @property
    def current(self) -> dict | None:
        for s in self._sessions:
            if s["id"] == self._current_id:
                return s
        return None

    @property
    def current_id(self) -> str | None:
        return self._current_id

    @property
    def all(self) -> list[dict]:
        return sorted(self._sessions, key=lambda s: s["updated_at"], reverse=True)

    def create(self, name: str, language: str = "a", voice: str = "af_heart", speed: float = 1.0) -> str:
        sid = uuid.uuid4().hex[:8]
        now = _now()
        session = {
            "id": sid,
            "name": name,
            "preview": "",
            "audio_path": None,
            "language": language,
            "voice": voice,
            "speed": speed,
            "created_at": now,
            "updated_at": now,
        }
        self._sessions.append(session)
        self._current_id = sid
        self._save()
        return sid

    def update_voice_settings(self, sid: str, language: str, voice: str, speed: float):
        s = self._find(sid)
        if s:
            s["language"] = language
            s["voice"] = voice
            s["speed"] = speed
            s["updated_at"] = _now()
        self._save()

    def rename(self, sid: str, name: str):
        s = self._find(sid)
        if s:
            s["name"] = name
            s["updated_at"] = _now()
        self._save()

    def update_audio_path(self, sid: str, path: str | None):
        s = self._find(sid)
        if s:
            s["audio_path"] = path
            s["updated_at"] = _now()
        self._save()

    def update_text(self, sid: str, text: str):
        s = self._find(sid)
        if s:
            self._write_text_file(sid, text)
            s["preview"] = text[:100]
            s["updated_at"] = _now()
            self._save()

    def read_text(self, sid: str) -> str:
        path = TEXTS_DIR / f"{sid}.txt"
        if path.exists():
            return path.read_text(encoding="utf-8")
        return ""

    def clear_text(self, sid: str):
        s = self._find(sid)
        if s:
            path = TEXTS_DIR / f"{sid}.txt"
            if path.exists():
                path.unlink()
            s["preview"] = ""
            s["updated_at"] = _now()
            self._save()

    def switch_to(self, sid: str):
        self._current_id = sid
        self._save()

    def delete(self, sid: str):
        self.clear_text(sid)
        self._sessions = [s for s in self._sessions if s["id"] != sid]
        if self._current_id == sid:
            self._current_id = self._sessions[0]["id"] if self._sessions else None
        self._save()

    def _write_text_file(self, sid: str, text: str):
        TEXTS_DIR.mkdir(parents=True, exist_ok=True)
        path = TEXTS_DIR / f"{sid}.txt"
        path.write_text(text, encoding="utf-8")

    def _find(self, sid: str) -> dict | None:
        for s in self._sessions:
            if s["id"] == sid:
                return s
        return None

    def get(self, sid: str) -> dict | None:
        return self._find(sid)

    def _load(self):
        SESSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
        if SESSIONS_FILE.exists():
            try:
                with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    self._sessions = data
                    self._current_id = self._sessions[0]["id"] if self._sessions else None
                else:
                    self._sessions = data.get("sessions", [])
                    self._current_id = data.get("last_session_id")
                self._migrate()
                if not self._sessions:
                    self._current_id = None
                elif not self._current_id or not any(
                    s["id"] == self._current_id for s in self._sessions
                ):
                    self._current_id = self._sessions[0]["id"]
            except (json.JSONDecodeError, IOError, KeyError, IndexError):
                self._sessions = []
                self._current_id = None

    def _migrate(self):
        changed = False
        for s in self._sessions:
            if "text" in s:
                if s["text"]:
                    self._write_text_file(s["id"], s["text"])
                    s["preview"] = s["text"][:100]
                del s["text"]
                changed = True
            if "preview" not in s:
                s["preview"] = ""
                changed = True
        if changed:
            self._save()

    def _save(self):
        SESSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "sessions": self._sessions,
                    "last_session_id": self._current_id,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
