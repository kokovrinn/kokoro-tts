DARK_STYLE = """
/* ── Global ─────────────────────────────────────────── */
QMainWindow, QDialog, QMessageBox {
    background-color: #2d2d2d;
    color: #f5f5f7;
    font-family: "SF Pro Display", "SF Pro Text", -apple-system,
                 "BlinkMacSystemFont", "Segoe UI", "Helvetica Neue", sans-serif;
    font-size: 13px;
}
QWidget {
    background-color: transparent;
    color: #f5f5f7;
    font-size: 13px;
}

/* ── Menu Bar ───────────────────────────────────────── */
QMenuBar {
    background-color: #2d2d2d;
    border-bottom: 1px solid rgba(0, 0, 0, 0.15);
    padding: 2px 0;
}
QMenuBar::item {
    padding: 6px 12px;
    background: transparent;
    border-radius: 5px;
    margin: 2px 2px;
}
QMenuBar::item:selected {
    background-color: rgba(255, 255, 255, 0.08);
}
QMenu {
    background-color: #353535;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 4px;
}
QMenu::item {
    padding: 6px 28px 6px 12px;
    border-radius: 5px;
}
QMenu::item:selected {
    background-color: #0a84ff;
    color: #ffffff;
}
QMenu::separator {
    height: 1px;
    background: rgba(255, 255, 255, 0.08);
    margin: 4px 8px;
}

/* ── Tooltip ────────────────────────────────────────── */
QToolTip {
    background-color: #353535;
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 6px;
    padding: 5px 10px;
    font-size: 12px;
}

/* ── Scrollbar ──────────────────────────────────────── */
QScrollBar:vertical {
    background: transparent;
    width: 8px;
    margin: 2px;
}
QScrollBar::handle:vertical {
    background: rgba(255, 255, 255, 0.12);
    border-radius: 4px;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover {
    background: rgba(255, 255, 255, 0.22);
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }

QScrollBar:horizontal {
    background: transparent;
    height: 8px;
    margin: 2px;
}
QScrollBar::handle:horizontal {
    background: rgba(255, 255, 255, 0.12);
    border-radius: 4px;
    min-width: 24px;
}
QScrollBar::handle:horizontal:hover {
    background: rgba(255, 255, 255, 0.22);
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: transparent; }

/* ── Labels ─────────────────────────────────────────── */
QLabel {
    color: #f5f5f7;
    background: transparent;
    border: none;
}
QLabel#title {
    font-size: 22px;
    font-weight: 600;
    color: #ffffff;
}
QLabel#subtitle {
    font-size: 12px;
    color: #9a9a9a;
}
QLabel#section {
    font-size: 11px;
    font-weight: 600;
    color: #9a9a9a;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
QLabel#section:disabled {
    color: #555555;
}
QLabel#sectionHeader {
    font-size: 11px;
    font-weight: 700;
    color: #9a9a9a;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    margin-top: 4px;
}
QLabel#footer {
    font-size: 11px;
    color: #777777;
    padding-right: 16px;
}
QFrame#footerBar {
    background-color: #1e1e22;
    border: none;
    border-top: 1px solid rgba(255, 255, 255, 0.04);
}
QLabel#statusDot {
    background-color: #22c55e;
    border-radius: 4px;
}
QLabel#footerStatus {
    font-size: 11px;
    color: #22c55e;
}
QLabel#sessionItemName {
    font-size: 13px;
    font-weight: 600;
    color: #ffffff;
}
QLabel#sessionItemSub {
    font-size: 11px;
    color: #9a9a9a;
}
QLabel#sessionItemDot {
    color: #22c55e;
    font-size: 12px;
}

/* ── Session List ───────────────────────────────────── */
QListWidget {
    background-color: transparent;
    border: none;
    outline: none;
}
QListWidget::item {
    border: 1px solid transparent;
    border-radius: 8px;
    margin: 2px 0;
}
QListWidget::item:selected {
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
}
QListWidget::item:hover:!selected {
    background-color: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.04);
}

/* ── Buttons ────────────────────────────────────────── */
QPushButton {
    background-color: #4a4a4a;
    color: #ffffff;
    border: 1px solid rgba(0, 0, 0, 0.2);
    border-radius: 5px;
    padding: 7px 16px;
    font-size: 13px;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #555555;
}
QPushButton:pressed {
    background-color: #383838;
}
QPushButton#primary {
    background-color: #0a84ff;
    color: #ffffff;
    border: none;
    font-weight: 600;
    font-size: 13px;
    border-radius: 6px;
    padding: 8px 20px;
}
QPushButton#primary:hover {
    background-color: #3593ff;
}
QPushButton#primary:pressed {
    background-color: #0062cc;
}
QPushButton#primary:disabled {
    background-color: rgba(255, 255, 255, 0.05);
    color: #6e6e73;
}
QPushButton#downloadBtn {
    background-color: #8b5cf6;
    color: #ffffff;
    border: none;
    font-weight: 600;
    font-size: 13px;
    border-radius: 6px;
    padding: 8px 20px;
}
QPushButton#downloadBtn:hover {
    background-color: #a78bfa;
}
QPushButton#downloadBtn:pressed {
    background-color: #7c3aed;
}
QPushButton#downloadBtn:disabled {
    background-color: rgba(255, 255, 255, 0.05);
    color: #6e6e73;
}
QPushButton#iconBtn {
    background: transparent;
    border: none;
    border-radius: 6px;
    padding: 5px;
    min-width: 28px;
    min-height: 28px;
    color: #a0a0a0;
}
QPushButton#iconBtn:hover {
    background-color: rgba(255, 255, 255, 0.08);
    color: #ffffff;
}
QPushButton#iconBtn:pressed {
    background-color: rgba(255, 255, 255, 0.15);
}
QPushButton#playBtn {
    background-color: #4a4a4a;
    color: #ffffff;
    border: 1px solid rgba(0, 0, 0, 0.2);
    border-radius: 28px;
    min-width: 56px;
    min-height: 56px;
    max-width: 56px;
    max-height: 56px;
}
QPushButton#generateBtn {
    background-color: #0a84ff;
    color: #ffffff;
    border: none;
    font-weight: 600;
    font-size: 14px;
    border-radius: 8px;
    padding: 10px 24px;
}
QPushButton#generateBtn:hover {
    background-color: #3593ff;
}
QPushButton#generateBtn:pressed {
    background-color: #0062cc;
}
QPushButton#generateBtn:disabled {
    background-color: rgba(255, 255, 255, 0.05);
    color: #6e6e73;
}
QPushButton#playBtn:hover {
    background-color: #555555;
}
QPushButton#playBtn:pressed {
    background-color: #383838;
}
QPushButton#playBtn:disabled {
    background-color: #303030;
    color: #6e6e6e;
    border: none;
}
QPushButton#smallBtn {
    background-color: #4a4a4a;
    color: #a0a0a0;
    border: 1px solid rgba(0, 0, 0, 0.15);
    border-radius: 5px;
    padding: 8px 20px;
    font-size: 13px;
}
QPushButton#smallBtn:hover {
    background-color: #555555;
    color: #f5f5f7;
}
QPushButton#playCircleBtn {
    background-color: #000000;
    border: none;
    border-radius: 14px;
    min-width: 28px;
    min-height: 28px;
    max-width: 28px;
    max-height: 28px;
    color: #ffffff;
}
QPushButton#playCircleBtn:hover {
    background-color: #1a1a1a;
}
QPushButton#playCircleBtn:pressed {
    background-color: #333333;
}
QPushButton#playCircleBtn:disabled {
    background-color: rgba(255, 255, 255, 0.06);
    color: #555555;
}
QPushButton#stopCircleBtn {
    background-color: transparent;
    border: 1.5px solid rgba(255, 255, 255, 0.2);
    border-radius: 11px;
    min-width: 22px;
    min-height: 22px;
    max-width: 22px;
    max-height: 22px;
    color: #a0a0a0;
}
QPushButton#stopCircleBtn:hover {
    border-color: rgba(255, 255, 255, 0.4);
    color: #ffffff;
}
QPushButton#stopCircleBtn:pressed {
    background-color: rgba(255, 255, 255, 0.1);
}
QPushButton#stopCircleBtn:disabled {
    border-color: rgba(255, 255, 255, 0.08);
    color: #555555;
}
QPushButton#skipCircleBtn {
    background-color: transparent;
    border: 1.5px solid rgba(255, 255, 255, 0.2);
    border-radius: 11px;
    min-width: 22px;
    min-height: 22px;
    max-width: 22px;
    max-height: 22px;
    color: #a0a0a0;
}
QPushButton#skipCircleBtn:hover {
    border-color: rgba(255, 255, 255, 0.4);
    color: #ffffff;
}
QPushButton#skipCircleBtn:pressed {
    background-color: rgba(255, 255, 255, 0.1);
}
QPushButton#skipCircleBtn:disabled {
    border-color: rgba(255, 255, 255, 0.08);
    color: #555555;
}
QPushButton#importBtn {
    background-color: #0a84ff;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 8px 20px;
    font-size: 13px;
    font-weight: 500;
}
QPushButton#importBtn:hover {
    background-color: #3593ff;
}
QPushButton#importBtn:pressed {
    background-color: #0062cc;
}
QPushButton#pasteBtn, QPushButton#clearBtn {
    font-size: 13px;
    font-weight: 500;
    border: none;
    border-radius: 6px;
    padding: 8px 20px;
}
QPushButton#pasteBtn {
    background-color: #22c55e;
    color: #ffffff;
}
QPushButton#pasteBtn:hover {
    background-color: #2dd96e;
}
QPushButton#pasteBtn:pressed {
    background-color: #16a34a;
}
QPushButton#clearBtn {
    background-color: #ef4444;
    color: #ffffff;
}
QPushButton#clearBtn:hover {
    background-color: #f87171;
}
QPushButton#clearBtn:pressed {
    background-color: #dc2626;
}

/* ── Text Input ─────────────────────────────────────── */
QTextEdit, QPlainTextEdit {
    background-color: #353535;
    color: #f5f5f7;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
    padding: 14px;
    font-size: 14px;
    line-height: 1.6;
    selection-background-color: #0a84ff;
    selection-color: #ffffff;
}
QTextEdit:focus, QPlainTextEdit:focus {
    border: 1.5px solid #0a84ff;
}
QFrame#textContainer {
    background-color: #353535;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
}
QTextEdit#textInput {
    background: transparent;
    border: none;
    border-radius: 0;
    padding: 14px 14px 0;
}
QTextEdit#textInput:focus {
    border: none;
}
QFrame#separator {
    background-color: rgba(255, 255, 255, 0.08);
    max-height: 1px;
}
QLabel#charCount {
    color: #777777;
    font-size: 11px;
}

/* ── ComboBox ───────────────────────────────────────── */
QComboBox {
    background-color: #353535;
    color: #f5f5f7;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 13px;
    min-width: 150px;
}
QComboBox:hover {
    border-color: rgba(255, 255, 255, 0.12);
}
QComboBox:focus {
    border: 1.5px solid #0a84ff;
}
QComboBox QAbstractItemView {
    background-color: #353535;
    color: #f5f5f7;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 6px;
    selection-background-color: #0a84ff;
    selection-color: #ffffff;
    outline: none;
    padding: 3px;
}
QComboBox::drop-down {
    border: none;
    width: 24px;
}
QComboBox::down-arrow {
    image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%23a0a0a0' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
    width: 12px;
    height: 12px;
}
QComboBox:disabled {
    background-color: #2a2a2a;
    color: #555555;
    border-color: rgba(255, 255, 255, 0.03);
}
QComboBox:disabled::drop-down {
    opacity: 0.3;
}
QComboBox:disabled::down-arrow {
    opacity: 0.3;
}
QComboBox QAbstractItemView::item {
    padding: 5px 8px;
    border-radius: 4px;
}

/* ── Slider ─────────────────────────────────────────── */
QSlider::groove:horizontal {
    background: rgba(255, 255, 255, 0.08);
    border: none;
    border-radius: 2px;
    height: 4px;
}
QSlider::handle:horizontal {
    background: #ffffff;
    border: 1px solid rgba(0, 0, 0, 0.15);
    border-radius: 7px;
    width: 14px;
    height: 14px;
    margin: -5px 0;
}
QSlider::handle:horizontal:hover {
    background: #f5f5f7;
}
QSlider::sub-page:horizontal {
    background: #0a84ff;
    border-radius: 2px;
}

/* ── Progress Bar ───────────────────────────────────── */
QProgressBar {
    background-color: rgba(255, 255, 255, 0.08);
    border: none;
    border-radius: 2px;
    height: 4px;
    text-align: center;
    font-size: 1px;
    color: transparent;
}
QProgressBar::chunk {
    background-color: #0a84ff;
    border-radius: 2px;
}

/* ── GroupBox ───────────────────────────────────────── */
QGroupBox {
    background-color: #252525;
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 12px;
    margin-top: 24px;
    padding: 20px 16px 12px 16px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 16px;
    top: 4px;
    font-size: 11px;
    font-weight: 600;
    color: #9a9a9a;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── Splitter ───────────────────────────────────────── */
QSplitter::handle {
    background: rgba(255, 255, 255, 0.05);
}
QSplitter::handle:horizontal { width: 1px; }
QSplitter::handle:vertical { height: 1px; }

/* ── Status Bar ─────────────────────────────────────── */
QStatusBar {
    background-color: #2d2d2d;
    color: #9a9a9a;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    font-size: 12px;
    padding: 3px 12px;
}

/* ── Checkbox ───────────────────────────────────────── */
QCheckBox {
    color: #f5f5f7;
    spacing: 8px;
    font-size: 13px;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1.5px solid rgba(255, 255, 255, 0.25);
    border-radius: 4px;
    background: transparent;
}
QCheckBox::indicator:hover {
    border-color: rgba(255, 255, 255, 0.4);
}
QCheckBox::indicator:checked {
    background: #0a84ff;
    border-color: #0a84ff;
    image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='4' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='20 6 9 17 4 12'%3E%3C/polyline%3E%3C/svg%3E");
}

/* ── Line Edit ──────────────────────────────────────── */
QLineEdit {
    background-color: #1a1a1a;
    color: #f5f5f7;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 6px;
    padding: 7px 12px;
    font-size: 13px;
    selection-background-color: #0a84ff;
    selection-color: #ffffff;
}
QLineEdit:focus {
    border: 1.5px solid #0a84ff;
}
QLineEdit#sessionName {
    background-color: transparent;
    border: none;
    color: #ffffff;
    font-size: 17px;
    font-weight: 600;
    padding: 0 6px;
    selection-background-color: #0a84ff;
    selection-color: #ffffff;
}
QLineEdit#sessionName:hover {
    color: #f5f5f7;
}
QLineEdit#sessionName:focus {
    border: none;
    background-color: transparent;
    color: #ffffff;
}
QLineEdit#outputPath {
    background-color: #2a2a2a;
    color: #9a9a9a;
    font-size: 12px;
    padding: 5px 10px;
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 5px;
}
"""

