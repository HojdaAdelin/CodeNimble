from PySide6.QtWidgets import (QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QGridLayout, QMessageBox)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from Tools import fetch

class FetchWindow(QWidget):
    def __init__(self, right_panel, theme, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.right_panel = right_panel
        self.theme = theme
        self.setWindowTitle("Code Nimble - fetch test cases")
        self.setFixedSize(320, 120)  # Dimensiuni inițiale
        self.setWindowIcon(QIcon("images/logo.ico"))
        self.apply_theme()
        self.initUI()

    def apply_theme(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.theme.get('background_color')};
                color: {self.theme.get('text_color')};
            }}
            QLineEdit, QComboBox, QLabel {{
                background-color: {self.theme.get('editor_background')};
                color: {self.theme.get('editor_foreground')};
                border: 1px solid {self.theme.get('border_color')};
                font-size: 16px;
            }}
            QLineEdit, QComboBox {{
                padding: 4px;
            }}
            QPushButton {{
                background-color: {self.theme.get('button_color')};
                color: {self.theme.get('text_color')};
                border: 1px solid {self.theme.get('border_color')};
                font-size: 16px;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: {self.theme.get('button_hover_color')};
            }}
        """)

    def initUI(self):
        layout = QGridLayout(self)
        layout.setHorizontalSpacing(8)
        layout.setVerticalSpacing(4)

        # Platform label
        self.site_label = QLabel("Platform", self)
        layout.addWidget(self.site_label, 0, 0, Qt.AlignTop)

        # Problem ID label
        self.id_label = QLabel("Problem ID", self)
        layout.addWidget(self.id_label, 0, 1, Qt.AlignTop)

        # Platform ComboBox
        self.site = QComboBox(self)
        self.site.addItems(["Pbinfo", "Kilonova", "Codeforces", "AtCoder"])
        self.site.currentIndexChanged.connect(self.toggle_gui)
        layout.addWidget(self.site, 1, 0)

        # Problem ID Entry
        self.id = QLineEdit(self)
        self.id.setFixedWidth(185)
        layout.addWidget(self.id, 1, 1)

        # Contest ID Entry and Label (Hidden by default)
        self.contest_id_for_cf = QLineEdit(self)
        self.contest_id_for_cf.setFixedWidth(120)
        self.contest_id_for_cf_label = QLabel("Contest ID", self)
        self.contest_id_for_cf.hide()
        self.contest_id_for_cf_label.hide()

        # Fetch Button
        self.fetch_button = QPushButton("Fetch test cases", self, clicked=self.fetch)
        self.fetch_button.setFixedWidth(300)
        layout.addWidget(self.fetch_button, 2, 0, 1, 3, Qt.AlignCenter)

        self.setLayout(layout)

    def toggle_gui(self):
        platform = self.site.currentText()
        if platform == "Codeforces":
            self.contest_id_for_cf_label.show()
            self.contest_id_for_cf.show()
            self.layout().addWidget(self.contest_id_for_cf_label, 0, 2)
            self.layout().addWidget(self.contest_id_for_cf, 1, 2)
            self.setFixedSize(480, 120)
            self.fetch_button.setFixedWidth(460)
        else:
            self.contest_id_for_cf.hide()
            self.contest_id_for_cf_label.hide()
            self.setFixedSize(320, 120)
            self.fetch_button.setFixedWidth(300)

    def fetch(self):
        problem_id = self.id.text().strip()
        if not problem_id:
            QMessageBox.critical(self, "Error", "Please enter a valid problem ID!")
            return
        
        platform = self.site.currentText().strip()

        if platform == "Pbinfo":
            intrare, iesire = fetch.fetch_pbinfo(self.id.text().strip())
        elif platform == "Kilonova":
            intrare, iesire = fetch.fetch_kilonova(self.id.text().strip())
        elif platform == "Codeforces":
            contest_id = self.contest_id_for_cf.text().strip()
            intrare, iesire = fetch.fetch_codeforce(contest_id=contest_id, problem_id=problem_id)
        elif platform == "AtCoder":
            intrare, iesire = fetch.fetch_atcoder(self.id.text().strip())
        else:
            QMessageBox.critical(self, "Error", "Invalid platform!")
            return

        self.right_panel.input_box.clear()
        self.right_panel.input_box.setPlainText(intrare)
        self.right_panel.expected_box.clear()
        self.right_panel.expected_box.setPlainText(iesire)
