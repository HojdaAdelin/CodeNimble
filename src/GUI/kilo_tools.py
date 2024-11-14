from PySide6.QtWidgets import QLabel, QMainWindow
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFont

from Tools import kilonova

class Kilotools(QMainWindow):
    def __init__(self,theme,parent=None):
        super().__init__(parent)
        self.theme = theme
        self.setWindowTitle("Code Nimble - Kilonova tools")
        self.setGeometry(100, 100, 600, 200)
        self.setWindowIcon(QIcon("images/logo.ico"))
        self.setFixedSize(600, 200)

        self.apply_theme(self.theme)
        self.contest_name, self.contest_info = kilonova.contest_info()

        self.gui()

    def apply_theme(self, theme):
        self.setStyleSheet(f"""
            background-color: {theme['background_color']};
            color: {theme['text_color']};
        """)

    def gui(self):

        self.contest_label = QLabel(f"Latest contest: {self.contest_name}", self)
        self.contest_label.setFont(QFont("Arial", 12))
        self.contest_label.setAlignment(Qt.AlignCenter)
        self.contest_label.setGeometry(50, 50, 500, 50)

        self.contest_status_label = QLabel(f"Status: {self.contest_info}", self)
        self.contest_status_label.setFont(QFont("Arial", 12))
        self.contest_status_label.setAlignment(Qt.AlignCenter)
        self.contest_status_label.setGeometry(50, 120, 500, 50)