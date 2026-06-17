"""Modern icons powered by Phosphor Icons (SVG)."""

import os

from PySide6.QtCore import Qt, QSize, QByteArray
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QApplication

_ICONS_DIR = os.path.join(os.path.dirname(__file__), "icons")

_svg_cache: dict[str, QPixmap] = {}


def _is_dark():
    app = QApplication.instance()
    if app is None:
        return True
    w = app.activeWindow()
    if w is None:
        return True
    from app.core.config import config
    return config.theme == "dark"


def icon_color():
    return "#f5f5f7" if _is_dark() else "#1d1d1f"


def _load_svg(name: str, size: int, color: str) -> QPixmap:
    cache_key = f"{name}:{size}:{color}"
    if cache_key in _svg_cache:
        return _svg_cache[cache_key]

    path = os.path.join(_ICONS_DIR, f"{name}.svg")
    with open(path, "r") as f:
        svg_data = f.read()

    svg_data = svg_data.replace("currentColor", color)

    renderer = QSvgRenderer(QByteArray(svg_data.encode("utf-8")))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    renderer.render(p)
    p.end()

    _svg_cache[cache_key] = pixmap
    return pixmap


def _load_icon(name: str, size: int = 24, color: str = None) -> QIcon:
    color = color or icon_color()
    pixmap = _load_svg(name, size, color)
    return QIcon(pixmap)


def icon_play(color=None):
    return _load_icon("play", 28, color or icon_color())


def icon_pause():
    return _load_icon("pause", 24, icon_color())


def icon_stop():
    return _load_icon("stop-circle", 24, icon_color())

def icon_skip_back():
    return _load_icon("skip-back", 20, icon_color())

def icon_skip_forward():
    return _load_icon("skip-forward", 20, icon_color())

def icon_rewind():
    return _load_icon("rewind", 20, icon_color())

def icon_fast_forward():
    return _load_icon("fast-forward", 20, icon_color())


def icon_settings():
    return _load_icon("gear-six", 22, icon_color())


def icon_export():
    return _load_icon("download-simple", 24, icon_color())


def icon_volume_high():
    return _load_icon("speaker-high", 24, icon_color())


def icon_volume_muted():
    return _load_icon("speaker-simple-x", 24, icon_color())


def icon_chevron_down():
    return _load_icon("caret-down", 16, "#8e8e93")


def icon_clear():
    return _load_icon("x", 20, icon_color())


def icon_text():
    return _load_icon("text-align-left", 20, icon_color())


def icon_microphone():
    return _load_icon("microphone", 20, icon_color())


def icon_gauge():
    return _load_icon("gauge", 20, icon_color())


def icon_clipboard():
    return _load_icon("clipboard-text", 20, icon_color())

def icon_trash():
    return _load_icon("trash", 20, icon_color())

def icon_pencil():
    return _load_icon("pencil-simple", 20, icon_color())

def icon_plus():
    return _load_icon("plus", 20, icon_color())

def icon_search():
    return _load_icon("magnifying-glass", 20, icon_color())

def icon_folder_open():
    return _load_icon("folder-open", 20, icon_color())
