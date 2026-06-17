import sys
import os
import shutil
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from app.core.config import MODEL_DIR, CONFIG_DIR

os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
os.environ.setdefault("KOKORO_LOG_LEVEL", "WARNING")
os.environ.setdefault("HF_HUB_CACHE", str(MODEL_DIR))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from app.core.config import config
from app.core.model_manager import ModelManager
from app.ui.main_window import MainWindow
from app.ui.download_dialog import DownloadDialog
from app.ui.setup_dialog import SetupDialog
from app.ui.styles import get_style


def main():
    args = set(sys.argv[1:])

    if "--reset" in args:
        if CONFIG_DIR.exists():
            shutil.rmtree(CONFIG_DIR)
        print("Reset: config and model cache cleared.")
        return

    if "--reset-config" in args:
        cfg = CONFIG_DIR / "config.json"
        if cfg.exists():
            cfg.unlink()
        print("Reset: config cleared.")
        return

    if "--reset-model" in args:
        if MODEL_DIR.exists():
            shutil.rmtree(MODEL_DIR)
        print("Reset: model cache cleared.")
        return

    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QApplication(sys.argv)
    app.setApplicationName("Kokoro TTS")
    app.setOrganizationName("kokoro-tts")
    app.setStyle("Fusion")
    app.setStyleSheet(get_style(config.theme))

    force_download = "--show-download" in args

    if config.first_run or force_download:
        model_mgr = ModelManager()
        if force_download or not model_mgr.is_model_downloaded():
            dlg = DownloadDialog(model_mgr)
            if dlg.exec() != DownloadDialog.DialogCode.Accepted:
                sys.exit(0)
        dlg = SetupDialog(model_mgr)
        if dlg.exec() != SetupDialog.DialogCode.Accepted:
            sys.exit(0)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
