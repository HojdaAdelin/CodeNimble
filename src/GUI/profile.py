import json
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PySide6.QtGui import QIcon, QFont, QColor

class ProfileWindow(QWidget):
    def __init__(self, theme=None):
        super().__init__()

        # Setează tema
        self.theme = theme

        self.setWindowTitle("CodeNimble - Profile")
        self.setWindowIcon(QIcon("images/logo.ico"))
        
        # Dimensiunile ferestrei
        self.setFixedSize(300, 200)

        # Setare layout
        layout = QVBoxLayout()

        # Creează eticheta și câmpul de text
        self.profile_name_label = QLabel("Profile name")
        self.profile_name_entry = QLineEdit()
        self.save_button = QPushButton("Save")

        # Setează fontul pentru widget-uri
        font = QFont("Consolas", 18)
        self.profile_name_label.setFont(font)
        self.profile_name_entry.setFont(font)
        self.save_button.setFont(font)

        # Conectează butonul la funcția de salvare
        self.save_button.clicked.connect(self.save_profile_name)
        layout.addStretch()
        # Adaugă widget-urile la layout
        layout.addWidget(self.profile_name_label)
        layout.addWidget(self.profile_name_entry)
        layout.addWidget(self.save_button)
        layout.addStretch()
        # Setează layout-ul pentru fereastră
        self.load_config()
        self.apply_theme()
        self.setLayout(layout)

    def apply_theme(self):
        # Aplică culorile de fundal și text conform temei
        bg_color = QColor(self.theme.get("background_color", "#ffffff"))
        text_color = QColor(self.theme.get("text_color", "#000000"))
        button_color = QColor(self.theme.get("button_color", "#555555"))
        button_hover_color = QColor(self.theme.get("button_hover_color", "#777777"))
        entry_bg = QColor(self.theme.get("editor_background", "#454545"))
        entry_fg = QColor(self.theme.get("editor_foreground", "#ffffff"))

        # Setează culoarea de fundal pentru fereastră
        self.setStyleSheet(f"background-color: {bg_color.name()};")

        # Setează culoarea textului pentru etichete
        self.profile_name_label.setStyleSheet(f"color: {text_color.name()};")

        # Setează stilul pentru câmpul de text
        self.profile_name_entry.setStyleSheet(f"background-color: {entry_bg.name()}; color: {entry_fg.name()};")

        # Setează stilul pentru buton
        self.save_button.setStyleSheet(f"""
            background-color: {button_color.name()};
            color: {text_color.name()};
            border: none;
            padding: 10px;
        """)
        self.save_button.setStyleSheet(f"""
            background-color: {button_color.name()};
            color: {text_color.name()};
            border: none;
            padding: 10px;
        """)
        self.save_button.setStyleSheet(f"""
            background-color: {button_color.name()};
            color: {text_color.name()};
            border: none;
            padding: 10px;
        """)
        # Setează stilul pentru hover (necesită un stil CSS pentru hover)
        self.save_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {button_color.name()};
                color: {text_color.name()};
                border: none;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: {button_hover_color.name()};
            }}
        """)

    def load_config(self):
        # Încarcă configurația din config.json
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                self.profile_name_entry.setText(config.get("profile_name", ""))
        except FileNotFoundError:
            pass

    def save_profile_name(self):
        profile_name = self.profile_name_entry.text()
        if not profile_name.strip():
            # Afișează un messagebox dacă câmpul este gol
            QMessageBox.warning(self, "Input Error", "Please enter a profile name.")
            return
        
        # Salvează configurația în config.json
        config = {"profile_name": profile_name}
        try:
            with open('config.json', 'r+') as f:
                existing_config = json.load(f)
                existing_config.update(config)
                f.seek(0)
                f.write(json.dumps(existing_config, indent=4))
                f.truncate()
        except FileNotFoundError:
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)

        # Confirmare salvare
        QMessageBox.information(self, "Success", "Profile name saved successfully.")