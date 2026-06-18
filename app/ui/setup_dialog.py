import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from app.core.config import config
from app.core.model_manager import ModelManager
from app.core.voices import LANGUAGES, VOICE_INFO, VOICES

OUTPUT_FORMATS = [
    (".wav", "wav"),
    (".mp3", "mp3"),
    (".flac", "flac"),
    (".aiff", "aiff"),
]


def _voice_gender(voice: str) -> str:
    prefix = voice.split("_")[0]
    return "f" if len(prefix) >= 2 and prefix[1] == "f" else "m"


def _gender_label(g: str) -> str:
    return "Feminine" if g == "f" else "Masculine"


class SetupDialog(QDialog):
    def __init__(self, model_manager: ModelManager, parent=None):
        super().__init__(parent)
        self._model_manager = model_manager
        self._setup_ui()
        self._connect_signals()
        self._populate()
        self._on_voice_changed()

    def _setup_ui(self):
        self.setWindowTitle("Kokoro TTS — Setup")
        self.setFixedSize(500, 460)
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.WindowCloseButtonHint
        )

        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)

        content = QVBoxLayout()
        content.setContentsMargins(36, 28, 36, 12)
        content.setSpacing(10)

        title = QLabel("Choose Your Voice")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content.addWidget(title)

        subtitle = QLabel("Select a language group and pick a voice.")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        content.addWidget(subtitle)

        content.addWidget(self._section_header("Model"))

        self._lang_combo = self._make_combo()
        self._lang_label = self._add_row("Group", self._lang_combo, content)

        self._tone_combo = self._make_combo()
        self._tone_combo.setEnabled(False)
        self._tone_label = self._add_row("Tone", self._tone_combo, content)
        self._tone_label.setEnabled(False)

        self._voice_combo = self._make_combo()
        self._voice_combo.setEnabled(False)
        self._voice_label = self._add_row("Voice", self._voice_combo, content)
        self._voice_label.setEnabled(False)

        self._voice_info = QLabel("")
        self._voice_info.setObjectName("subtitle")
        self._voice_info.setWordWrap(True)
        content.addWidget(self._voice_info)

        content.addWidget(self._section_header("Output"))

        out_row = QHBoxLayout()
        out_label = QLabel("Folder")
        out_label.setObjectName("section")
        out_label.setFixedWidth(50)
        out_row.addWidget(out_label)
        self._output_edit = QLineEdit()
        self._output_edit.setText(os.path.abspath(config.output_dir))
        self._output_edit.setReadOnly(True)
        self._output_edit.setObjectName("outputPath")
        self._output_edit.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        out_row.addWidget(self._output_edit, 1)
        self._browse_btn = QPushButton("Browse")
        self._browse_btn.setObjectName("smallBtn")
        out_row.addWidget(self._browse_btn)
        content.addLayout(out_row)

        fmt_row = QHBoxLayout()
        fmt_label = QLabel("Format")
        fmt_label.setObjectName("section")
        fmt_label.setFixedWidth(50)
        fmt_row.addWidget(fmt_label)
        self._format_combo = self._make_combo()
        fmt_row.addWidget(self._format_combo, 1)
        content.addLayout(fmt_row)

        content.addSpacing(10)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)
        self._continue_btn = QPushButton("Continue")
        self._continue_btn.setObjectName("primary")
        self._continue_btn.setEnabled(False)
        btn_row.addStretch()
        btn_row.addWidget(self._continue_btn)
        content.addLayout(btn_row)

        main.addLayout(content)
        main.addStretch()
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

        self.setTabOrder(self._lang_combo, self._tone_combo)
        self.setTabOrder(self._tone_combo, self._voice_combo)
        self.setTabOrder(self._voice_combo, self._browse_btn)
        self.setTabOrder(self._browse_btn, self._format_combo)
        self.setTabOrder(self._format_combo, self._continue_btn)

    def _section_header(self, text: str) -> QLabel:
        lbl = QLabel(text.upper())
        lbl.setObjectName("sectionHeader")
        return lbl

    def _make_combo(self) -> QComboBox:
        c = QComboBox()
        c.setMinimumWidth(200)
        return c

    def _add_row(self, label: str, combo: QComboBox, layout: QVBoxLayout) -> QLabel:
        row = QHBoxLayout()
        lbl = QLabel(label)
        lbl.setObjectName("section")
        lbl.setFixedWidth(50)
        row.addWidget(lbl)
        row.addWidget(combo, 1)
        layout.addLayout(row)
        return lbl

    @staticmethod
    def _add_placeholder(combo: QComboBox, text: str):
        combo.addItem(text)
        model = combo.model()
        if model:
            model.item(combo.count() - 1).setEnabled(False)

    @staticmethod
    def _disable_item(combo: QComboBox, index: int):
        model = combo.model()
        if model:
            model.item(index).setEnabled(False)

    def _connect_signals(self):
        self._lang_combo.currentIndexChanged.connect(self._on_language_changed)
        self._tone_combo.currentIndexChanged.connect(self._on_tone_changed)
        self._voice_combo.currentIndexChanged.connect(self._on_voice_changed)
        self._continue_btn.clicked.connect(self._on_continue)
        self._browse_btn.clicked.connect(self._on_browse_output)

    def _on_browse_output(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder", self._output_edit.text())
        if folder:
            self._output_edit.setText(folder)

    def _populate(self):
        self._lang_combo.blockSignals(True)
        self._lang_combo.addItem("Select group…")
        self._disable_item(self._lang_combo, 0)
        for code, name in LANGUAGES.items():
            self._lang_combo.addItem(name, code)
        self._lang_combo.blockSignals(False)

        self._tone_combo.blockSignals(True)
        self._add_placeholder(self._tone_combo, "Select tone…")
        self._tone_combo.blockSignals(False)

        self._voice_combo.blockSignals(True)
        self._add_placeholder(self._voice_combo, "Select voice…")
        self._voice_combo.blockSignals(False)

        self._format_combo.blockSignals(True)
        for label, code in OUTPUT_FORMATS:
            self._format_combo.addItem(label, code)
        idx = self._format_combo.findData(config.output_format)
        if idx >= 0:
            self._format_combo.setCurrentIndex(idx)
        self._format_combo.blockSignals(False)

    def _on_language_changed(self):
        code = self._lang_combo.currentData()
        self._tone_combo.blockSignals(True)
        self._tone_combo.clear()
        self._add_placeholder(self._tone_combo, "Select tone…")
        if code:
            genders = set()
            for v in VOICES.get(code, []):
                genders.add(_voice_gender(v))
            for g in sorted(genders):
                self._tone_combo.addItem(_gender_label(g), g)
            self._tone_combo.setEnabled(True)
            self._tone_label.setEnabled(True)
        else:
            self._tone_combo.setEnabled(False)
            self._tone_label.setEnabled(False)
        self._tone_combo.blockSignals(False)

        self._voice_combo.blockSignals(True)
        self._voice_combo.clear()
        self._add_placeholder(self._voice_combo, "Select voice…")
        self._voice_combo.setEnabled(False)
        self._voice_label.setEnabled(False)
        self._voice_combo.blockSignals(False)

        self._voice_info.setText("")
        self._continue_btn.setEnabled(False)

    def _on_tone_changed(self):
        tone = self._tone_combo.currentData()
        lang = self._lang_combo.currentData()
        self._voice_combo.blockSignals(True)
        self._voice_combo.clear()
        self._add_placeholder(self._voice_combo, "Select voice…")
        if tone and lang:
            for v in VOICES.get(lang, []):
                if _voice_gender(v) == tone:
                    self._voice_combo.addItem(v, v)
            self._voice_combo.setEnabled(True)
            self._voice_label.setEnabled(True)
        else:
            self._voice_combo.setEnabled(False)
            self._voice_label.setEnabled(False)
        self._voice_combo.blockSignals(False)

        self._voice_info.setText("")
        self._continue_btn.setEnabled(False)

    def _on_voice_changed(self):
        voice = self._voice_combo.currentData()
        if voice:
            info = VOICE_INFO.get(voice, "")
            gender = _voice_gender(voice)
            self._voice_info.setText(f"{_gender_label(gender)} · {info}" if info else _gender_label(gender))
        else:
            self._voice_info.setText("")
        self._continue_btn.setEnabled(bool(voice))

    def _on_continue(self):
        voice = self._voice_combo.currentData()
        if not self._model_manager.ensure_voice(voice):
            self._voice_info.setText("Failed to download voice file. Try again.")
            return
        config.language = self._lang_combo.currentData()
        config.voice = voice
        config.speed = 1.0
        config.output_dir = self._output_edit.text()
        config.output_format = self._format_combo.currentData()
        config.first_run = False
        self.accept()
