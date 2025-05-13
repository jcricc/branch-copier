import os
import pyperclip
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QListWidget,
    QLineEdit, QLabel, QMessageBox, QListWidgetItem, QTextEdit,
    QHBoxLayout, QMenu, QFrame
)
from PyQt6.QtGui import QShortcut, QKeySequence, QColor, QAction, QPixmap
from PyQt6.QtCore import Qt, QPoint


class ProjectCopier(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Branch Copier")
        self.setMinimumSize(800, 600)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.src_folder = ''
        self.files = []
        self.excluded_items = set()

        # Inputs
        self.extensions_input = QLineEdit("")
        self.exclude_input = QLineEdit(".git,__pycache__")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Filter files by name...")

        # Buttons
        self.folder_btn = QPushButton("Choose Project Folder")
        self.copy_contents_btn = QPushButton("Copy File Contents (with filename)")
        self.copy_structure_btn = QPushButton("Copy Folder Structure")

        # File list and preview
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.file_list.itemClicked.connect(self.preview_file)
        self.file_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.file_list.customContextMenuRequested.connect(self.show_context_menu)

        self.preview_area = QTextEdit()
        self.preview_area.setReadOnly(True)

        # Top input controls
        top_controls = QHBoxLayout()
        top_controls.addWidget(QLabel("Include extensions:"))
        top_controls.addWidget(self.extensions_input)
        top_controls.addWidget(QLabel("Exclude folders containing:"))
        top_controls.addWidget(self.exclude_input)

        # Shortcut help and logo box (bottom row)
        help_label = QLabel()
        help_label.setTextFormat(Qt.TextFormat.RichText)
        help_label.setText(
            "<b>⌨️ Shortcuts:</b><br>"
            "<b>⌘ + O</b> → Open project folder<br>"
            "<b>⌘ + F</b> → Focus file search<br>"
            "<b>⌘ + ⇧ + C</b> → Copy selected file content<br>"
            "<b>⌘ + ⇧ + S</b> → Copy folder structure<br>"
            "<b>Right-click</b> a file → Copy full path"
        )

        logo_label = QLabel()
        logo_pixmap = QPixmap("logo.png").scaledToHeight(164, Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)

        bottom_row = QHBoxLayout()
        bottom_row.addWidget(help_label)
        bottom_row.addStretch()
        bottom_row.addWidget(logo_label)

        # Layout
        layout = QVBoxLayout()
        layout.addLayout(top_controls)
        layout.addWidget(self.folder_btn)
        layout.addWidget(QLabel("Search:"))
        layout.addWidget(self.search_input)
        layout.addWidget(QLabel("File List:"))
        layout.addWidget(self.file_list)
        layout.addWidget(QLabel("File Preview:"))
        layout.addWidget(self.preview_area)
        layout.addWidget(self.copy_contents_btn)
        layout.addWidget(self.copy_structure_btn)
        layout.addLayout(bottom_row)
        self.setLayout(layout)

        # Connect signals
        self.folder_btn.clicked.connect(self.choose_folder)
        self.copy_contents_btn.clicked.connect(self.copy_preview_contents)
        self.copy_structure_btn.clicked.connect(self.copy_folder_structure)
        self.exclude_input.textChanged.connect(self.load_files)
        self.extensions_input.textChanged.connect(self.load_files)
        self.search_input.textChanged.connect(self.filter_files)

        # Keyboard shortcuts
        QShortcut(QKeySequence("Meta+O"), self, self.choose_folder)
        QShortcut(QKeySequence("Meta+F"), self, self.focus_search)
        QShortcut(QKeySequence("Meta+Shift+C"), self, self.copy_preview_contents)
        QShortcut(QKeySequence("Meta+Shift+S"), self, self.copy_folder_structure)

        try:
            pyperclip.set_clipboard("pbcopy")
        except:
            pass

    def show_context_menu(self, position: QPoint):
        item = self.file_list.itemAt(position)
        if item:
            menu = QMenu()
            copy_action = QAction("Copy Path", self)
            copy_action.triggered.connect(lambda: self.copy_path(item.text()))
            menu.addAction(copy_action)
            menu.exec(self.file_list.mapToGlobal(position))

    def copy_path(self, path):
        pyperclip.copy(path)
        QMessageBox.information(self, "Copied", "File path copied to clipboard.")

    def focus_search(self):
        self.search_input.setFocus()

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Project Folder")
        if folder:
            self.src_folder = folder
            self.file_list.clear()
            self.preview_area.clear()
            self.setWindowTitle(f"Project to AI Helper — {os.path.basename(folder)}")
            self.load_files()

    def load_files(self):
        self.files.clear()
        self.file_list.clear()
        self.excluded_items.clear()

        exts = [e.strip() for e in self.extensions_input.text().split(',') if e.strip()]
        excludes = [e.strip() for e in self.exclude_input.text().split(',') if e.strip()]

        for root, _, files in os.walk(self.src_folder):
            is_excluded = any(ex in root for ex in excludes)
            for file in files:
                if not exts or any(file.endswith(ext) for ext in exts):
                    full_path = os.path.join(root, file)
                    self.files.append(full_path)

                    item = QListWidgetItem(full_path)
                    if is_excluded:
                        item.setForeground(QColor('gray'))
                        self.excluded_items.add(full_path)

                    self.file_list.addItem(item)

        self.filter_files()

    def filter_files(self):
        text = self.search_input.text().lower()
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            item.setHidden(text not in item.text().lower())

    def preview_file(self, item: QListWidgetItem):
        path = item.text()
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.preview_area.setPlainText(content)
        except Exception as e:
            self.preview_area.setPlainText(f"[Failed to read file: {e}]")

    def copy_preview_contents(self):
        item = self.file_list.currentItem()
        if not item:
            QMessageBox.warning(self, "No file", "Select a file first.")
            return

        path = item.text()
        content = self.preview_area.toPlainText()
        if not content.strip():
            QMessageBox.warning(self, "Empty", "File preview is empty.")
            return

        filename = os.path.relpath(path, self.src_folder)
        result = f"# {filename}\n\n{content}"

        try:
            pyperclip.copy(result)
            QMessageBox.information(self, "Copied", "File content with header copied.")
        except Exception as e:
            QMessageBox.critical(self, "Clipboard Error", str(e))

    def copy_folder_structure(self):
        if not self.src_folder:
            QMessageBox.warning(self, "No folder", "Select a project folder first.")
            return

        excludes = [e.strip() for e in self.exclude_input.text().split(',') if e.strip()]
        structure = []
        root_len = len(self.src_folder.rstrip(os.sep)) + 1

        for root, dirs, files in os.walk(self.src_folder):
            if any(ex in root for ex in excludes):
                continue

            rel_root = root[root_len:]
            indent = "  " * rel_root.count(os.sep)
            structure.append(f"{indent}{os.path.basename(root)}/")

            for file in files:
                structure.append(f"{indent}  {file}")

        try:
            pyperclip.copy("\n".join(structure))
            QMessageBox.information(self, "Copied", "Folder structure copied to clipboard.")
        except Exception as e:
            QMessageBox.critical(self, "Clipboard Error", str(e))
