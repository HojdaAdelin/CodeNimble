from PySide6.QtWidgets import QFileDialog, QTextEdit, QPlainTextEdit, QDialog, QPushButton, QVBoxLayout, QLineEdit
from PySide6.QtCore import QDir
from PySide6.QtGui import QIcon
import os

class FileManager:
    def __init__(self):
        self.opened_filename = None
        self.opened_foldername = None

    def open_file(self, text_widget: QTextEdit,tab_bar, file_dialog_title="Open File"):
        filename, _ = QFileDialog.getOpenFileName(None, file_dialog_title, "", "All files (*.*)")
        
        if filename:
            tab_bar.add_tab(filename)
            self.opened_filename = filename

            with open(filename, "r", encoding="utf-8") as file:
                file_content = file.read()

                text_widget.clear()
                text_widget.setPlainText(file_content)

    def save_file(self, text_widget: QTextEdit):
        
        if self.opened_filename:
            content = text_widget.toPlainText()

            with open(self.opened_filename, "w", encoding="utf-8") as file:
                file.write(content)
            print(f"Saved: {self.opened_filename}")
        else:
            self.save_as_file(text_widget)

    def save_as_file(self, text_widget: QTextEdit):
        
        content = text_widget.toPlainText()
        filename, _ = QFileDialog.getSaveFileName(None, "Save As", os.getcwd(), "Text files (*.txt);;All files (*.*)")

        if filename:
            self.opened_filename = filename

            with open(filename, "w", encoding="utf-8") as file:
                file.write(content)
            print(f"Saved As: {filename}")

    def get_file_content(self, path=None):
        if path:
            with open(path, "r", encoding="utf-8") as file:
                file_content = file.read()
        else:
            with open(self.opened_filename, "r", encoding="utf-8") as file:
                file_content = file.read()

        return file_content

    def change_opened_filename(self, filename):
        self.opened_filename = filename

    def get_opened_filename(self):
        return self.opened_filename
    
    def get_opened_foldername(self):
        return self.opened_foldername
    
    def open_folder(self, treeview,win, folder_dialog_title="Open Folder"):
        foldername = QFileDialog.getExistingDirectory(None, folder_dialog_title, "", QFileDialog.ShowDirsOnly)

        if foldername:
            self.opened_foldername = foldername
            treeview.model.setRootPath(foldername)
            treeview.tree.setRootIndex(treeview.model.index(foldername))
            win.splitter.setSizes([250] + win.splitter.sizes()[1:])

    def close_folder(self, treeview, win):
        if self.opened_foldername:
            self.opened_foldername = None
            treeview.model.setRootPath(QDir.rootPath())
            treeview.tree.setRootIndex(treeview.model.index(QDir.rootPath()))
            treeview.tree.setRootIndex(treeview.model.index("")) 
            win.splitter.setSizes([0] + win.splitter.sizes()[1:])

    def new_file(self, tab_bar, theme):
        self.dialog = QDialog()
        self.dialog.setWindowTitle("New File")
        self.dialog.setWindowIcon(QIcon("images/png-logo.png"))

        layout = QVBoxLayout()

        # Entry field for file name
        self.text_box = QLineEdit(self.dialog)
        self.text_box.setPlaceholderText("Enter file name")
        layout.addWidget(self.text_box)

        # Button to create the file
        self.create_button = QPushButton("Create", self.dialog)
        layout.addWidget(self.create_button)

        # Apply the theme when the dialog is created
        self.apply_theme(theme)

        def create_file():
            filename = self.text_box.text().strip()
            if filename:
                if not "." in filename:
                    filename += ".txt"

                # Determine the file path based on opened_foldername or default path
                if self.opened_foldername:
                    filepath = os.path.join(self.opened_foldername, filename)
                else:
                    filepath = os.path.join(os.getcwd(), filename)

                try:
                    with open(filepath, "x") as file:
                        self.opened_filename = filepath
                        tab_bar.add_tab(filepath)
                except FileExistsError:
                    pass

            self.dialog.close()

        self.create_button.clicked.connect(create_file)

        self.dialog.setLayout(layout)
        self.dialog.exec()

    def apply_theme(self, theme):
        if self.dialog and self.text_box and self.create_button:
            # Apply styles to the dialog
            self.dialog.setStyleSheet(f"""
                QDialog {{
                    background-color: {theme['background_color']};
                }}
            """)

            # Apply styles to the text box
            self.text_box.setStyleSheet(f"""
                QLineEdit {{
                    background-color: {theme['editor_background']};
                    color: {theme['text_color']};
                    border: none;
                }}
            """)

            # Apply styles to the create button
            self.create_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {theme['button_color']};
                    color: {theme['text_color']};
                    border: none;
                    padding: 5px 10px;
                }}
                QPushButton:hover {{
                    background-color: {theme['button_hover_color']};
                }}
            """)

    def create_file(self,text, ext, tab_bar):
        if self.opened_foldername:
            filename = self.opened_foldername +"/template" + ext 
        else:
            filename = "template" + ext

        count = 1
        while os.path.exists(filename):
            if self.opened_foldername:
                filename = self.opened_foldername + f"/template{count}" + ext
            else:
                filename = f"template{count}" + ext
            count += 1

        with open(filename, "w", encoding="utf-8") as file:
            file.write(text)
        self.opened_filename = filename
        tab_bar.add_tab(filename)

    def return_extension(self, path=None):
        if path:
            filename = path
        elif self.opened_filename:
            filename = self.opened_filename
        else:
            return ""  

        _, ext = os.path.splitext(filename)
        return ext if ext else ""