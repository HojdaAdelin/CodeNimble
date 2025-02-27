import os
from PySide6 import QtWidgets, QtGui

class ThemeManager:
    def __init__(self, win):
        self.win = win

    def use_theme(self, theme):
        self.win.change_theme(theme)

    def manager_view(self):
        def open_manager_view_window():
            theme_window = QtWidgets.QWidget()
            theme_window.setWindowTitle("Theme Manager")
            theme_window.setWindowIcon(QtGui.QIcon("images/logo.ico"))

            layout = QtWidgets.QVBoxLayout(theme_window)

            search_label = QtWidgets.QLabel("Search:")
            search_label.setFont(QtGui.QFont("Arial", 20))
            layout.addWidget(search_label)

            search_box = QtWidgets.QLineEdit()
            search_box.setFont(QtGui.QFont("Arial", 30))
            layout.addWidget(search_box)

            listbox = QtWidgets.QListWidget()
            listbox.setFont(QtGui.QFont("Arial", 16))
            layout.addWidget(listbox)
            tm = self.win.get_theme()
            theme_window.setStyleSheet(f"""
                QWidget {{
                    background-color: {tm['background_color']};
                }}
                QPushButton {{
                        background-color: {tm.get("button_color")};
                        color: {tm.get("text_color")};
                        padding: 5px;
                        border: 1px solid {tm.get('border_color')};
                }}
                QPushButton:hover {{
                    background-color: {tm.get("button_hover_color")};
                }}
                QLineEdit {{
                    background-color: {tm.get("editor_background")};
                    color: {tm.get("editor_foreground")};
                    border: 1px solid {tm.get("border_color")};
                    padding: 5px;
                }}
                QPlainTextEdit {{
                    background-color: {tm.get("editor_background")};
                    color: {tm.get("editor_foreground")};
                    border: 1px solid {tm.get("border_color")};
                    padding: 5px;
                }}
                QListWidget {{
                    background-color: {tm['editor_background']};
                    color: {tm['editor_foreground']};
                    border: 1px solid {tm['border_color']};
                }}
                QListWidget::item:selected {{
                    background-color: {tm['item_hover_background_color']};
                    color: {tm['item_hover_text_color']};
                }}
                QLabel {{
                    color: {tm['text_color']};
                }}
                """)

            tmp_folder = "Themes"
            if not os.path.isdir(tmp_folder):
                os.makedirs(tmp_folder)

            def update_listbox():
                search_term = search_box.text().strip().lower()
                listbox.clear()
                for file in os.listdir(tmp_folder):
                    if search_term in file.lower() and file.endswith('.json'):
                        listbox.addItem(file)

            search_box.textChanged.connect(update_listbox)
            update_listbox()

            def use_selected_theme():
                selected = listbox.currentItem()
                if not selected:
                    QtWidgets.QMessageBox.critical(theme_window, "Error", "No theme selected!")
                    return
                
                theme_file = selected.text()
                theme_name, _ = os.path.splitext(theme_file)  # Remove the .json extension
                self.use_theme(theme_name)

            use_button = QtWidgets.QPushButton("Use")
            use_button.setFont(QtGui.QFont("Arial", 16))
            use_button.clicked.connect(use_selected_theme)
            layout.addWidget(use_button)

            theme_window.setLayout(layout)
            theme_window.resize(400, 500)
            theme_window.show()

        open_manager_view_window()
