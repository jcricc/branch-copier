import os
import pyperclip
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QListWidget, 
    QLineEdit, QLabel, QMessageBox, QListWidgetItem, QTextEdit
)
from PyQt6.QtCore import Qt

class ProjectCopier(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Branch Copier")

        self.src_folder = ''
        self.files = []

        # Inputs
        self.extensions_input = QLineEdit("")
        self.exclude_input = QLineEdit(".git,__pycache__")

        # Buttons
        self.folder_btn = QPushButton("Choose Project Folder")
        self.copy_contents_btn = QPushButton("Copy File Contents (with filename)")
        self.copy_structure_btn = QPushButton("Copy Folder Structure")

        # File list and preview
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.file_list.itemClicked.connect(self.preview_file)

        self.preview_area = QTextEdit()
        self.preview_area.setReadOnly(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Include extensions:"))
        layout.addWidget(self.extensions_input)
        layout.addWidget(QLabel("Exclude folders containing:"))
        layout.addWidget(self.exclude_input)
        layout.addWidget(self.folder_btn)
        layout.addWidget(QLabel("File List:"))
        layout.addWidget(self.file_list)
        layout.addWidget(QLabel("File Preview:"))
        layout.addWidget(self.preview_area)
        layout.addWidget(self.copy_contents_btn)
        layout.addWidget(self.copy_structure_btn)

        self.setLayout(layout)

        # Connections
        self.folder_btn.clicked.connect(self.choose_folder)
        self.copy_contents_btn.clicked.connect(self.copy_preview_contents)
        self.copy_structure_btn.clicked.connect(self.copy_folder_structure)

        # macOS clipboard compatibility
        try:
            pyperclip.set_clipboard("pbcopy")
        except:
            pass

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

        exts = [e.strip() for e in self.extensions_input.text().split(',') if e.strip()]
        excludes = [e.strip() for e in self.exclude_input.text().split(',') if e.strip()]

        for root, _, files in os.walk(self.src_folder):
            if any(ex in root for ex in excludes):
                continue
            for file in files:
                if not exts or any(file.endswith(ext) for ext in exts):
                    full_path = os.path.join(root, file)
                    self.files.append(full_path)
                    self.file_list.addItem(QListWidgetItem(full_path))

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

        structure = []
        root_len = len(self.src_folder.rstrip(os.sep)) + 1

        for root, dirs, files in os.walk(self.src_folder):
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
