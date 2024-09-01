from PySide6 import QtWidgets, QtCore, QtGui
import os

# Coduri template
cpp_text = """#include <iostream>

int main()
{
    std::cout << "Hello World";
    return 0;
}"""

c_text = """#include <stdio.h>

int main()
{
    printf("Hello World");

    return 0;
}"""

java_text = """public class Main
{
    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}"""

html_text = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    
</body>
</html>"""

competitive_text = """#include <bits/stdc++.h>

using namespace std;

#define ll long long

void solution() {
    
}

int main()
{
    solution();

    return 0;
}"""

def return_content(type):
    if type == "cpp":
        return cpp_text
    elif type == "c":
        return c_text
    elif type == "java":
        return java_text
    elif type == "html":
        return html_text
    elif type == "competitive":
        return competitive_text
    


def apply_theme(widget, theme):
    # Apply the theme to the widget
    palette = widget.palette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(theme['background_color']))
    palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(theme['text_color']))
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(theme['button_color']))
    palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(theme['text_color']))
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(theme['editor_background']))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(theme['line_number_background']))
    palette.setColor(QtGui.QPalette.Text, QtGui.QColor(theme['editor_foreground']))
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(theme['highlight_color']))
    palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(theme['text_color']))
    
    widget.setPalette(palette)

    widget.setStyleSheet(f"""
        QPushButton {{
            background-color: {theme['button_color']};
            color: {theme['text_color']};
        }}
        QPushButton:hover {{
            background-color: {theme['button_hover_color']};
        }}
        QLineEdit {{
            background-color: {theme['editor_background']};
            color: {theme['editor_foreground']};
            border: 1px solid {theme['border_color']};
        }}
        QPlainTextEdit {{
            background-color: {theme['editor_background']};
            color: {theme['editor_foreground']};
            border: 1px solid {theme['border_color']};
        }}
        QListWidget {{
            background-color: {theme['editor_background']};
            color: {theme['editor_foreground']};
            border: 1px solid {theme['border_color']};
        }}
        QListWidget::item:selected {{
            background-color: {theme['item_hover_background_color']};
            color: {theme['item_hover_text_color']};
        }}
        QLabel {{
            color: {theme['text_color']};
        }}
        """)

def create_template(text_widget, file_manager, theme):
    def open_template_window():
        template_window = QtWidgets.QWidget()
        template_window.setWindowTitle("CodeNimble - Create Templates")
        template_window.setWindowIcon(QtGui.QIcon("images/logo.ico"))

        layout = QtWidgets.QVBoxLayout(template_window)

        name_label = QtWidgets.QLabel("Name:")
        name_label.setFont(QtGui.QFont("Arial", 20))
        layout.addWidget(name_label)

        name_box = QtWidgets.QLineEdit()
        name_box.setFont(QtGui.QFont("Arial", 30))
        layout.addWidget(name_box)

        content_label = QtWidgets.QLabel("Text:")
        content_label.setFont(QtGui.QFont("Arial", 20))
        layout.addWidget(content_label)

        text_box = QtWidgets.QPlainTextEdit()
        text_box.setFont(QtGui.QFont("Arial", 16))
        layout.addWidget(text_box)

        apply_theme(template_window, theme)

        def create_template_file():
            template_name_full = name_box.text().strip()
            if '.' in template_name_full:
                template_name, extension = template_name_full.rsplit('.', 1)
            else:
                template_name = template_name_full
                extension = 'txt'  # Default extension if none provided

            template_content = text_box.toPlainText().strip()

            if not template_name:
                QtWidgets.QMessageBox.critical(template_window, "Error", "Template name cannot be empty!")
                return
            
            curr_dir = os.getcwd()
            tmp_folder = os.path.join(curr_dir, 'Templates')
            if not os.path.isdir(tmp_folder):
                os.makedirs(tmp_folder)
            
            template_path = os.path.join(tmp_folder, f"{template_name}.{extension}")

            if os.path.exists(template_path):
                QtWidgets.QMessageBox.critical(template_window, "Error", f"Template '{template_name}' already exists!")
                return

            if not template_content:
                QtWidgets.QMessageBox.critical(template_window, "Error", "Template content cannot be empty!")
                return

            with open(template_path, 'w') as template_file:
                template_file.write(template_content)
            
            QtWidgets.QMessageBox.information(template_window, "Success", f"Template '{template_name}.{extension}' created successfully!")

        create_button = QtWidgets.QPushButton("Create")
        create_button.setFont(QtGui.QFont("Arial", 16))
        create_button.clicked.connect(create_template_file)
        layout.addWidget(create_button)

        template_window.setLayout(layout)
        template_window.resize(460, 560)
        template_window.show()

    open_template_window()

def use_template(text_widget, file_manager, theme, tab_bar):
    def open_use_template_window():
        template_window = QtWidgets.QWidget()
        template_window.setWindowTitle("CodeNimble - Use Templates")
        template_window.setWindowIcon(QtGui.QIcon("images/logo.ico"))

        layout = QtWidgets.QVBoxLayout(template_window)

        search_label = QtWidgets.QLabel("Search:")
        search_label.setFont(QtGui.QFont("Arial", 20))
        layout.addWidget(search_label)

        search_box = QtWidgets.QLineEdit()
        search_box.setFont(QtGui.QFont("Arial", 30))
        layout.addWidget(search_box)

        listbox = QtWidgets.QListWidget()
        listbox.setFont(QtGui.QFont("Arial", 16))
        layout.addWidget(listbox)

        apply_theme(template_window, theme)

        curr_dir = os.getcwd()
        tmp_folder = os.path.join(curr_dir, 'Templates')
        if not os.path.isdir(tmp_folder):
            os.makedirs(tmp_folder)
        
        def update_listbox():
            search_term = search_box.text().strip().lower()
            listbox.clear()
            for file in os.listdir(tmp_folder):
                if search_term in file.lower():
                    listbox.addItem(file)

        search_box.textChanged.connect(update_listbox)
        update_listbox()

        def use_selected_template():
            selected = listbox.currentItem()
            if not selected:
                QtWidgets.QMessageBox.critical(template_window, "Error", "No template selected!")
                return
            
            template_file = selected.text()
            template_path = os.path.join(tmp_folder, template_file)
            
            with open(template_path, 'r') as file:
                template_content = file.read()
            
            _, extension = os.path.splitext(template_file)
            
            text_widget.clear()
            text_widget.insertPlainText(template_content)
            file_manager.create_file(template_content, extension, tab_bar)
            
            QtWidgets.QMessageBox.information(template_window, "Success", f"Used template {template_file}")

        use_button = QtWidgets.QPushButton("Use")
        use_button.setFont(QtGui.QFont("Arial", 16))
        use_button.clicked.connect(use_selected_template)
        layout.addWidget(use_button)

        template_window.setLayout(layout)
        template_window.resize(400, 500)
        template_window.show()

    open_use_template_window()
