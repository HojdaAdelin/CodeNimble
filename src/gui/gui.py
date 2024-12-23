import sys
from PyQt6.QtWidgets import QMainWindow, QMenuBar, QVBoxLayout, QWidget
from PyQt6.QtGui import QIcon, QAction
from gui.editor import EditorWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup()
        self.setup_ui()

    def setup(self):
        self.setWindowTitle("CodeNimble")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(400, 300)
        self.setWindowIcon(QIcon("logo.png"))  

    def set_theme(self):
        self.background_color = "#121212"
        self.text_color = "#ffffff"
        self.button_color = "#1e1e1e"
        self.button_hover_color = "#333333"
        self.item_hover_background_color = "#444444"
        self.item_hover_text_color = "#ffffff"
        self.border_color = "#555555"
        self.separator_color = "#666666"
        font_family = "Fire Code" 
        font_size = "16px"

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.background_color};
                color: {self.text_color};
                font-family: {font_family};
                font-size: {font_size};
            }}
            QPushButton {{
                background-color: {self.button_color};
                color: {self.text_color};
            }}
            QPushButton:hover {{
                background-color: {self.button_hover_color};
            }}
            QMenuBar {{
                background-color: {self.background_color};
                color: {self.text_color};
                font-family: {font_family};
                font-size: 16px;
            }}
            QMenuBar::item {{
                font-family: {font_family};
                font-size: {font_size};
            }}
            QMenuBar::item:selected {{
                background-color: {self.item_hover_background_color};
                color: {self.item_hover_text_color};
            }}
            QMenu {{
                background-color: {self.background_color};
                color: {self.text_color};
                border: 1px solid {self.border_color};
                margin: 0;
                padding: 0;
                font-family: {font_family};
                font-size: {font_size};
            }}
            QMenu::item {{
                padding: 5px 10px;
                font-family: {font_family};
                font-size: {font_size};
                margin: 0; 
            }}
            QMenu::item:selected {{
                background-color: {self.item_hover_background_color};
                color: {self.item_hover_text_color};
                padding: 5px 10px; 
            }}
            QMenu::separator {{
                height: 1px;
                background: {self.separator_color};
            }}
        """)

    def setup_menu(self):
        """Create and set up the main menu bar."""
        menu_bar = self.menuBar()

        # Home Menu
        home_menu = menu_bar.addMenu("Home")
        home_menu.addAction("Version")
        home_menu.addAction("Changelog")
        home_menu.addAction("Site")
        home_menu.addSeparator()
        home_menu.addAction("Exit")

        # File Menu
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction("New File")
        file_menu.addAction("Open")
        file_menu.addSeparator()
        file_menu.addAction("Open Folder")
        file_menu.addAction("Close Folder")
        file_menu.addSeparator()
        file_menu.addAction("Save")
        file_menu.addAction("Save as")

        # Edit Menu
        edit_menu = menu_bar.addMenu("Edit")
        edit_menu.addAction("Undo")
        edit_menu.addAction("Redo")
        edit_menu.addSeparator()
        edit_menu.addAction("Cut")
        edit_menu.addAction("Copy")
        edit_menu.addAction("Paste")
        edit_menu.addAction("Delete")
        edit_menu.addAction("Clear")
        edit_menu.addAction("Select All")
        edit_menu.addSeparator()
        edit_menu.addAction("Find")
        edit_menu.addAction("Replace")
        edit_menu.addAction("Go to")

        # View Menu
        view_menu = menu_bar.addMenu("View")
        view_menu.addAction("Zoom In")
        view_menu.addAction("Zoom Out")
        view_menu.addAction("Reset Zoom")
        view_menu.addAction("Fullscreen")

    def setup_ui(self):
        self.setup_menu()
        self.set_theme()

        # Main Widget with layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Editor
        self.editor_widget = EditorWidget()
        layout.addWidget(self.editor_widget)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

