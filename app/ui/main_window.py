import threading

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame, QApplication, QComboBox, QSlider,
    QLineEdit, QFileDialog, QDialog, QListWidget, QListWidgetItem,
    QDialogButtonBox, QProgressBar,
)

from app.core.config import config
from app.core.model_manager import ModelManager
from app.core.session_manager import SessionManager
from app.core.tts_engine import TTSEngine
from app.core.voices import LANGUAGES, VOICES, VOICE_INFO
from app.ui.audio_panel import AudioPanel
from app.ui.icons import icon_play, icon_pencil, icon_plus, icon_search, icon_trash
from app.ui.settings_dialog import SettingsDialog
from app.ui.styles import get_style
from app.ui.text_panel import TextPanel


def _voice_gender(voice: str) -> str:
    prefix = voice.split("_")[0]
    return "f" if len(prefix) >= 2 and prefix[1] == "f" else "m"

def _gender_label(g: str) -> str:
    return "Feminine" if g == "f" else "Masculine"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._model_manager = ModelManager(self)
        self._tts = TTSEngine(self)
        self._sessions = SessionManager()
        if not self._sessions.current:
            self._sessions.create("Initial session")
        self._save_timer = QTimer()
        self._save_timer.setSingleShot(True)
        self._save_timer.setInterval(500)
        self._save_timer.timeout.connect(self._flush_text)
        self._setup_ui()
        self._connect_signals()
        self._apply_theme()

    def _setup_ui(self):
        self.setWindowTitle("Kokoro TTS")
        self.setMinimumSize(960, 600)
        self.resize(1100, 680)

        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(16, 16, 16, 0)
        main_layout.setSpacing(20)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(6)

        session_bar = QHBoxLayout()
        session_bar.setSpacing(6)

        self._session_name = QLineEdit()
        self._session_name.setReadOnly(True)
        self._session_name.setObjectName("sessionName")
        self._session_name.editingFinished.connect(self._save_session_name)
        session_bar.addWidget(self._session_name, 1)

        self._session_edit_btn = QPushButton()
        self._session_edit_btn.setIcon(icon_pencil())
        self._session_edit_btn.setObjectName("iconBtn")
        self._session_edit_btn.setToolTip("Rename session")
        self._session_edit_btn.clicked.connect(self._on_rename_session)
        session_bar.addWidget(self._session_edit_btn)

        self._session_clear_btn = QPushButton()
        self._session_clear_btn.setIcon(icon_trash())
        self._session_clear_btn.setObjectName("iconBtn")
        self._session_clear_btn.setToolTip("Delete session")
        self._session_clear_btn.clicked.connect(self._on_delete_session)
        session_bar.addWidget(self._session_clear_btn)

        self._session_new_btn = QPushButton()
        self._session_new_btn.setIcon(icon_plus())
        self._session_new_btn.setObjectName("iconBtn")
        self._session_new_btn.setToolTip("New session")
        self._session_new_btn.clicked.connect(self._on_new_session)
        session_bar.addWidget(self._session_new_btn)

        self._session_list_btn = QPushButton()
        self._session_list_btn.setIcon(icon_search())
        self._session_list_btn.setObjectName("iconBtn")
        self._session_list_btn.setToolTip("All sessions")
        self._session_list_btn.clicked.connect(self._on_list_sessions)
        session_bar.addWidget(self._session_list_btn)

        left_layout.addLayout(session_bar)

        self._text_panel = TextPanel()
        left_layout.addWidget(self._text_panel, 1)

        main_layout.addWidget(left_panel, 6)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(12)

        voice_title = QLabel("VOICE OPTIONS")
        voice_title.setObjectName("sectionHeader")
        right_layout.addWidget(voice_title)

        def add_row(label, widget):
            row = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setObjectName("section")
            lbl.setFixedWidth(50)
            row.addWidget(lbl)
            row.addWidget(widget, 1)
            right_layout.addLayout(row)

        self._lang_combo = QComboBox()
        add_row("Language", self._lang_combo)

        self._tone_combo = QComboBox()
        self._tone_combo.setEnabled(False)
        add_row("Tone", self._tone_combo)

        self._voice_combo = QComboBox()
        self._voice_combo.setEnabled(False)
        add_row("Voice", self._voice_combo)

        self._voice_info = QLabel("")
        self._voice_info.setObjectName("subtitle")
        self._voice_info.setWordWrap(True)
        self._voice_info.setVisible(False)
        right_layout.addWidget(self._voice_info)

        speed_row = QHBoxLayout()
        speed_row.setSpacing(8)
        speed_lbl = QLabel("Speed")
        speed_lbl.setObjectName("section")
        speed_lbl.setFixedWidth(50)
        speed_row.addWidget(speed_lbl)
        self._speed_label = QLabel("1.0×")
        self._speed_label.setObjectName("subtitle")
        speed_row.addStretch()
        speed_row.addWidget(self._speed_label)
        right_layout.addLayout(speed_row)

        self._speed_slider = QSlider(Qt.Orientation.Horizontal)
        self._speed_slider.setRange(50, 200)
        right_layout.addWidget(self._speed_slider)

        out_title = QLabel("OUTPUT")
        out_title.setObjectName("sectionHeader")
        right_layout.addWidget(out_title)

        out_row = QHBoxLayout()
        out_lbl = QLabel("Folder")
        out_lbl.setObjectName("section")
        out_lbl.setFixedWidth(50)
        out_row.addWidget(out_lbl)
        self._output_edit = QLineEdit()
        self._output_edit.setText(config.output_dir)
        self._output_edit.setReadOnly(True)
        self._output_edit.setObjectName("outputPath")
        self._output_edit.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        out_row.addWidget(self._output_edit, 1)
        self._browse_btn = QPushButton("Browse")
        self._browse_btn.setObjectName("smallBtn")
        self._browse_btn.clicked.connect(self._on_browse_output)
        out_row.addWidget(self._browse_btn)
        right_layout.addLayout(out_row)

        fmt_row = QHBoxLayout()
        fmt_lbl = QLabel("Format")
        fmt_lbl.setObjectName("section")
        fmt_lbl.setFixedWidth(50)
        fmt_row.addWidget(fmt_lbl)
        self._format_combo = QComboBox()
        for label, code in [(".wav", "wav"), (".mp3", "mp3"), (".flac", "flac"), (".aiff", "aiff")]:
            self._format_combo.addItem(label, code)
        idx = self._format_combo.findData(config.output_format)
        if idx >= 0:
            self._format_combo.setCurrentIndex(idx)
        self._format_combo.currentIndexChanged.connect(self._on_format_changed)
        fmt_row.addWidget(self._format_combo, 1)
        right_layout.addLayout(fmt_row)

        save_info = QLabel("Auto-saves to configured path. Repeated text overwrites.")
        save_info.setObjectName("subtitle")
        save_info.setWordWrap(True)
        right_layout.addWidget(save_info)

        right_layout.addSpacing(4)

        self._generate_btn = QPushButton("  Generate")
        self._generate_btn.setIcon(icon_play("#ffffff"))
        self._generate_btn.setObjectName("generateBtn")
        self._generate_btn.setMinimumHeight(44)
        self._generate_btn.clicked.connect(self._on_transform)
        right_layout.addWidget(self._generate_btn)

        self._synth_progress = QProgressBar()
        self._synth_progress.setFixedHeight(4)
        self._synth_progress.setTextVisible(False)
        self._synth_progress.setRange(0, 0)
        self._synth_progress.setVisible(False)
        right_layout.addWidget(self._synth_progress)

        self._audio_panel = AudioPanel()
        right_layout.addWidget(self._audio_panel)

        right_layout.addStretch()

        main_layout.addWidget(right_panel, 5)

        root.addLayout(main_layout, 1)

        root.addSpacing(10)

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
        self._status_text = QLabel("Model ready")
        self._status_text.setObjectName("footerStatus")
        fl.addWidget(self._status_text)
        fl.addStretch()
        flabel = QLabel("made with ♥ by kokovrinn")
        flabel.setObjectName("footer")
        flabel.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        fl.addWidget(flabel)
        root.addWidget(footer_frame)

        for code, name in LANGUAGES.items():
            self._lang_combo.addItem(name, code)

        self._load_config_to_ui()
        self._setup_menu()
        self._load_current_session()

    def _load_config_to_ui(self):
        self._lang_combo.blockSignals(True)
        self._tone_combo.blockSignals(True)
        self._voice_combo.blockSignals(True)
        self._speed_slider.blockSignals(True)

        idx = self._lang_combo.findData(config.language)
        if idx >= 0:
            self._lang_combo.setCurrentIndex(idx)

        self._populate_tones(config.language)

        gender = _voice_gender(config.voice) if config.voice else None
        if gender:
            idx = self._tone_combo.findData(gender)
            if idx >= 0:
                self._tone_combo.setCurrentIndex(idx)

        self._populate_voices(config.language, gender)

        if config.voice:
            idx = self._voice_combo.findData(config.voice)
            if idx >= 0:
                self._voice_combo.setCurrentIndex(idx)

        self._speed_slider.setValue(int(config.speed * 100))
        self._speed_label.setText(f"{config.speed:.1f}×")

        self._lang_combo.blockSignals(False)
        self._tone_combo.blockSignals(False)
        self._voice_combo.blockSignals(False)
        self._speed_slider.blockSignals(False)

        self._update_voice_info()

    def _populate_tones(self, lang_code):
        self._tone_combo.clear()
        if lang_code and lang_code in VOICES:
            genders = set()
            for v in VOICES[lang_code]:
                genders.add(_voice_gender(v))
            for g in sorted(genders):
                self._tone_combo.addItem(_gender_label(g), g)
            self._tone_combo.setEnabled(True)
        else:
            self._tone_combo.setEnabled(False)

    def _populate_voices(self, lang_code, gender):
        self._voice_combo.clear()
        if gender and lang_code and lang_code in VOICES:
            for v in VOICES[lang_code]:
                if _voice_gender(v) == gender:
                    self._voice_combo.addItem(v, v)
            self._voice_combo.setEnabled(True)
        else:
            self._voice_combo.setEnabled(False)

    def _update_voice_info(self):
        voice = self._voice_combo.currentData()
        if voice and voice in VOICE_INFO:
            info = VOICE_INFO[voice]
            gender = _voice_gender(voice)
            self._voice_info.setText(f"{_gender_label(gender)} · {info}")
            self._voice_info.setVisible(True)
        else:
            self._voice_info.setVisible(False)

    def _setup_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&File")
        file_menu.addSeparator()

        quit_action = QAction("Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        edit_menu = menubar.addMenu("&Edit")

        settings_action = QAction("Settings…", self)
        settings_action.setShortcut("Ctrl+,")
        settings_action.triggered.connect(self._open_settings)
        edit_menu.addAction(settings_action)

        help_menu = menubar.addMenu("&Help")
        about_action = QAction("About Kokoro TTS", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _connect_signals(self):
        self._lang_combo.currentIndexChanged.connect(self._on_language_changed)
        self._tone_combo.currentIndexChanged.connect(self._on_tone_changed)
        self._voice_combo.currentIndexChanged.connect(self._on_voice_changed)
        self._speed_slider.valueChanged.connect(self._on_speed_changed)
        self._tts.synthesis_started.connect(self._on_synthesis_started)
        self._tts.synthesis_progress.connect(self._on_synthesis_progress)
        self._tts.synthesis_finished.connect(self._on_synthesis_finished)
        self._tts.synthesis_error.connect(self._on_synthesis_error)
        self._model_manager.model_ready.connect(self._on_model_ready)
        self._text_panel.text_changed.connect(self._on_text_changed)
        self._text_panel.text_extracted.connect(self._on_text_imported)
        self._audio_panel._discard_btn.clicked.connect(self._on_audio_discarded)

    def _apply_theme(self):
        QApplication.instance().setStyleSheet(get_style(config.theme))

    def _on_language_changed(self):
        code = self._lang_combo.currentData()
        config.language = code

        self._tone_combo.blockSignals(True)
        self._voice_combo.blockSignals(True)

        self._populate_tones(code)

        gender = None
        if code and code in VOICES:
            first = VOICES[code][0]
            gender = _voice_gender(first)

        if gender:
            idx = self._tone_combo.findData(gender)
            if idx >= 0:
                self._tone_combo.setCurrentIndex(idx)

        self._populate_voices(code, gender)

        if gender and code and code in VOICES:
            for v in VOICES[code]:
                if _voice_gender(v) == gender:
                    idx = self._voice_combo.findData(v)
                    if idx >= 0:
                        self._voice_combo.setCurrentIndex(idx)
                        config.voice = v
                    break

        self._tone_combo.blockSignals(False)
        self._voice_combo.blockSignals(False)
        self._update_voice_info()
        self._save_voice_to_session()

    def _on_tone_changed(self):
        gender = self._tone_combo.currentData()
        lang = self._lang_combo.currentData()

        self._voice_combo.blockSignals(True)
        self._populate_voices(lang, gender)
        self._voice_combo.blockSignals(False)

        if gender and lang and lang in VOICES:
            for v in VOICES[lang]:
                if _voice_gender(v) == gender:
                    idx = self._voice_combo.findData(v)
                    if idx >= 0:
                        self._voice_combo.setCurrentIndex(idx)
                        config.voice = v
                    break

        self._update_voice_info()
        self._save_voice_to_session()

    def _on_voice_changed(self):
        voice = self._voice_combo.currentData()
        if voice:
            config.voice = voice
        self._update_voice_info()
        self._save_voice_to_session()

    def _on_speed_changed(self, value):
        speed = value / 100.0
        config.speed = speed
        self._speed_label.setText(f"{speed:.1f}×")
        self._save_voice_to_session()

    def _on_browse_output(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder", self._output_edit.text())
        if folder:
            self._output_edit.setText(folder)
            config.output_dir = folder

    def _on_format_changed(self):
        fmt = self._format_combo.currentData()
        if fmt:
            config.output_format = fmt

    def _on_transform(self):
        text = self._text_panel.text().strip()
        if not text:
            self._status_text.setText("Please enter some text")
            return

        if not self._model_manager.is_model_downloaded():
            self._status_text.setText("Model not downloaded. Open Settings to download.")
            return

        voice = self._voice_combo.currentData()
        lang = self._lang_combo.currentData()
        speed = self._speed_slider.value() / 100.0

        thread = threading.Thread(
            target=self._tts.synthesize,
            args=(text, voice, speed, lang),
            daemon=True,
        )
        thread.start()

    def _on_synthesis_started(self):
        self._generate_btn.setEnabled(False)
        self._synth_progress.setVisible(True)
        self._status_text.setText("Converting text to speech…")

    def _on_synthesis_progress(self, message: str):
        self._status_text.setText(message)

    def _on_synthesis_finished(self, text: str, audio):
        import os
        import time
        import re
        import soundfile as sf

        self._synth_progress.setVisible(False)

        session = self._sessions.current
        safe_name = re.sub(r"[^a-z0-9]+", "_", session["name"].lower()).strip("_") if session else "output"

        os.makedirs(config.output_dir, exist_ok=True)
        output_path = os.path.join(
            config.output_dir,
            f"{safe_name}_{int(time.time())}.wav"
        )
        audio_np = audio.numpy()
        if audio_np.ndim > 1:
            audio_np = audio_np.squeeze()
        audio_int16 = (audio_np * 32767).astype("int16")
        sf.write(output_path, audio_int16, 24000)

        self._audio_panel.set_audio(audio, output_path)

        if self._sessions.current_id:
            self._sessions.update_audio_path(self._sessions.current_id, output_path)

        self._generate_btn.setEnabled(True)
        self._status_text.setText(f"Saved to {output_path}")

    def _on_synthesis_error(self, error: str):
        self._synth_progress.setVisible(False)
        self._generate_btn.setEnabled(True)
        self._status_text.setText(f"Error: {error}")

    def _on_model_ready(self):
        self._status_text.setText("Model ready")

    def _on_audio_discarded(self):
        if self._sessions.current_id:
            self._sessions.update_audio_path(self._sessions.current_id, None)

    def _open_settings(self):
        prev_theme = config.theme
        dialog = SettingsDialog(self._model_manager, self)
        if dialog.exec() == SettingsDialog.DialogCode.Accepted:
            if config.theme != prev_theme:
                self._apply_theme()
            self._load_config_to_ui()

    def _show_about(self):
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.about(
            self, "About Kokoro TTS",
            "<h3>Kokoro TTS</h3>"
            "<p>A modern text-to-speech application.</p>"
            "<p>Powered by <b>Kokoro v0.9.4</b> — an 82M-parameter "
            "neural TTS model.</p>"
            "<p>Models by <b>hexgrad</b> on HuggingFace Hub.</p>"
        )

    def _load_current_session(self):
        s = self._sessions.current
        if s:
            self._session_name.setText(s["name"])
            self._text_panel.set_text(s.get("text", ""))
            config.language = s.get("language", "a")
            config.voice = s.get("voice", "af_heart")
            config.speed = s.get("speed", 1.0)
            self._restore_audio(s)

    def _on_text_changed(self, text: str):
        self._save_timer.start()

    def _on_text_imported(self, text: str):
        if text and self._sessions.current_id:
            self._sessions.update_text(self._sessions.current_id, text)
            self._save_timer.stop()

    def _flush_text(self):
        if self._sessions.current_id:
            actual = self._text_panel.text()
            if actual:
                self._sessions.update_text(self._sessions.current_id, actual)

    def _on_rename_session(self):
        if self._session_name.isReadOnly():
            self._session_name.setReadOnly(False)
            self._session_name.setFocus()
            self._session_name.selectAll()
        else:
            self._save_session_name()

    def _save_session_name(self):
        name = self._session_name.text().strip()
        if name and self._sessions.current_id:
            self._sessions.rename(self._sessions.current_id, name)
        else:
            s = self._sessions.current
            if s:
                self._session_name.setText(s["name"])
        self._session_name.setReadOnly(True)
        self._session_name.clearFocus()

    def _on_delete_session(self):
        from PySide6.QtWidgets import QMessageBox
        sessions = self._sessions.all
        if len(sessions) <= 1:
            reply = QMessageBox(
                QMessageBox.Icon.Warning,
                "Reset Session",
                "This is your only session.\n\n"
                "Reset it to a blank state?"
                "\n\nGenerated audio files will be kept.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                self,
            )
            reply.setStyleSheet(get_style(config.theme))
            if reply.exec() != QMessageBox.StandardButton.Yes:
                return
            self._text_panel.set_text("")
            if self._sessions.current_id:
                self._sessions.clear_text(self._sessions.current_id)
                self._sessions.rename(self._sessions.current_id, "Initial session")
                self._sessions.update_voice_settings(
                    self._sessions.current_id, "a", "af_heart", 1.0,
                )
                self._sessions.update_audio_path(self._sessions.current_id, None)
            self._session_name.setText("Initial session")
            config.language = "a"
            config.voice = "af_heart"
            config.speed = 1.0
            self._load_config_to_ui()
            return

        reply = QMessageBox(
            QMessageBox.Icon.Warning,
            "Delete Session",
            "Are you sure you want to delete this session?\n\n"
            "Only session data will be removed. "
            "Generated audio files will be kept.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            self,
        )
        reply.setStyleSheet(get_style(config.theme))
        if reply.exec() != QMessageBox.StandardButton.Yes:
            return

        sid = self._sessions.current_id
        if sid:
            self._sessions.delete(sid)
            s = self._sessions.current
            if s:
                self._load_session(s["id"])
            else:
                new_id = self._sessions.create("Initial session")
                self._load_session(new_id)

    def _on_new_session(self):
        dlg = _NewSessionDialog(self._sessions, self)
        if dlg.exec() == QDialog.DialogCode.Accepted and dlg.name:
            sid = self._sessions.create(
                dlg.name, config.language, config.voice, config.speed
            )
            self._load_session(sid)

    def _on_list_sessions(self):
        dlg = _SessionListDialog(self._sessions, self)
        if dlg.exec() == QDialog.DialogCode.Accepted and dlg.selected_id:
            self._load_session(dlg.selected_id)

    def _load_session(self, sid: str):
        self._sessions.switch_to(sid)
        s = self._sessions.current
        if s:
            self._session_name.setText(s["name"])
            self._text_panel.set_text(s.get("text", ""))
            config.language = s.get("language", "a")
            config.voice = s.get("voice", "af_heart")
            config.speed = s.get("speed", 1.0)
            self._load_config_to_ui()
            self._restore_audio(s)

    def _restore_audio(self, s: dict):
        import os
        import soundfile as sf
        audio_path = s.get("audio_path")
        if audio_path and os.path.exists(audio_path):
            try:
                audio_np, sr = sf.read(audio_path, dtype="float32")
                import torch
                audio_tensor = torch.from_numpy(audio_np).float()
                self._audio_panel.set_audio(audio_tensor, audio_path)
                return
            except Exception:
                pass
        self._audio_panel.set_audio(None)

    def _save_voice_to_session(self):
        if self._sessions.current_id:
            self._sessions.update_voice_settings(
                self._sessions.current_id,
                config.language, config.voice, config.speed,
            )

    def closeEvent(self, event):
        self._audio_panel.cleanup()
        super().closeEvent(event)


class _NewSessionDialog(QDialog):
    def __init__(self, sessions: SessionManager, parent=None):
        super().__init__(parent)
        self._sessions = sessions
        self.setWindowTitle("New Session")
        self.setFixedSize(340, 160)
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.WindowCloseButtonHint
        )
        self.name = ""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 16, 24, 12)
        layout.setSpacing(6)

        lbl = QLabel("Enter a name for the new session:")
        lbl.setWordWrap(True)
        layout.addWidget(lbl)

        self._edit = QLineEdit()
        self._edit.setPlaceholderText("Session name")
        self._edit.setFocus()
        self._edit.returnPressed.connect(self._accept)
        layout.addWidget(self._edit)

        self._error = QLabel("")
        self._error.setObjectName("subtitle")
        self._error.setVisible(False)
        self._error.setStyleSheet("color: #ef4444; padding-top: 2px;")
        layout.addWidget(self._error)

        layout.addSpacing(6)

        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self._accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def _accept(self):
        name = self._edit.text().strip()
        if not name:
            return
        for s in self._sessions.all:
            if s["name"].lower() == name.lower():
                self._error.setText("A session with this name already exists.")
                self._error.setVisible(True)
                return
        self.name = name
        self.accept()


class _SessionListDialog(QDialog):
    def __init__(self, sessions: SessionManager, parent=None):
        super().__init__(parent)
        self._sessions = sessions
        self.selected_id: str | None = None

        self.setWindowTitle("Sessions")
        self.setFixedSize(420, 480)
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.WindowCloseButtonHint
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 12)
        layout.setSpacing(10)

        self._search = QLineEdit()
        self._search.setPlaceholderText("Search sessions…")
        self._search.textChanged.connect(self._filter)
        layout.addWidget(self._search)

        self._list = QListWidget()
        self._list.setSpacing(4)
        self._list.itemClicked.connect(self._on_click)
        self._list.itemDoubleClicked.connect(self._on_select)
        layout.addWidget(self._list, 1)

        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self._on_select)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

        self._populate()

    def _on_click(self, item):
        for i in range(self._list.count()):
            self._list.item(i).setSelected(i == self._list.row(item))

    def _populate(self):
        self._list.clear()
        current = self._sessions.current_id
        for s in self._sessions.all:
            sid = s["id"]
            is_current = sid == current

            widget = QWidget()
            row = QHBoxLayout(widget)
            row.setContentsMargins(10, 8, 10, 8)
            row.setSpacing(10)

            left = QVBoxLayout()
            left.setSpacing(2)

            name_lbl = QLabel(s["name"])
            name_lbl.setObjectName("sessionItemName")
            left.addWidget(name_lbl)

            preview = s.get("text", "")
            date_str = self._fmt_date(s["updated_at"])
            if preview:
                preview = preview[:55] + ("…" if len(preview) > 55 else "")
                sub = QLabel(f"{date_str} — {preview}")
            else:
                sub = QLabel(f"{date_str} — Empty")
            sub.setObjectName("sessionItemSub")
            left.addWidget(sub)

            row.addLayout(left, 1)

            if is_current:
                dot = QLabel("●")
                dot.setObjectName("sessionItemDot")
                row.addWidget(dot)

            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, sid)
            item.setSizeHint(widget.sizeHint())
            self._list.addItem(item)
            self._list.setItemWidget(item, widget)

            if is_current:
                self._list.setCurrentItem(item)

    @staticmethod
    def _fmt_date(iso: str) -> str:
        from datetime import datetime, timezone
        try:
            dt = datetime.fromisoformat(iso)
            now = datetime.now(timezone.utc)
            diff = (now - dt).days
            if diff == 0:
                return "Today"
            elif diff == 1:
                return "Yesterday"
            else:
                return dt.strftime("%d/%m")
        except Exception:
            return ""

    def _filter(self, text: str):
        lower = text.lower()
        for i in range(self._list.count()):
            item = self._list.item(i)
            sid = item.data(Qt.ItemDataRole.UserRole)
            s = self._sessions.get(sid)
            matches = s and (
                lower in s["name"].lower()
                or lower in s.get("text", "").lower()
            )
            item.setHidden(not matches)

    def _on_select(self):
        item = self._list.currentItem()
        if item:
            self.selected_id = item.data(Qt.ItemDataRole.UserRole)
            self.accept()
