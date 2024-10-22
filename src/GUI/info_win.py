from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QIcon, QFont, QColor
from PySide6.QtCore import Qt
import sys
from Tools import scrap

def get_current_version():
    return "2.0"

class VersionWindow(QWidget):
    def __init__(self, theme=None):
        super().__init__()
        
        # Setează tema
        self.theme = theme
        
        self.setWindowTitle("CodeNimble - Version")
        self.setWindowIcon(QIcon("images/logo.ico"))
        
        # Dimensiunile ferestrei
        self.setFixedSize(300, 100)
        
        # Setare layout
        layout = QVBoxLayout()
        
        # Obține versiunea curentă și ultima versiune
        current_version = get_current_version()
        latest_version = scrap.get_latest_version_from_github("HojdaAdelin", "CodeNimble")
        
        # Creează etichetele
        self.current_version_label = QLabel(f"Current version: {current_version}")
        self.latest_version_label = QLabel(f"Latest version: {latest_version}")
        
        # Setează fontul pentru etichete
        font = QFont("Consolas", 18)
        self.current_version_label.setFont(font)
        self.latest_version_label.setFont(font)
        
        # Alinierea textului
        self.current_version_label.setAlignment(Qt.AlignCenter)
        self.latest_version_label.setAlignment(Qt.AlignCenter)
        
        # Adaugă etichetele la layout
        layout.addWidget(self.current_version_label)
        layout.addWidget(self.latest_version_label)
        
        # Setează layout-ul pentru fereastră
        self.apply_theme()
        self.setLayout(layout)
        
    def apply_theme(self):
        # Aplică culorile de fundal și text conform temei
        bg_color = QColor(self.theme.get("background_color", "#ffffff"))
        text_color = QColor(self.theme.get("text_color", "#000000"))
        
        # Setează culoarea de fundal pentru fereastră
        self.setStyleSheet(f"background-color: {bg_color.name()};")
        
        # Setează culoarea textului pentru etichete
        self.current_version_label.setStyleSheet(f"color: {text_color.name()};")
        self.latest_version_label.setStyleSheet(f"color: {text_color.name()};")

    def show_window(self):
        self.show()