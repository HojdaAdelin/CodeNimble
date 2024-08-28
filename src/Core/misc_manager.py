from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTextEdit
from PySide6.QtGui import QTextCursor, QIcon
from PySide6.QtCore import Qt

class MiscManager:
    def __init__(self, text_widget, theme):
        self.text_widget = text_widget
        self.theme = theme

    def find_text(self):
        dialog = QDialog()
        dialog.setWindowTitle("Find Text")
        dialog.setWindowIcon(QIcon("images/png-logo.png"))
        dialog.setFixedSize(300, 100)  # Dezactivează redimensionarea

        layout = QVBoxLayout()

        entry = QLineEdit(dialog)
        entry.setPlaceholderText("Enter text to find")
        layout.addWidget(entry)

        find_button = QPushButton("Find", dialog)
        layout.addWidget(find_button)

        dialog.setLayout(layout)

        # Apply theme
        dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {self.theme['background_color']};
                color: {self.theme['text_color']};
            }}
            QLineEdit {{
                background-color: {self.theme['background_color']};
                color: {self.theme['text_color']};
                border: 1px solid {self.theme['highlight_color']};
            }}
            QPushButton {{
                background-color: {self.theme['button_color']};
                color: {self.theme['text_color']};
            }}
            QPushButton:hover {{
                background-color: {self.theme['button_hover_color']};
            }}
        """)

        def find_action():
            search_text = entry.text().strip()
            if not search_text:
                QMessageBox.warning(dialog, "No Text Entered", "Please enter text to find.")
                return

            cursor = self.text_widget.textCursor()
            if cursor.hasSelection():
                cursor.setPosition(cursor.selectionEnd(), QTextCursor.MoveAnchor)

            found = self.text_widget.find(search_text)  # Fără QTextDocument.FindWholeWords

            if not found:
                cursor.movePosition(QTextCursor.Start)
                self.text_widget.setTextCursor(cursor)
                found = self.text_widget.find(search_text)

            if found:
                cursor = self.text_widget.textCursor()
                cursor.setPosition(cursor.selectionStart(), QTextCursor.MoveAnchor)
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(search_text))
                self.text_widget.setTextCursor(cursor)

        find_button.clicked.connect(find_action)
        dialog.exec()

    def replace_text(self):
        dialog = QDialog()
        dialog.setWindowTitle("Replace Text")
        dialog.setWindowIcon(QIcon("images/png-logo.png"))
        dialog.setFixedSize(400, 150)  # Dezactivează redimensionarea

        layout = QVBoxLayout()

        find_entry = QLineEdit(dialog)
        find_entry.setPlaceholderText("Enter text to find")
        layout.addWidget(find_entry)

        replace_entry = QLineEdit(dialog)
        replace_entry.setPlaceholderText("Enter replacement text")
        layout.addWidget(replace_entry)

        button_layout = QHBoxLayout()

        find_button = QPushButton("Find", dialog)
        button_layout.addWidget(find_button)

        replace_button = QPushButton("Replace", dialog)
        button_layout.addWidget(replace_button)

        replace_all_button = QPushButton("Replace All", dialog)
        button_layout.addWidget(replace_all_button)

        layout.addLayout(button_layout)
        dialog.setLayout(layout)

        # Apply theme
        dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {self.theme['background_color']};
                color: {self.theme['text_color']};
            }}
            QLineEdit {{
                background-color: {self.theme['background_color']};
                color: {self.theme['text_color']};
                border: 1px solid {self.theme['highlight_color']};
            }}
            QPushButton {{
                background-color: {self.theme['button_color']};
                color: {self.theme['text_color']};
            }}
            QPushButton:hover {{
                background-color: {self.theme['button_hover_color']};
            }}
        """)

        def find_action():
            search_text = find_entry.text().strip()
            if not search_text:
                QMessageBox.warning(dialog, "No Text Entered", "Please enter text to find.")
                return

            cursor = self.text_widget.textCursor()
            if cursor.hasSelection():
                cursor.setPosition(cursor.selectionEnd(), QTextCursor.MoveAnchor)

            found = self.text_widget.find(search_text)  # Fără QTextDocument.FindWholeWords

            if not found:
                cursor.movePosition(QTextCursor.Start)
                self.text_widget.setTextCursor(cursor)
                found = self.text_widget.find(search_text)

            if found:
                cursor = self.text_widget.textCursor()
                cursor.setPosition(cursor.selectionStart(), QTextCursor.MoveAnchor)
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(search_text))
                self.text_widget.setTextCursor(cursor)

        def replace_action():
            search_text = find_entry.text().strip()
            replace_text = replace_entry.text().strip()

            if not search_text:
                QMessageBox.warning(dialog, "No Text Entered", "Please enter text to find.")
                return

            cursor = self.text_widget.textCursor()

            # Dacă textul selectat este cel care trebuie înlocuit, se face înlocuirea
            if cursor.hasSelection() and cursor.selectedText() == search_text:
                cursor.insertText(replace_text)

            # Mută cursorul la următoarea apariție
            found = self.text_widget.find(search_text)

            if not found:
                # Dacă textul nu este găsit, începem de la începutul documentului
                cursor.movePosition(QTextCursor.Start)
                self.text_widget.setTextCursor(cursor)
                found = self.text_widget.find(search_text)

            if found:
                cursor = self.text_widget.textCursor()
                cursor.setPosition(cursor.selectionStart(), QTextCursor.MoveAnchor)
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(search_text))
                self.text_widget.setTextCursor(cursor)

        def replace_all_action():
            search_text = find_entry.text().strip()
            replace_text = replace_entry.text().strip()

            if not search_text:
                QMessageBox.warning(dialog, "No Text Entered", "Please enter text to find.")
                return

            cursor = self.text_widget.textCursor()
            cursor.beginEditBlock()

            self.text_widget.moveCursor(QTextCursor.Start)
            while self.text_widget.find(search_text):
                cursor = self.text_widget.textCursor()
                if cursor.selectedText() == search_text:
                    cursor.insertText(replace_text)

            cursor.endEditBlock()

        find_button.clicked.connect(find_action)
        replace_button.clicked.connect(replace_action)
        replace_all_button.clicked.connect(replace_all_action)
        dialog.exec()

    def go_to_line(self):
        dialog = QDialog()
        dialog.setWindowTitle("Go To Line")
        dialog.setWindowIcon(QIcon("images/png-logo.png"))
        dialog.setFixedSize(300, 100)  # Dezactivează redimensionarea

        layout = QVBoxLayout()

        entry = QLineEdit(dialog)
        entry.setPlaceholderText("Enter line number")
        layout.addWidget(entry)

        go_button = QPushButton("Go", dialog)
        layout.addWidget(go_button)

        dialog.setLayout(layout)

        # Apply theme
        dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {self.theme['background_color']};
                color: {self.theme['text_color']};
            }}
            QLineEdit {{
                background-color: {self.theme['background_color']};
                color: {self.theme['text_color']};
                border: 1px solid {self.theme['highlight_color']};
            }}
            QPushButton {{
                background-color: {self.theme['button_color']};
                color: {self.theme['text_color']};
            }}
            QPushButton:hover {{
                background-color: {self.theme['button_hover_color']};
            }}
        """)

        def go_action():
            line_number_str = entry.text().strip()
            if not line_number_str.isdigit():
                QMessageBox.warning(dialog, "Invalid Input", "Please enter a valid line number.")
                return

            line_number = int(line_number_str)
            if line_number <= 0:
                QMessageBox.warning(dialog, "Invalid Line Number", "Line number must be greater than 0.")
                return

            cursor = self.text_widget.textCursor()
            block_number = line_number - 1

            cursor.movePosition(QTextCursor.Start)
            cursor.movePosition(QTextCursor.Down, QTextCursor.MoveAnchor, block_number)
            self.text_widget.setTextCursor(cursor)
            self.text_widget.ensureCursorVisible()

        go_button.clicked.connect(go_action)
        dialog.exec()
