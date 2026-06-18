from pathlib import Path

import requests
from huggingface_hub import hf_hub_url
from PySide6.QtCore import QObject, Signal

from app.core.config import MODEL_DIR, config
from app.core.voices import REPO_ID


class ModelManager(QObject):
    progress = Signal(int, str)
    download_finished = Signal(bool, str)
    model_ready = Signal()
    voice_ready = Signal(str)

    _MODEL_FILE = "kokoro-v1_0.pth"
    _CONFIG_FILE = "config.json"

    def __init__(self, parent=None):
        super().__init__(parent)

    def is_model_downloaded(self) -> bool:
        return (MODEL_DIR / self._MODEL_FILE).exists()

    def is_voice_downloaded(self, voice: str) -> bool:
        if not voice:
            return False
        return (MODEL_DIR / "voices" / f"{voice}.pt").exists()

    def check_and_emit(self):
        if self.is_model_downloaded():
            config.model_downloaded = True
            self.model_ready.emit()

    def download_model(self, voice: str = None):
        files = [self._CONFIG_FILE, self._MODEL_FILE]
        try:
            MODEL_DIR.mkdir(parents=True, exist_ok=True)
            voices_dir = MODEL_DIR / "voices"
            voices_dir.mkdir(parents=True, exist_ok=True)

            for filename in files:
                url = hf_hub_url(REPO_ID, filename)
                dest = MODEL_DIR / filename
                self._download_file(url, dest, filename)

            if voice:
                vfile = f"voices/{voice}.pt"
                url = hf_hub_url(REPO_ID, vfile)
                dest = voices_dir / f"{voice}.pt"
                self._download_file(url, dest, voice)

            config.model_downloaded = True
            if voice:
                self.voice_ready.emit(voice)
            self.download_finished.emit(True, "")
            self.model_ready.emit()
        except Exception as e:
            self.download_finished.emit(False, str(e))

    def download_voice(self, voice: str):
        if self.is_voice_downloaded(voice):
            self.voice_ready.emit(voice)
            return
        try:
            voices_dir = MODEL_DIR / "voices"
            voices_dir.mkdir(parents=True, exist_ok=True)
            vfile = f"voices/{voice}.pt"
            url = hf_hub_url(REPO_ID, vfile)
            dest = voices_dir / f"{voice}.pt"
            self._download_file(url, dest, voice)
            self.voice_ready.emit(voice)
        except Exception:
            raise

    def ensure_voice(self, voice: str) -> bool:
        if self.is_voice_downloaded(voice):
            return True
        try:
            voices_dir = MODEL_DIR / "voices"
            voices_dir.mkdir(parents=True, exist_ok=True)
            vfile = f"voices/{voice}.pt"
            url = hf_hub_url(REPO_ID, vfile)
            dest = voices_dir / f"{voice}.pt"
            headers = {}
            token = self._get_token()
            if token:
                headers["Authorization"] = f"Bearer {token}"
            resp = requests.get(url, headers=headers, stream=True, timeout=30)
            resp.raise_for_status()
            temp = dest.with_suffix(".tmp")
            with open(temp, "wb") as f:
                for chunk in resp.iter_content(65536):
                    if chunk:
                        f.write(chunk)
            temp.rename(dest)
            return True
        except Exception:
            return False

    def _download_file(self, url: str, dest: Path, display_name: str):
        headers = {}
        token = self._get_token()
        if token:
            headers["Authorization"] = f"Bearer {token}"

        response = requests.get(url, headers=headers, stream=True, timeout=30)
        response.raise_for_status()

        total = int(response.headers.get("content-length", 0))
        downloaded = 0
        temp = dest.with_suffix(".tmp")

        with open(temp, "wb") as f:
            for chunk in response.iter_content(chunk_size=65536):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        percent = int(downloaded * 100 / total)
                        self.progress.emit(percent, f"{display_name} ({percent}%)")

        temp.rename(dest)

    def _get_token(self):
        import os
        return os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")

    def get_cache_size(self) -> str:
        total = 0
        for f in MODEL_DIR.rglob("*"):
            if f.is_file():
                total += f.stat().st_size
        if total < 1024:
            return f"{total} B"
        elif total < 1024 * 1024:
            return f"{total / 1024:.1f} KB"
        elif total < 1024 * 1024 * 1024:
            return f"{total / (1024 * 1024):.1f} MB"
        else:
            return f"{total / (1024 * 1024 * 1024):.1f} GB"

    def clear_cache(self):
        for f in MODEL_DIR.rglob("*"):
            if f.is_file():
                f.unlink()
        for d in sorted(MODEL_DIR.rglob("*"), reverse=True):
            if d.is_dir() and not any(d.iterdir()):
                d.rmdir()
        config.model_downloaded = False
