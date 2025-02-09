import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from view.main_window import MainWindow

if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())