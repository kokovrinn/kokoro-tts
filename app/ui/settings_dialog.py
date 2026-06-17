from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QSlider, QCheckBox, QFileDialog, QGroupBox,
    QWidget, QFormLayout,
)

from app.core.config import config
from app.core.model_manager import ModelManager
from app.core.voices import LANGUAGES, VOICE_INFO, get_all_voices, get_voice_display_name


class SettingsDialog(QDialog):
    def __init__(self, model_manager: ModelManager, parent=None):
        super().__init__(parent)
        self._model_manager = model_manager
        self._setup_ui()
        self._connect_signals()
        self._populate()

    def _setup_ui(self):
        self.setWindowTitle("Settings")
        self.setMinimumWidth(460)
        self.setMaximumWidth(520)
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.WindowCloseButtonHint
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        title = QLabel("Settings")
        title.setObjectName("title")
        layout.addWidget(title)

        voice_group = QGroupBox("Voice & Language")
        voice_form = QFormLayout(voice_group)
        voice_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        voice_form.setSpacing(10)

        self._lang_combo = QComboBox()
        voice_form.addRow("Language", self._lang_combo)

        self._voice_combo = QComboBox()
        voice_form.addRow("Voice", self._voice_combo)

        speed_row = QHBoxLayout()
        self._speed_slider = QSlider(Qt.Orientation.Horizontal)
        self._speed_slider.setRange(50, 200)
        self._speed_slider.setValue(100)
        speed_row.addWidget(self._speed_slider)
        self._speed_label = QLabel("1.0×")
        self._speed_label.setMinimumWidth(44)
        self._speed_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        speed_row.addWidget(self._speed_label)
        voice_form.addRow("Speed", speed_row)

        layout.addWidget(voice_group)

        app_group = QGroupBox("Application")
        app_form = QFormLayout(app_group)
        app_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        app_form.setSpacing(10)

        self._theme_check = QCheckBox()
        app_form.addRow("Dark theme", self._theme_check)

        out_row = QHBoxLayout()
        self._output_label = QLabel("")
        self._output_label.setObjectName("subtitle")
        out_row.addWidget(self._output_label, 1)
        self._output_btn = QPushButton("Browse…")
        self._output_btn.clicked.connect(self._browse_output)
        out_row.addWidget(self._output_btn)
        app_form.addRow("Output folder", out_row)

        layout.addWidget(app_group)

        model_group = QGroupBox("Model Cache")
        model_layout = QVBoxLayout(model_group)

        self._cache_info = QLabel("")
        self._cache_info.setObjectName("subtitle")
        model_layout.addWidget(self._cache_info)

        model_btns = QHBoxLayout()
        self._clear_cache_btn = QPushButton("Clear Cache")
        self._clear_cache_btn.clicked.connect(self._clear_cache)
        model_btns.addWidget(self._clear_cache_btn)
        self._download_btn = QPushButton("Re-download Model")
        self._download_btn.clicked.connect(self._model_manager.download_model)
        model_btns.addWidget(self._download_btn)
        model_btns.addStretch()
        model_layout.addLayout(model_btns)

        layout.addWidget(model_group)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        close_btn = QPushButton("Close")
        close_btn.setObjectName("primary")
        close_btn.clicked.connect(self._save_and_close)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

    def _connect_signals(self):
        self._lang_combo.currentIndexChanged.connect(self._on_language_changed)
        self._speed_slider.valueChanged.connect(
            lambda v: self._speed_label.setText(f"{v / 100:.1f}×")
        )
        self._model_manager.download_finished.connect(self._update_cache_info)
        self._model_manager.progress.connect(lambda p, m: None)

    def _populate(self):
        for code, name in LANGUAGES.items():
            self._lang_combo.addItem(name, code)
        idx = self._lang_combo.findData(config.language)
        if idx >= 0:
            self._lang_combo.setCurrentIndex(idx)

        # Populate all voices
        self._voice_combo.blockSignals(True)
        self._voice_combo.clear()
        for v in get_all_voices():
            self._voice_combo.addItem(get_voice_display_name(v), v)
        self._voice_combo.blockSignals(False)

        saved_voice = config.voice
        idx = self._voice_combo.findData(saved_voice)
        if idx >= 0:
            self._voice_combo.setCurrentIndex(idx)
        else:
            self._on_language_changed()

        self._speed_slider.setValue(int(config.speed * 100))
        self._theme_check.setChecked(config.theme == "dark")
        self._output_label.setText(config.output_dir)
        self._update_cache_info()

    def _on_language_changed(self):
        code = self._lang_combo.currentData()
        current_voice = self._voice_combo.currentData()
        
        # Smart default: select first voice of this language if current voice is mismatched
        if not current_voice or not current_voice.startswith(code):
            for i in range(self._voice_combo.count()):
                v = self._voice_combo.itemData(i)
                if v and v.startswith(code):
                    self._voice_combo.setCurrentIndex(i)
                    break

    def _browse_output(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Select Output Folder", config.output_dir
        )
        if folder:
            self._output_label.setText(folder)

    def _update_cache_info(self, *args):
        if self._model_manager.is_model_downloaded():
            size = self._model_manager.get_cache_size()
            self._cache_info.setText(f"Model cached ({size})")
        else:
            self._cache_info.setText("Model not downloaded")

    def _clear_cache(self):
        self._model_manager.clear_cache()
        self._update_cache_info()

    def _save_and_close(self):
        config.language = self._lang_combo.currentData()
        config.voice = self._voice_combo.currentData()
        config.speed = self._speed_slider.value() / 100.0
        config.theme = "dark" if self._theme_check.isChecked() else "light"
        config.output_dir = self._output_label.text()
        self.accept()
