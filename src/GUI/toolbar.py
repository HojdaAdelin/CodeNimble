from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout

class ToolBar(QWidget):
    def __init__(self, theme, win):
        super().__init__()
        self.theme = theme
        self.win = win
        # Layout
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.submit_button = QPushButton(self, text="Submit code", clicked=self.submit_core)
        self.layout.addWidget(self.submit_button)
        self.apply_theme(self.theme)

    def submit_core(self):
        self.win.pbinfo_tools_core()
        
    def apply_theme(self, theme):
        self.setStyleSheet(f"""background-color: {theme['background_color']};""")
        button_style = f"""
            QPushButton {{
                background-color: {theme.get("button_color")};
                color: {theme.get("text_color")};
                padding: 5px;
                border: 1px solid {theme.get('border_color')};
            }}
            QPushButton:hover {{
                background-color: {theme.get("button_hover_color")};
            }}
        """
        self.submit_button.setStyleSheet(button_style)
        
