from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QFrame, QVBoxLayout, QHBoxLayout, QScrollBar
from PySide6.QtGui import QTextCursor, QColor, QFont, QIcon
from PySide6.QtCore import Qt


class OutputComparator(QMainWindow):
    def __init__(self, right_panel, theme, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Setează dimensiunea ferestrei
        self.setGeometry(100, 100, 450, 300)
        self.setWindowTitle("Output Comparator")
        self.setWindowIcon(QIcon("images/logo.ico"))
        
        # Creează un frame pentru a conține TextBox-ul și scrollbars
        frame = QFrame(self)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        # Creează TextBox-ul folosind QTextEdit
        self.textbox = QTextEdit(self)
        self.textbox.setReadOnly(True)
        self.textbox.setFont(QFont("Consolas", 16))  # Font size is set to 10 since 30 might be too large
        layout.addWidget(self.textbox)
        
        # Creează scrollbars și le asociază cu TextBox-ul
        self.scrollbar_y = QScrollBar(Qt.Vertical)
        self.textbox.setVerticalScrollBar(self.scrollbar_y)
        self.scrollbar_x = QScrollBar(Qt.Horizontal)
        self.textbox.setHorizontalScrollBar(self.scrollbar_x)
        
        self.setCentralWidget(frame)

        # Aplică tema
        self.apply_theme(theme)
        
        # Compară și afișează rezultatele
        self.compare_and_display(right_panel)

    def apply_theme(self, theme):
        # Setează culorile în funcție de tema primită
        self.textbox.setStyleSheet(f"""
            background-color: {theme.get('background_color', '#333333')};
            color: {theme.get('text_color', '#ffffff')};
            selection-background-color: {theme.get('selection_background_color', '#333333')};
        """)
        
        self.scrollbar_y.setStyleSheet(f"""
            QScrollBar:vertical {{
                background-color: {theme.get('background_color', '#333333')};
            }}
            QScrollBar::handle:vertical {{
                background-color: {theme.get('button_color', '#555555')};
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {theme.get('button_hover_color', '#777777')};
            }}
        """)
        
        self.scrollbar_x.setStyleSheet(f"""
            QScrollBar:horizontal {{
                background-color: {theme.get('background_color', '#333333')};
            }}
            QScrollBar::handle:horizontal {{
                background-color: {theme.get('button_color', '#555555')};
            }}
            QScrollBar::handle:horizontal:hover {{
                background-color: {theme.get('button_hover_color', '#777777')};
            }}
        """)

    def compare_and_display(self, right_panel):
        # Obține textul din fiecare TextBox și îl transformă în liste
        output_list = right_panel.output_box.toPlainText().split()
        expected_list = right_panel.expected_box.toPlainText().split()
        
        # Curăță TextBox-ul
        self.textbox.clear()
        
        # Compară elementele din cele două liste și formatează textul
        for i, (output, expected) in enumerate(zip(output_list, expected_list), start=1):
            result = f"{i}. {expected} ("
            if output == expected:
                result += "correct)"
                self.textbox.setTextColor(QColor("green"))
            else:
                result += "incorrect)"
                self.textbox.setTextColor(QColor("#ff6363"))
            self.textbox.append(result)
        
        # Dacă există elemente în `expected_list` care nu au pereche în `output_list`
        if len(expected_list) > len(output_list):
            for i, expected in enumerate(expected_list[len(output_list):], start=len(output_list) + 1):
                result = f"{i}. {expected} (incorrect)"
                self.textbox.setTextColor(QColor("#ff6363"))
                self.textbox.append(result)
        
        # Mută cursorul la începutul TextBox-ului
        self.textbox.moveCursor(QTextCursor.Start)