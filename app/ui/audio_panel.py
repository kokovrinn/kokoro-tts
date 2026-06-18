import contextlib
import io
import math
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf
from PySide6.QtCore import QPointF, Qt, QUrl
from PySide6.QtGui import QColor, QDesktopServices, QPainter, QPen
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from app.core.config import config
from app.ui.icons import (
    icon_folder_open,
    icon_pause,
    icon_play,
    icon_trash,
    icon_volume_high,
)


class WaveformWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._audio = None
        self._progress = 0.0
        self.setFixedHeight(60)

    def set_audio(self, audio: np.ndarray | None):
        self._audio = audio
        self._progress = 0.0
        self.update()

    def set_progress(self, progress: float):
        self._progress = progress
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        m = 8

        is_dark = config.theme == "dark"

        bg_color = QColor("#16161a") if is_dark else QColor("#ffffff")
        border_color = QColor(255, 255, 255, 12) if is_dark else QColor(0, 0, 0, 20)

        painter.setPen(QPen(border_color, 1))
        painter.setBrush(bg_color)
        painter.drawRoundedRect(1, 1, w - 2, h - 2, 8, 8)

        if self._audio is None or len(self._audio) == 0:
            muted = QColor(255, 255, 255, 30) if is_dark else QColor(0, 0, 0, 20)
            pen = QPen(muted, 2)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            bar_w = 2
            bar_gap = 2
            bar_step = bar_w + bar_gap
            usable_w = w - m * 2
            num = min(40, max(20, usable_w // bar_step))
            total_w = num * bar_step
            start_x = (w - total_w) // 2
            mid = h // 2
            scale = (h - m * 2) // 2

            for i in range(num):
                px = start_x + i * bar_step + bar_w / 2.0
                t = i / num * math.pi * 8
                envelope = 0.3 + 0.7 * max(0, math.sin(t * 0.5)) ** 2
                noise = ((i * 7919 + 1) % 13) / 13.0
                raw = max(1, int(envelope * (3 + noise * 18) * scale / 22))
                half_h = min(raw, scale)
                painter.drawLine(QPointF(px, mid - half_h), QPointF(px, mid + half_h))
            return

        audio = np.asarray(self._audio, dtype=np.float64).flatten()
        n = len(audio)

        bar_w = 2
        bar_gap = 1
        bar_step = bar_w + bar_gap

        usable_w = w - m * 2
        num_bars = max(1, usable_w // bar_step)
        chunk_size = max(1, n // num_bars)

        mid = h // 2
        scale = (h - m * 2) // 2

        played_color = QColor("#ffffff") if is_dark else QColor("#007aff")
        unplayed_color = QColor(255, 255, 255, 30) if is_dark else QColor(0, 0, 0, 25)

        for i in range(num_bars):
            px = m + i * bar_step + bar_w / 2.0
            idx = i * chunk_size
            end = min(idx + chunk_size, n)
            chunk = audio[idx:end]

            if len(chunk) == 0:
                y_t = mid - 1
                y_b = mid + 1
            else:
                amp = float(np.max(np.abs(chunk)))
                half_h = max(1, int(amp * scale))
                y_t = mid - half_h
                y_b = mid + half_h

            y_t = max(m, min(h - m, y_t))
            y_b = max(m, min(h - m, y_b))

            bar_progress = (i / num_bars) * 100.0
            color = played_color if bar_progress <= self._progress else unplayed_color

            pen = QPen(color, bar_w)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
            painter.drawLine(QPointF(px, y_t), QPointF(px, y_b))


class AudioPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._audio = None
        self._current_file: str | None = None
        self._saved_path: str | None = None
        self._player = QMediaPlayer()
        self._audio_output = QAudioOutput()
        self._player.setAudioOutput(self._audio_output)
        self._player.positionChanged.connect(self._on_position_changed)
        self._player.playbackStateChanged.connect(self._on_state_changed)
        self._player.durationChanged.connect(self._on_duration_changed)
        self._duration_ms = 0
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        title = QLabel("AUDIO OUTPUT")
        title.setObjectName("sectionHeader")
        layout.addWidget(title)

        self._waveform = WaveformWidget()
        layout.addWidget(self._waveform)

        seek_row = QHBoxLayout()
        seek_row.setSpacing(8)
        self._seek_slider = QSlider(Qt.Orientation.Horizontal)
        self._seek_slider.setRange(0, 1000)
        self._seek_slider.sliderMoved.connect(self._on_seek)
        self._seek_slider.setEnabled(False)
        seek_row.addWidget(self._seek_slider, 1)
        self._duration_label = QLabel("00:00 / 00:00")
        self._duration_label.setObjectName("subtitle")
        seek_row.addWidget(self._duration_label)
        layout.addLayout(seek_row)

        controls = QHBoxLayout()
        controls.setSpacing(8)

        self._play_btn = QPushButton()
        self._play_btn.setIcon(icon_play())
        self._play_btn.setObjectName("playCircleBtn")
        self._play_btn.setToolTip("Play / Pause")
        self._play_btn.clicked.connect(self._toggle_play)
        self._play_btn.setEnabled(False)
        controls.addWidget(self._play_btn)

        self._reveal_btn = QPushButton("Reveal")
        self._reveal_btn.setIcon(icon_folder_open())
        self._reveal_btn.setObjectName("smallBtn")
        self._reveal_btn.setToolTip("Show in Finder")
        self._reveal_btn.clicked.connect(self._open_location)
        self._reveal_btn.setEnabled(False)
        controls.addWidget(self._reveal_btn)

        self._discard_btn = QPushButton("Discard")
        self._discard_btn.setIcon(icon_trash())
        self._discard_btn.setObjectName("smallBtn")
        self._discard_btn.setToolTip("Remove generated audio")
        self._discard_btn.clicked.connect(self._discard_audio)
        self._discard_btn.setEnabled(False)
        controls.addWidget(self._discard_btn)

        controls.addStretch()

        vol_icon = QLabel()
        vol_icon.setPixmap(icon_volume_high().pixmap(16, 16))
        controls.addWidget(vol_icon)

        self._volume_slider = QSlider(Qt.Orientation.Horizontal)
        self._volume_slider.setRange(0, 100)
        self._volume_slider.setValue(80)
        self._volume_slider.setFixedWidth(80)
        self._volume_slider.valueChanged.connect(self._on_volume_changed)
        controls.addWidget(self._volume_slider)
        layout.addLayout(controls)

    def set_audio(self, audio, file_path: str | None = None):
        self._audio = audio
        self._saved_path = file_path
        self._player.stop()
        self._save_temp()
        self._waveform.set_audio(audio.numpy() if audio is not None else None)
        enabled = audio is not None
        self._play_btn.setEnabled(enabled)
        self._reveal_btn.setEnabled(enabled)
        self._discard_btn.setEnabled(enabled)
        self._seek_slider.setEnabled(enabled)
        self._seek_slider.setValue(0)

    def _save_temp(self):
        if self._current_file:
            try:
                Path(self._current_file).unlink(missing_ok=True)
            except OSError:
                pass
            self._current_file = None

        if self._audio is None:
            return

        audio_np = self._audio.numpy()
        if audio_np.ndim > 1:
            audio_np = audio_np.squeeze()
        audio_int16 = (audio_np * 32767).astype("int16")

        tmp = tempfile.NamedTemporaryFile(
            suffix=".wav", delete=False, dir=tempfile.gettempdir()
        )
        sf.write(tmp.name, audio_int16, 24000)
        self._current_file = tmp.name
        with contextlib.redirect_stderr(io.StringIO()):
            self._player.setSource(QUrl.fromLocalFile(self._current_file))

    def _toggle_play(self):
        if self._player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self._player.pause()
        else:
            self._player.play()

    def _open_location(self):
        if self._saved_path:
            import os
            folder = os.path.dirname(self._saved_path)
            QDesktopServices.openUrl(QUrl.fromLocalFile(folder))

    def _discard_audio(self):
        if self._saved_path:
            try:
                Path(self._saved_path).unlink(missing_ok=True)
            except OSError:
                pass
            self._saved_path = None
        self.set_audio(None)

    def _on_seek(self, value):
        if self._duration_ms > 0:
            pos = int(value / 1000.0 * self._duration_ms)
            self._player.setPosition(pos)

    def _on_position_changed(self, position):
        if self._duration_ms > 0:
            progress = (position / self._duration_ms) * 100.0
            self._waveform.set_progress(progress)
            self._seek_slider.blockSignals(True)
            self._seek_slider.setValue(int(progress * 10))
            self._seek_slider.blockSignals(False)
            self._duration_label.setText(
                f"{self._fmt_time(position)} / {self._fmt_time(self._duration_ms)}"
            )

    def _on_duration_changed(self, duration):
        self._duration_ms = duration

    def _on_state_changed(self, state):
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self._play_btn.setIcon(icon_pause())
        else:
            self._play_btn.setIcon(icon_play())

    def _on_volume_changed(self, value):
        self._audio_output.setVolume(value / 100.0)

    @staticmethod
    def _fmt_time(ms: int) -> str:
        s = ms // 1000
        m = s // 60
        s = s % 60
        return f"{m:02d}:{s:02d}"

    def cleanup(self):
        self._player.stop()
        if self._current_file:
            try:
                Path(self._current_file).unlink(missing_ok=True)
            except OSError:
                pass
            self._current_file = None
