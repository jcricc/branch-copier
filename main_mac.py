import sys
from PyQt6.QtWidgets import QApplication
from copier_ui import ProjectCopier

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ProjectCopier()
    win.resize(800, 600)
    win.show()
    sys.exit(app.exec())
