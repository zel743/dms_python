import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt en VS Code")
        self.label = QLabel("¡Hola desde PyQt6!")
        self.setCentralWidget(self.label)
        self.resize(1512, 982)

        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(40, 40))
        self.addToolBar(toolbar)
        self.city = self.ui.comboBoxCity.currentText()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



