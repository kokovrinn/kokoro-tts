from PySide6.QtCore import Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.core.text_extractor import extract_text
from app.ui.icons import icon_clipboard, icon_folder_open, icon_text, icon_trash


class TextPanel(QWidget):
    text_extracted = Signal(str)
    text_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._setup_clipboard()
        self.setAcceptDrops(True)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QHBoxLayout()
        header.setSpacing(6)
        icon_lbl = QLabel()
        icon_lbl.setPixmap(icon_text().pixmap(18, 18))
        header.addWidget(icon_lbl)
        title = QLabel("Enter your text")
        title.setObjectName("section")
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)

        layout.addSpacing(10)

        container = QFrame()
        container.setObjectName("textContainer")

        inner = QVBoxLayout(container)
        inner.setContentsMargins(0, 0, 0, 0)
        inner.setSpacing(0)

        self._text_edit = QTextEdit()
        self._text_edit.setAcceptRichText(False)
        self._text_edit.setObjectName("textInput")
        self._text_edit.setPlaceholderText(
            "Type or paste text here…\n\n"
            "You can also drag & drop .txt, .pdf, or .docx files"
        )
        self._text_edit.textChanged.connect(self._on_text_changed)
        inner.addWidget(self._text_edit, 1)

        counter_row = QHBoxLayout()
        counter_row.setContentsMargins(14, 0, 14, 6)
        counter_row.addStretch()
        self._char_count = QLabel("0 chars")
        self._char_count.setObjectName("charCount")
        counter_row.addWidget(self._char_count)
        inner.addLayout(counter_row)

        layout.addWidget(container, 1)

        layout.addSpacing(10)

        bottom_row = QHBoxLayout()
        bottom_row.setContentsMargins(0, 0, 0, 0)
        bottom_row.setSpacing(8)

        self._import_btn = QPushButton(" Import File")
        self._import_btn.setIcon(icon_folder_open())
        self._import_btn.setObjectName("importBtn")
        self._import_btn.setToolTip("Import a text file")
        self._import_btn.clicked.connect(self._import_file)
        bottom_row.addWidget(self._import_btn)

        bottom_row.addStretch()

        self._paste_btn = QPushButton(" Paste")
        self._paste_btn.setIcon(icon_clipboard())
        self._paste_btn.setObjectName("pasteBtn")
        self._paste_btn.setToolTip("Paste from clipboard")
        self._paste_btn.clicked.connect(self._paste)
        self._paste_btn.setVisible(False)
        bottom_row.addWidget(self._paste_btn)

        self._clear_btn = QPushButton(" Clear")
        self._clear_btn.setIcon(icon_trash())
        self._clear_btn.setObjectName("clearBtn")
        self._clear_btn.setToolTip("Clear")
        self._clear_btn.clicked.connect(self._clear)
        bottom_row.addWidget(self._clear_btn)

        layout.addLayout(bottom_row)

    def _setup_clipboard(self):
        self._clipboard = QApplication.clipboard()
        if self._clipboard is not None:
            self._clipboard.dataChanged.connect(self._on_clipboard_changed)
        self._update_paste_visibility()

    def _on_clipboard_changed(self):
        self._update_paste_visibility()

    def _update_paste_visibility(self):
        if self._clipboard is None:
            self._paste_btn.setVisible(False)
            return
        mime = self._clipboard.mimeData()
        self._paste_btn.setVisible(mime is not None and mime.hasText())

    def _paste(self):
        mime = self._clipboard.mimeData()
        if mime.hasText():
            text = mime.text()
            self._text_edit.insertPlainText(text)

    def _on_text_changed(self):
        text = self._text_edit.toPlainText()
        self._char_count.setText(f"{len(text)} chars")
        self.text_changed.emit(text)

    def _clear(self):
        self._text_edit.clear()

    def _import_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Import Text File", "",
            "Text Files (*.txt *.pdf *.docx *.md *.rst);;All Files (*)"
        )
        if path:
            try:
                text = extract_text(path)
                self._text_edit.setPlainText(text)
                self.text_extracted.emit(text)
            except ValueError:
                pass

    def text(self) -> str:
        return self._text_edit.toPlainText()

    def set_text(self, text: str):
        self._text_edit.setPlainText(text)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                path = url.toLocalFile()
                if path.lower().endswith((".txt", ".pdf", ".docx", ".md", ".rst")):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            try:
                text = extract_text(path)
                self._text_edit.setPlainText(text)
                self.text_extracted.emit(text)
                event.acceptProposedAction()
                return
            except ValueError:
                continue
        event.ignore()
