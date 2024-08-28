from PySide6.QtWidgets import QWidget, QLabel, QTextEdit, QPushButton, QGridLayout, QSizePolicy
from PySide6.QtCore import Qt

from GUI import fetch_window
from GUI import diff

class RightPanel(QWidget):
    def __init__(self, theme, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.theme = theme
        # Crearea layout-ului principal
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)
        self.layout.setContentsMargins(10, 10, 10, 10)  # Margini pentru întregul layout
        self.layout.setSpacing(10)  # Spațiere între widget-uri
        
        # Configurarea grid-ului
        self.layout.setColumnStretch(0, 1)
        self.layout.setRowStretch(0, 0)
        self.layout.setRowStretch(1, 1)
        self.layout.setRowStretch(2, 0)
        self.layout.setRowStretch(3, 1)
        self.layout.setRowStretch(4, 0)
        self.layout.setRowStretch(5, 1)
        self.layout.setRowStretch(6, 0)
        self.layout.setRowStretch(7, 0)

        # Label-ul pentru input
        self.input_label = QLabel("Input", self)
        self.layout.addWidget(self.input_label, 0, 0, Qt.AlignHCenter)

        # Textbox pentru input
        self.input_box = QTextEdit(self)
        self.input_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.input_box.setMinimumHeight(100)
        self.layout.addWidget(self.input_box, 1, 0)

        # Label-ul pentru output
        self.output_label = QLabel("Output", self)
        self.layout.addWidget(self.output_label, 2, 0, Qt.AlignHCenter)

        # Textbox pentru output
        self.output_box = QTextEdit(self)
        self.output_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.output_box.setMinimumHeight(100)
        self.layout.addWidget(self.output_box, 3, 0)

        # Label-ul pentru expected output
        self.expected_label = QLabel("Expected Output", self)
        self.layout.addWidget(self.expected_label, 4, 0, Qt.AlignHCenter)

        # Textbox pentru expected output
        self.expected_box = QTextEdit(self)
        self.expected_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.expected_box.setMinimumHeight(100)
        self.layout.addWidget(self.expected_box, 5, 0)

        # Butonul pentru comparare
        self.diff = QPushButton("Output comparator", self, clicked=self.diff_core)
        self.diff.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.diff.setMinimumHeight(40)
        self.layout.addWidget(self.diff, 6, 0)

        # Butonul pentru fetch
        self.fetch = QPushButton("Fetch test cases", self, clicked=self.fetch_core)
        self.fetch.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.fetch.setMinimumHeight(40)
        self.layout.addWidget(self.fetch, 7, 0)

        # Aplicarea temei
        self.apply_theme(self.theme)

    def diff_core(self):
        self.diff_win = diff.OutputComparator(self, self.theme)
        self.diff_win.show()

    def fetch_core(self):
        self.fetch_win = fetch_window.FetchWindow(self, self.theme)
        self.fetch_win.show()

    def apply_theme(self, theme):
        # Aplicarea temei pentru fiecare element din RightPanel
        self.setStyleSheet(f"""
            background-color: {theme.get("background_color")};
            color: {theme.get("text_color")};
        """)

        self.input_label.setStyleSheet(f"color: {theme.get('text_color')};")
        self.output_label.setStyleSheet(f"color: {theme.get('text_color')};")
        self.expected_label.setStyleSheet(f"color: {theme.get('text_color')};")

        self.input_box.setStyleSheet(f"""
            background-color: {theme.get("editor_background")};
            color: {theme.get("editor_foreground")};
            border: 1px solid {theme.get("border_color")};
            padding: 5px;
        """)
        self.output_box.setStyleSheet(f"""
            background-color: {theme.get("editor_background")};
            color: {theme.get("editor_foreground")};
            border: 1px solid {theme.get("border_color")};
            padding: 5px;
        """)
        self.expected_box.setStyleSheet(f"""
            background-color: {theme.get("editor_background")};
            color: {theme.get("editor_foreground")};
            border: 1px solid {theme.get("border_color")};
            padding: 5px;
        """)
        button_style = f"""
            QPushButton {{
                background-color: {theme.get("button_color")};
                color: {theme.get("text_color")};
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: {theme.get("button_hover_color")};
            }}
        """
        self.diff.setStyleSheet(button_style)
        self.fetch.setStyleSheet(button_style)