LIGHT_STYLE = """
/* ── Global ─────────────────────────────────────────── */
QMainWindow, QDialog, QMessageBox {
    background-color: #f5f5f7;
    color: #1d1d1f;
    font-family: "SF Pro Display", "SF Pro Text", -apple-system,
                 "BlinkMacSystemFont", "Segoe UI", "Helvetica Neue", sans-serif;
    font-size: 13px;
}
QWidget {
    background-color: transparent;
    color: #1d1d1f;
    font-size: 13px;
}

/* ── Menu Bar ───────────────────────────────────────── */
QMenuBar {
    background-color: #f5f5f7;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    padding: 2px 0;
}
QMenuBar::item {
    padding: 6px 12px;
    background: transparent;
    border-radius: 5px;
    margin: 2px 2px;
}
QMenuBar::item:selected {
    background-color: rgba(0, 0, 0, 0.05);
}
QMenu {
    background-color: #ffffff;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 8px;
    padding: 4px;
}
QMenu::item {
    padding: 6px 28px 6px 12px;
    border-radius: 5px;
}
QMenu::item:selected {
    background-color: #007aff;
    color: #ffffff;
}
QMenu::separator {
    height: 1px;
    background: rgba(0, 0, 0, 0.05);
    margin: 4px 8px;
}

/* ── Tooltip ────────────────────────────────────────── */
QToolTip {
    background-color: #ffffff;
    color: #1d1d1f;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 6px;
    padding: 5px 10px;
    font-size: 12px;
}

/* ── Scrollbar ──────────────────────────────────────── */
QScrollBar:vertical {
    background: transparent;
    width: 8px;
    margin: 2px;
}
QScrollBar::handle:vertical {
    background: rgba(0, 0, 0, 0.15);
    border-radius: 4px;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover {
    background: rgba(0, 0, 0, 0.3);
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }

QScrollBar:horizontal {
    background: transparent;
    height: 8px;
    margin: 2px;
}
QScrollBar::handle:horizontal {
    background: rgba(0, 0, 0, 0.15);
    border-radius: 4px;
    min-width: 24px;
}
QScrollBar::handle:horizontal:hover {
    background: rgba(0, 0, 0, 0.3);
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: transparent; }

/* ── Labels ─────────────────────────────────────────── */
QLabel {
    color: #1d1d1f;
    background: transparent;
    border: none;
}
QLabel#title {
    font-size: 22px;
    font-weight: 600;
    color: #000000;
}
QLabel#subtitle {
    font-size: 12px;
    color: #86868b;
}
QLabel#section {
    font-size: 11px;
    font-weight: 600;
    color: #86868b;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
QLabel#section:disabled {
    color: #aeaeb2;
}
QLabel#sectionHeader {
    font-size: 11px;
    font-weight: 700;
    color: #86868b;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.08);
    margin-top: 4px;
}
QLabel#footer {
    font-size: 11px;
    color: #aeaeb2;
    padding-right: 16px;
}
QFrame#footerBar {
    background-color: #e8e8ed;
    border: none;
    border-top: 1px solid rgba(0, 0, 0, 0.05);
}
QLabel#statusDot {
    background-color: #22c55e;
    border-radius: 4px;
}
QLabel#footerStatus {
    font-size: 11px;
    color: #22c55e;
}
QLabel#sessionItemName {
    font-size: 13px;
    font-weight: 600;
    color: #1d1d1f;
}
QLabel#sessionItemSub {
    font-size: 11px;
    color: #86868b;
}
QLabel#sessionItemDot {
    color: #22c55e;
    font-size: 12px;
}

/* ── Session List ───────────────────────────────────── */
QListWidget {
    background-color: transparent;
    border: none;
    outline: none;
}
QListWidget::item {
    border: 1px solid transparent;
    border-radius: 8px;
    margin: 2px 0;
}
QListWidget::item:selected {
    background-color: rgba(0, 0, 0, 0.03);
    border: 1px solid rgba(0, 0, 0, 0.06);
}
QListWidget::item:hover:!selected {
    background-color: rgba(0, 0, 0, 0.02);
    border: 1px solid rgba(0, 0, 0, 0.04);
}

/* ── Buttons ────────────────────────────────────────── */
QPushButton {
    background-color: #ffffff;
    color: #1d1d1f;
    border: 1px solid rgba(0, 0, 0, 0.12);
    border-radius: 6px;
    padding: 7px 16px;
    font-size: 13px;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #f5f5f7;
}
QPushButton:pressed {
    background-color: #e5e5ea;
}
QPushButton#primary {
    background-color: #007aff;
    color: #ffffff;
    border: none;
    font-weight: 600;
    font-size: 13px;
    border-radius: 6px;
    padding: 8px 20px;
}
QPushButton#primary:hover {
    background-color: #2b8cff;
}
QPushButton#primary:pressed {
    background-color: #0062cc;
}
QPushButton#primary:disabled {
    background-color: rgba(0, 0, 0, 0.04);
    color: #aeaeb2;
}
QPushButton#downloadBtn {
    background-color: #8b5cf6;
    color: #ffffff;
    border: none;
    font-weight: 600;
    font-size: 13px;
    border-radius: 6px;
    padding: 8px 20px;
}
QPushButton#downloadBtn:hover {
    background-color: #a78bfa;
}
QPushButton#downloadBtn:pressed {
    background-color: #7c3aed;
}
QPushButton#downloadBtn:disabled {
    background-color: rgba(0, 0, 0, 0.04);
    color: #aeaeb2;
}
QPushButton#iconBtn {
    background: transparent;
    border: none;
    border-radius: 6px;
    padding: 5px;
    min-width: 28px;
    min-height: 28px;
    color: #86868b;
}
QPushButton#iconBtn:hover {
    background-color: rgba(0, 0, 0, 0.06);
    color: #1d1d1f;
}
QPushButton#iconBtn:pressed {
    background-color: rgba(0, 0, 0, 0.1);
}
QPushButton#playBtn {
    background-color: #007aff;
    color: #ffffff;
    border: none;
    border-radius: 28px;
    min-width: 56px;
    min-height: 56px;
    max-width: 56px;
    max-height: 56px;
}
QPushButton#playBtn:hover {
    background-color: #2b8cff;
}
QPushButton#playBtn:pressed {
    background-color: #0062cc;
}
QPushButton#playBtn:disabled {
    background-color: rgba(0, 0, 0, 0.06);
    color: #aeaeb2;
}
QPushButton#generateBtn {
    background-color: #007aff;
    color: #ffffff;
    border: none;
    font-weight: 600;
    font-size: 14px;
    border-radius: 8px;
    padding: 10px 24px;
}
QPushButton#generateBtn:hover {
    background-color: #2b8cff;
}
QPushButton#generateBtn:pressed {
    background-color: #0062cc;
}
QPushButton#generateBtn:disabled {
    background-color: rgba(0, 0, 0, 0.06);
    color: #aeaeb2;
}
QPushButton#smallBtn {
    background-color: #ffffff;
    color: #86868b;
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    padding: 8px 20px;
    font-size: 13px;
}
QPushButton#smallBtn:hover {
    background-color: #f5f5f7;
    color: #1d1d1f;
}
QPushButton#playCircleBtn {
    background-color: #ffffff;
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 14px;
    min-width: 28px;
    min-height: 28px;
    max-width: 28px;
    max-height: 28px;
    color: #000000;
}
QPushButton#playCircleBtn:hover {
    background-color: #f5f5f7;
}
QPushButton#playCircleBtn:pressed {
    background-color: #e5e5ea;
}
QPushButton#playCircleBtn:disabled {
    background-color: rgba(0, 0, 0, 0.04);
    color: #aeaeb2;
    border-color: transparent;
}
QPushButton#stopCircleBtn {
    background-color: transparent;
    border: 1.5px solid rgba(0, 0, 0, 0.2);
    border-radius: 11px;
    min-width: 22px;
    min-height: 22px;
    max-width: 22px;
    max-height: 22px;
    color: #86868b;
}
QPushButton#stopCircleBtn:hover {
    border-color: rgba(0, 0, 0, 0.4);
    color: #1d1d1f;
}
QPushButton#stopCircleBtn:pressed {
    background-color: rgba(0, 0, 0, 0.06);
}
QPushButton#stopCircleBtn:disabled {
    border-color: rgba(0, 0, 0, 0.08);
    color: #aeaeb2;
}
QPushButton#skipCircleBtn {
    background-color: transparent;
    border: 1.5px solid rgba(0, 0, 0, 0.2);
    border-radius: 11px;
    min-width: 22px;
    min-height: 22px;
    max-width: 22px;
    max-height: 22px;
    color: #86868b;
}
QPushButton#skipCircleBtn:hover {
    border-color: rgba(0, 0, 0, 0.4);
    color: #1d1d1f;
}
QPushButton#skipCircleBtn:pressed {
    background-color: rgba(0, 0, 0, 0.06);
}
QPushButton#skipCircleBtn:disabled {
    border-color: rgba(0, 0, 0, 0.08);
    color: #aeaeb2;
}
QPushButton#importBtn {
    background-color: #007aff;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 8px 20px;
    font-size: 13px;
    font-weight: 500;
}
QPushButton#importBtn:hover {
    background-color: #2b8cff;
}
QPushButton#importBtn:pressed {
    background-color: #0062cc;
}
QPushButton#pasteBtn, QPushButton#clearBtn {
    font-size: 13px;
    font-weight: 500;
    border: none;
    border-radius: 6px;
    padding: 8px 20px;
}
QPushButton#pasteBtn {
    background-color: #22c55e;
    color: #ffffff;
}
QPushButton#pasteBtn:hover {
    background-color: #2dd96e;
}
QPushButton#pasteBtn:pressed {
    background-color: #16a34a;
}
QPushButton#clearBtn {
    background-color: #ef4444;
    color: #ffffff;
}
QPushButton#clearBtn:hover {
    background-color: #f87171;
}
QPushButton#clearBtn:pressed {
    background-color: #dc2626;
}

/* ── Text Input ─────────────────────────────────────── */
QTextEdit, QPlainTextEdit {
    background-color: #ffffff;
    color: #1d1d1f;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 10px;
    padding: 14px;
    font-size: 14px;
    line-height: 1.6;
    selection-background-color: #007aff;
    selection-color: #ffffff;
}
QTextEdit:focus, QPlainTextEdit:focus {
    border: 1.5px solid #007aff;
}
QFrame#textContainer {
    background-color: #ffffff;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 10px;
}
QTextEdit#textInput {
    background: transparent;
    border: none;
    border-radius: 0;
    padding: 14px 14px 0;
}
QTextEdit#textInput:focus {
    border: none;
}
QFrame#separator {
    background-color: rgba(0, 0, 0, 0.08);
    max-height: 1px;
}
QLabel#charCount {
    color: #86868b;
    font-size: 11px;
}

/* ── ComboBox ───────────────────────────────────────── */
QComboBox {
    background-color: #ffffff;
    color: #1d1d1f;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 13px;
    min-width: 150px;
}
QComboBox:hover {
    border-color: rgba(0, 0, 0, 0.15);
}
QComboBox:focus {
    border: 1.5px solid #007aff;
}
QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #1d1d1f;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 6px;
    selection-background-color: #007aff;
    selection-color: #ffffff;
    outline: none;
    padding: 3px;
}
QComboBox::drop-down {
    border: none;
    width: 24px;
}
QComboBox::down-arrow {
    image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2386868b' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
    width: 12px;
    height: 12px;
}
QComboBox:disabled {
    background-color: #f0f0f0;
    color: #aeaeb2;
    border-color: rgba(0, 0, 0, 0.04);
}
QComboBox:disabled::drop-down {
    opacity: 0.3;
}
QComboBox:disabled::down-arrow {
    opacity: 0.3;
}
QComboBox QAbstractItemView::item {
    padding: 5px 8px;
    border-radius: 4px;
}

/* ── Slider ─────────────────────────────────────────── */
QSlider::groove:horizontal {
    background: rgba(0, 0, 0, 0.1);
    border: none;
    border-radius: 2px;
    height: 4px;
}
QSlider::handle:horizontal {
    background: #ffffff;
    border: 1px solid rgba(0, 0, 0, 0.15);
    border-radius: 7px;
    width: 14px;
    height: 14px;
    margin: -5px 0;
}
QSlider::handle:horizontal:hover {
    background: #f5f5f7;
}
QSlider::sub-page:horizontal {
    background: #007aff;
    border-radius: 2px;
}

/* ── Progress Bar ───────────────────────────────────── */
QProgressBar {
    background-color: rgba(0, 0, 0, 0.05);
    border: none;
    border-radius: 2px;
    height: 4px;
    text-align: center;
    font-size: 1px;
    color: transparent;
}
QProgressBar::chunk {
    background-color: #007aff;
    border-radius: 2px;
}

/* ── GroupBox ───────────────────────────────────────── */
QGroupBox {
    background-color: #ffffff;
    border: 1px solid rgba(0, 0, 0, 0.06);
    border-radius: 12px;
    margin-top: 24px;
    padding: 20px 16px 12px 16px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 16px;
    top: 4px;
    font-size: 11px;
    font-weight: 600;
    color: #86868b;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── Splitter ───────────────────────────────────────── */
QSplitter::handle {
    background: rgba(0, 0, 0, 0.05);
}
QSplitter::handle:horizontal { width: 1px; }
QSplitter::handle:vertical { height: 1px; }

/* ── Status Bar ─────────────────────────────────────── */
QStatusBar {
    background-color: #f5f5f7;
    color: #86868b;
    border-top: 1px solid rgba(0, 0, 0, 0.05);
    font-size: 12px;
    padding: 3px 12px;
}

/* ── Checkbox ───────────────────────────────────────── */
QCheckBox {
    color: #1d1d1f;
    spacing: 8px;
    font-size: 13px;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1.5px solid rgba(0, 0, 0, 0.2);
    border-radius: 4px;
    background: transparent;
}
QCheckBox::indicator:hover {
    border-color: rgba(0, 0, 0, 0.4);
}
QCheckBox::indicator:checked {
    background: #007aff;
    border-color: #007aff;
    image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='4' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='20 6 9 17 4 12'%3E%3C/polyline%3E%3C/svg%3E");
}

/* ── Line Edit ──────────────────────────────────────── */
QLineEdit {
    background-color: #ffffff;
    color: #1d1d1f;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 6px;
    padding: 7px 12px;
    font-size: 13px;
    selection-background-color: #007aff;
    selection-color: #ffffff;
}
QLineEdit:focus {
    border: 1.5px solid #007aff;
}
QLineEdit#sessionName {
    background-color: transparent;
    border: none;
    color: #1d1d1f;
    font-size: 17px;
    font-weight: 600;
    padding: 0 6px;
    selection-background-color: #007aff;
    selection-color: #ffffff;
}
QLineEdit#sessionName:hover {
    color: #000000;
}
QLineEdit#sessionName:focus {
    border: none;
    background-color: transparent;
    color: #1d1d1f;
}
QLineEdit#outputPath {
    background-color: #f0f0f0;
    color: #86868b;
    font-size: 12px;
    padding: 5px 10px;
    border: 1px solid rgba(0, 0, 0, 0.06);
    border-radius: 5px;
}
"""


def get_style(theme: str) -> str:
    return DARK_STYLE if theme == "dark" else LIGHT_STYLE
