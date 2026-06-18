from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
)

from app.core.model_manager import ModelManager


class DownloadDialog(QDialog):
    def __init__(self, model_manager: ModelManager, parent=None):
        super().__init__(parent)
        self._model_manager = model_manager
        self._setup_ui()
        self._connect_signals()
        self._start_download()

    def _setup_ui(self):
        self.setWindowTitle("Kokoro TTS")
        self.setFixedSize(440, 306)
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.WindowTitleHint
        )

        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)

        content = QVBoxLayout()
        content.setContentsMargins(40, 36, 40, 0)
        content.setSpacing(0)

        content.addStretch()

        title = QLabel("Welcome to Kokoro TTS")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content.addWidget(title)

        content.addSpacing(8)

        self._subtitle = QLabel("Downloading the voice model…")
        self._subtitle.setObjectName("subtitle")
        self._subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._subtitle.setWordWrap(True)
        content.addWidget(self._subtitle)

        content.addSpacing(20)

        self._progress = QProgressBar()
        self._progress.setFixedHeight(4)
        self._progress.setValue(0)
        self._progress.setTextVisible(False)
        content.addWidget(self._progress)

        content.addSpacing(6)

        self._status_label = QLabel("")
        self._status_label.setObjectName("subtitle")
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content.addWidget(self._status_label)

        content.addStretch()

        main.addLayout(content)

        btn_row = QHBoxLayout()
        btn_row.setContentsMargins(40, 0, 40, 12)
        self._continue_btn = QPushButton("Continue")
        self._continue_btn.setObjectName("primary")
        self._continue_btn.setEnabled(False)
        self._continue_btn.setVisible(False)
        btn_row.addWidget(self._continue_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        main.addLayout(btn_row)

        main.addSpacing(10)

        footer_frame = QFrame()
        footer_frame.setObjectName("footerBar")
        footer_frame.setFixedHeight(26)
        fl = QHBoxLayout(footer_frame)
        fl.setContentsMargins(20, 0, 0, 0)
        status_dot = QLabel()
        status_dot.setFixedSize(8, 8)
        status_dot.setObjectName("statusDot")
        fl.addWidget(status_dot)
        fl.addSpacing(6)
        status_text = QLabel("Model ready")
        status_text.setObjectName("footerStatus")
        fl.addWidget(status_text)
        fl.addStretch()
        flabel = QLabel("made with ♥ by kokovrinn")
        flabel.setObjectName("footer")
        flabel.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        fl.addWidget(flabel)
        main.addWidget(footer_frame)

    def _connect_signals(self):
        self._model_manager.progress.connect(self._on_progress)
        self._model_manager.download_finished.connect(self._on_finished)
        self._continue_btn.clicked.connect(self.accept)

    def _start_download(self):
        import threading
        thread = threading.Thread(
            target=self._model_manager.download_model, daemon=True
        )
        thread.start()

    def _on_progress(self, percent: int, message: str):
        self._progress.setValue(percent)
        self._status_label.setText(message)

    def _on_finished(self, success: bool, error: str):
        if success:
            self._subtitle.setText("Model ready!")
            self._progress.setValue(100)
            self._continue_btn.setVisible(True)
            self._continue_btn.setEnabled(True)
            self._continue_btn.setFocus()
        else:
            self._subtitle.setText("Download failed")
            self._status_label.setText(error)
