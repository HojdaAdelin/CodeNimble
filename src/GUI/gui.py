from PySide6.QtWidgets import QSplitter, QMainWindow, QMenu, QVBoxLayout, QWidget
from PySide6.QtGui import QIcon, QAction, QTextCursor
from PySide6.QtCore import Qt, QCoreApplication
import json
from GUI import text_editor
from GUI import info_win
from GUI import profile
from GUI import treeview
from GUI import status_bar
from GUI import tab_bar
from GUI import right_panel
from GUI import paint
from GUI import kilo_tools
from GUI import toolbar
from Core import run
from Core import templates
from Core import web
from Core import file_manager
from Core import edit_manager
from Core import misc_manager
from Core import view_manager
from Core import theme_manager
from Core import session
from Tools import pbinfo
from Update import internal
import sys
import os

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        # Instance
        self.file_manager = file_manager.FileManager()
        self.theme_manager = theme_manager.ThemeManager(self)

        self.setWindowTitle("Code Nimble")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(850, 400)
        self.setWindowIcon(QIcon('images/png-logo.png'))
        if not os.path.isfile("config.json"):
            default_config = {
                "font_family": "Arial",
                "font_size": "20px",
                "editor_font_size": "20",
                "profile_name": "user",
                "theme": "dark",
                "version": "",
                "session": {
                    "opened_folder": "",
                    "opened_file": ""
                },
                "credits": {
                    "username": "",
                    "password": ""
                }
            }
            with open('config.json', 'w') as file:
                json.dump(default_config, file, indent=4)
    
        with open('config.json', 'r') as file:
                self.config = json.load(file)
        with open(f'Themes/{self.config.get("theme")}.json', 'r') as file:
            themes = json.load(file)
        
        self.theme = themes
        self.view_manager = view_manager.ViewManager(self.config, self)
        # Crearea meniului
        self.create_menu()

        # Setarea layout-ului și widget-ului principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Modifică layout-ul principal la QVBoxLayout pentru a adăuga status bar-ul în partea de jos
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.central_widget.setLayout(self.layout)

        # Crearea splitter-ului pentru organizarea TreeView și a editorului
        self.splitter = QSplitter(Qt.Horizontal)

        # Adăugarea splitter-ului în layout
        self.layout.addWidget(self.splitter)

        # Left frame
        self.left_panel = QWidget()

        self.left_layout = QVBoxLayout(self.left_panel)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(0)

        self.tree_view = treeview.TreeView(self.theme, self)

        self.left_panel.setMinimumWidth(250) 
        self.left_panel.setMaximumWidth(400)

        self.tool_bar = toolbar.ToolBar(self.theme, self)

        self.left_layout.addWidget(self.tree_view)
        self.left_layout.addWidget(self.tool_bar)
        self.splitter.addWidget(self.left_panel)

        # Configurarea editorului de cod
        self.editor = text_editor.CodeEditor(self.config, self.theme)
        self.tab_bar = tab_bar.TabBar(self.theme, self.editor, self.file_manager)
        self.editor.setMinimumWidth(600)
        self.tab_bar.setFixedHeight(0)
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(0)
        self.container_layout.addWidget(self.tab_bar)
        self.container_layout.addWidget(self.editor)
        self.edit_manager = edit_manager.EditManager(self.editor)
        self.splitter.addWidget(self.container)

        self.right_panel = right_panel.RightPanel(self.theme, self)
        self.right_panel.setMaximumWidth(500)
        self.right_panel.setMinimumWidth(300)
        self.splitter.addWidget(self.right_panel)

        # Configurarea dimensiunilor splitter-ului
        self.splitter.setSizes([0, 600, 0]) 
        self.splitter.setStretchFactor(0, 1)  
        self.splitter.setStretchFactor(1, 3)  
        self.splitter.setStretchFactor(2, 1)

        self.status_bar = status_bar.StatusBar(self.editor, self.theme, self)
        self.status_bar.update_stats()
        self.status_bar.setFixedHeight(30)
        self.editor.textChanged.connect(self.status_bar.update_stats)
        self.layout.addWidget(self.status_bar)

        # Aplicarea temei "dark"
        self.load_theme()
        session.session_engine(self)


    def create_menu(self):
        menubar = self.menuBar()
        # Crearea meniurilor și acțiunilor
        home_menu = QMenu("Home", self)
        file_menu = QMenu("File", self)
        edit_menu = QMenu("Edit", self)
        view_menu = QMenu("View", self)
        template_menu = QMenu("Templates", self)
        textures_menu = QMenu("Textures", self)
        utility_menu = QMenu("Utility", self)

        # Crearea acțiunilor pentru Home
        version_action = QAction("Version", self)
        version_action.triggered.connect(self.open_version_win)
        home_menu.addAction(version_action)
        check_for_updates_action = QAction("Check for updates", self)
        check_for_updates_action.triggered.connect(self.update_core)
        home_menu.addAction(check_for_updates_action)
        log_action = QAction("Change log", self)
        log_action.triggered.connect(self.log_web)
        home_menu.addAction(log_action)
        site_action = QAction("Site", self)
        site_action.triggered.connect(self.site_web)
        home_menu.addAction(site_action)
        bugs_action = QAction("Report bugs", self)
        bugs_action.triggered.connect(self.bugs_web)
        home_menu.addAction(bugs_action)
        home_menu.addSeparator()
        profile_action = QAction("Profile", self)
        profile_action.triggered.connect(self.open_profile_win)
        home_menu.addAction(profile_action)
        home_menu.addSeparator()
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_app)
        home_menu.addAction(exit_action)

        # Crearea acțiunilor pentru File
        new_file_action = QAction("New File", self, shortcut="Ctrl+N")
        new_file_action.triggered.connect(self.new_file_core)
        file_menu.addAction(new_file_action)
        open_file_action = QAction("Open", self, shortcut="Ctrl+O")
        open_file_action.triggered.connect(self.open_file_core)
        file_menu.addAction(open_file_action)
        file_menu.addSeparator()
        open_folder_action = QAction("Open Folder", self, shortcut="Ctrl+K")
        open_folder_action.triggered.connect(self.open_folder_core)
        file_menu.addAction(open_folder_action)
        close_folder_action = QAction("Close Folder", self)
        close_folder_action.triggered.connect(self.close_folder_core)
        file_menu.addAction(close_folder_action)
        file_menu.addSeparator()
        save_file_action = QAction("Save", self, shortcut="Ctrl+S")
        save_file_action.triggered.connect(self.save_file_core)
        file_menu.addAction(save_file_action)
        save_as_file_action = QAction("Save as", self, shortcut="Ctrl+Shift+S")
        save_as_file_action.triggered.connect(self.save_as_file_core)
        file_menu.addAction(save_as_file_action)
        file_menu.addSeparator()
        save_session_action = QAction("Save session", self)
        save_session_action.triggered.connect(self.save_session_core)
        file_menu.addAction(save_session_action)
        reset_session_action = QAction("Reset session", self)
        reset_session_action.triggered.connect(self.reset_session_core)
        file_menu.addAction(reset_session_action)

        # Crearea acțiunilor pentru Edit
        undo_action = QAction("Undo", self, shortcut="Ctrl+Z")
        undo_action.triggered.connect(self.undo_core)
        edit_menu.addAction(undo_action)
        redo_action = QAction("Redo", self, shortcut="Ctrl+Y")
        redo_action.triggered.connect(self.redo_core)
        edit_menu.addAction(redo_action)
        edit_menu.addSeparator()
        cut_action = QAction("Cut", self, shortcut="Ctrl+X")
        cut_action.triggered.connect(self.cut_core)
        edit_menu.addAction(cut_action)
        copy_action = QAction("Copy", self, shortcut="Ctrl+C")
        copy_action.triggered.connect(self.copy_core)
        edit_menu.addAction(copy_action)
        paste_action = QAction("Paste", self, shortcut="Ctrl+P")
        paste_action.triggered.connect(self.paste_core)
        edit_menu.addAction(paste_action)
        delete_action = QAction("Delete", self, shortcut="Ctrl+D")
        delete_action.triggered.connect(self.delete_core)
        edit_menu.addAction(delete_action)
        clear_action = QAction("Clear", self, shortcut="Ctrl+Alt+C")
        clear_action.triggered.connect(self.clear_core)
        edit_menu.addAction(clear_action)
        select_action = QAction("Select all", self, shortcut="Ctrl+A")
        select_action.triggered.connect(self.select_core)
        edit_menu.addAction(select_action)
        edit_menu.addSeparator()
        find_action = QAction("Find", self, shortcut="Ctrl+F")
        find_action.triggered.connect(self.find_core)
        edit_menu.addAction(find_action)
        replace_action = QAction("Replace", self, shortcut="Ctrl+H")
        replace_action.triggered.connect(self.replace_core)
        edit_menu.addAction(replace_action)
        gotoline_action = QAction("Go to line", self, shortcut="Ctrl+G")
        gotoline_action.triggered.connect(self.go_to_line_core)
        edit_menu.addAction(gotoline_action)

        # Crearea acțiunilor pentru View
        zoom_in_action = QAction("Zoom in", self, shortcut="Ctrl+=")
        zoom_in_action.triggered.connect(self.zoom_in_core)
        view_menu.addAction(zoom_in_action)
        zoom_out_action = QAction("Zoom out", self, shortcut="Ctrl+-")
        zoom_out_action.triggered.connect(self.zoom_out_core)
        view_menu.addAction(zoom_out_action)
        reset_out_action = QAction("Reset zoom", self)
        reset_out_action.triggered.connect(self.reset_zoom_core)
        view_menu.addAction(reset_out_action)
        fullscreen_action = QAction("Fullscreen", self, shortcut="F11")
        fullscreen_action.triggered.connect(self.fullscreen_core)
        view_menu.addAction(fullscreen_action)
        view_menu.addSeparator()
        statusbar_action = QAction("Status Bar", self)
        statusbar_action.triggered.connect(self.status_bar_core)
        view_menu.addAction(statusbar_action)
        left_panel_action = QAction("Left Panel", self, shortcut="Ctrl+B")
        left_panel_action.triggered.connect(self.left_panel_core)
        view_menu.addAction(left_panel_action)
        right_panel_action = QAction("Right Panel", self, shortcut="Ctrl+Alt+B")
        right_panel_action.triggered.connect(self.right_panel_core)
        view_menu.addAction(right_panel_action)

        # Crearea acțiunilor pentru Templates
        cpp_template_action = QAction("C++", self)
        cpp_template_action.triggered.connect(self.cpp_template_core)
        c_template_action = QAction("C", self)
        c_template_action.triggered.connect(self.c_template_core)
        java_template_action = QAction("Java", self)
        java_template_action.triggered.connect(self.java_template_core)
        html_template_action = QAction("Html", self)
        html_template_action.triggered.connect(self.html_template_core)
        comp_template_action = QAction("C++ Competitive", self)
        comp_template_action.triggered.connect(self.comp_template_core)
        auth_template_action = QAction("Author Details", self)
        auth_template_action.triggered.connect(self.auth_details)
        template_menu.addAction(cpp_template_action)
        template_menu.addAction(c_template_action)
        template_menu.addAction(java_template_action)
        template_menu.addAction(html_template_action)
        template_menu.addAction(comp_template_action)
        template_menu.addAction(auth_template_action)
        template_menu.addSeparator()
        create_template_action = QAction("Create Template", self)
        create_template_action.triggered.connect(self.create_template_core)
        template_menu.addAction(create_template_action)
        use_template_action = QAction("Use Template", self, shortcut="Ctrl+Shift+T")
        use_template_action.triggered.connect(self.use_template_core)
        template_menu.addAction(use_template_action)
        #template_menu.addAction(QAction("Snippets Code", self))

        # Crearea acțiunilor pentru Textures
        light_theme_action = QAction("Light theme", self)
        light_theme_action.triggered.connect(self.light_theme_core)
        textures_menu.addAction(light_theme_action)
        dark_theme_action = QAction("Dark theme", self)
        dark_theme_action.triggered.connect(self.dark_theme_core)
        textures_menu.addAction(dark_theme_action)
        ocean_theme_action = QAction("Ocean theme", self)
        ocean_theme_action.triggered.connect(self.ocean_theme_core)
        textures_menu.addAction(ocean_theme_action)
        dark_blue_theme_action = QAction("Dark-blue theme", self)
        dark_blue_theme_action.triggered.connect(self.dark_blue_theme_core)
        textures_menu.addAction(dark_blue_theme_action)
        textures_menu.addSeparator()
        theme_changer_core = QAction("Theme changer", self)
        theme_changer_core.triggered.connect(self.theme_view_core)
        textures_menu.addAction(theme_changer_core)

        # Crearea acțiunilor pentru Utility
        run_action = QAction("Run", self, shortcut="F5")
        run_action.triggered.connect(self.run_core)
        utility_menu.addAction(run_action)
        pre_input_run_action = QAction("Run with pre-input", self)
        pre_input_run_action.triggered.connect(self.pre_input_run_core)
        utility_menu.addAction(pre_input_run_action)
        paint_action = QAction("Paint Mode", self, shortcut="Ctrl+P")
        paint_action.triggered.connect(self.paint_core)
        utility_menu.addAction(paint_action)
        utility_menu.addSeparator()
        pbinfo_tools_action = QAction("Submit code", self)
        pbinfo_tools_action.triggered.connect(self.pbinfo_tools_core)
        utility_menu.addAction(pbinfo_tools_action)
        kilo_tools_action = QAction("Kilonova tools", self)
        kilo_tools_action.triggered.connect(self.kilo_tools_core)
        utility_menu.addAction(kilo_tools_action)

        # Adăugarea meniurilor la menubar
        menubar.addMenu(home_menu)
        menubar.addMenu(file_menu)
        menubar.addMenu(edit_menu)
        menubar.addMenu(view_menu)
        menubar.addMenu(template_menu)
        menubar.addMenu(textures_menu)
        menubar.addMenu(utility_menu)

    def update_core(self):
        internal.check_for_updates()

    def auth_details(self):
        author_info = "// Author: \n// School: \n// Date: \n// Specific algorithm:\n"
        cursor = self.editor.textCursor() 
        cursor.movePosition(QTextCursor.Start)  
        cursor.insertText(author_info + "\n")  
        self.editor.setTextCursor(cursor) 

    def save_session_core(self):
        session.save_session(self.file_manager)

    def reset_session_core(self):
        session.reset_session()

    def pbinfo_tools_core(self):
        self.pbinfo_win = pbinfo.PbinfoInterface(self.editor, self.theme, self.config,parent=self)
        self.pbinfo_win.show()

    def kilo_tools_core(self):
        self.kilo_win = kilo_tools.Kilotools(self.theme,parent=self)
        self.kilo_win.show()

    def dark_theme_core(self):
        self.theme_manager.use_theme("dark")
    def light_theme_core(self):
        self.theme_manager.use_theme("light")
    def ocean_theme_core(self):
        self.theme_manager.use_theme("ocean")
    def dark_blue_theme_core(self):
        self.theme_manager.use_theme("dark-blue")

    def theme_view_core(self):
        self.theme_win = self.theme_manager.manager_view()

    def pre_input_run_core(self):
        run.pre_input_run(self.editor, self.right_panel, self.file_manager,self)

    def run_core(self):
        run.run(self.editor, self.file_manager,self)

    def paint_core(self):
        self.paint_window = paint.PaintApp(self.theme,parent=self)
        self.paint_window.show()

    def cpp_template_core(self):
        self.file_manager.create_file(templates.return_content("cpp"), ".cpp", self.tab_bar)

    def html_template_core(self):
        self.file_manager.create_file(templates.return_content("html"), ".html", self.tab_bar)

    def java_template_core(self):
        self.file_manager.create_file(templates.return_content("java"), ".java", self.tab_bar)

    def c_template_core(self):
        self.file_manager.create_file(templates.return_content("c"), ".c", self.tab_bar)

    def comp_template_core(self):
        self.file_manager.create_file(templates.return_content("competitive"), ".cpp", self.tab_bar)

    def create_template_core(self):
        templates.create_template(self.editor, self.file_manager, self.theme)

    def use_template_core(self):
        templates.use_template(self.editor, self.file_manager, self.theme, self.tab_bar)

    def right_panel_core(self):
        self.view_manager.right_panel()

    def fullscreen_core(self):
        self.view_manager.fullscreen()

    def status_bar_core(self):
        self.view_manager.status_bar()

    def left_panel_core(self):
        self.view_manager.left_panel()

    def reset_zoom_core(self):
        self.view_manager.reset_zoom()

    def zoom_in_core(self):
        self.view_manager.zoom_in()

    def zoom_out_core(self):
        self.view_manager.zoom_out()

    def find_core(self):
        misc = misc_manager.MiscManager(self.editor, self.theme)
        misc.find_text()

    def replace_core(self):
        misc = misc_manager.MiscManager(self.editor, self.theme)
        misc.replace_text()

    def go_to_line_core(self):
        misc = misc_manager.MiscManager(self.editor, self.theme)
        misc.go_to_line()

    def clear_core(self):
        self.edit_manager.clear()
    def select_core(self):
        self.edit_manager.select_all()
    def undo_core(self):
        self.edit_manager.undo()
    def redo_core(self):
        self.edit_manager.redo()
    def copy_core(self):
        self.edit_manager.copy()
    def paste_core(self):
        self.edit_manager.paste()
    def cut_core(self):
        self.edit_manager.cut()
    def delete_core(self):
        self.edit_manager.delete()

    def new_file_core(self):
        self.file_manager.new_file(self.tab_bar, self.theme)

    def open_folder_core(self):
        self.file_manager.open_folder(self.tree_view, self)

    def close_folder_core(self):
        self.file_manager.close_folder(self.tree_view, self)

    def save_file_core(self):
        self.file_manager.save_file(self.editor)

    def save_as_file_core(self):
        self.file_manager.save_as_file(self.editor)

    def open_file_core(self):
        self.file_manager.open_file(self.editor, self.tab_bar)

    def exit_app(self):
        sys.exit(0)

    def open_profile_win(self):
        self.profile_window = profile.ProfileWindow(self.theme)
        self.profile_window.show()

    def log_web(self):
        web.open_links("https://hojdaadelin.github.io/code-nimble/src/blogs.html")

    def site_web(self):
        web.open_links("https://hojdaadelin.github.io/code-nimble/")

    def bugs_web(self):
        web.open_links("https://github.com/HojdaAdelin/CodeNimble/issues")

    def open_version_win(self):
        self.version_window = info_win.VersionWindow(self.theme)
        self.version_window.show_window()

    def get_theme(self):
        return self.theme

    def change_theme(self, theme):
        self.config['theme'] = theme
        with open('config.json', 'w') as file:
            json.dump(self.config, file,indent=4)
        with open(f'Themes/{self.config.get("theme")}.json', 'r') as file:
            self.theme = json.load(file)
        self.load_theme()

    def load_theme(self):
        font_family = self.config.get('font_family', 'Consolas')
        font_size = self.config.get('font_size', '18px')
        self.editor.apply_theme(self.theme)
        self.status_bar.apply_theme(self.theme)
        self.tree_view.apply_theme(self.theme)
        self.right_panel.apply_theme(self.theme)
        self.tab_bar.apply_stylesheet(self.theme)
        self.tool_bar.apply_theme(self.theme)
        self.splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background-color: {self.theme['background_color']};
            }}
            QSplitter::handle:horizontal {{
                background-color: {self.theme['background_color']};  
            }}
            QSplitter::handle:vertical {{
                background-color: {self.theme['background_color']}; 
            }}
        """)

        self.editor.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {self.theme['editor_background']};
                color: {self.theme['editor_foreground']};
                selection-background-color: {self.theme['selection_background_color']};
            }}
        """)
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.theme['background_color']};
                color: {self.theme['text_color']};
                font-family: {font_family};
                font-size: {font_size};
            }}
            QPushButton {{
                background-color: {self.theme['button_color']};
                color: {self.theme['text_color']};
            }}
            QPushButton:hover {{
                background-color: {self.theme['button_hover_color']};
            }}
            QMenuBar {{
                background-color: {self.theme['background_color']};
                color: {self.theme['text_color']};
                font-family: {font_family};
                font-size: 16px;
            }}
            QMenuBar::item {{
                font-family: {font_family};
                font-size: {font_size};
            }}
            QMenuBar::item:selected {{
                background-color: {self.theme['item_hover_background_color']};
                color: {self.theme['item_hover_text_color']};
            }}
            QMenu {{
                background-color: {self.theme['background_color']};
                color: {self.theme['text_color']};
                border: 1px solid {self.theme['border_color']};
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
                background-color: {self.theme['item_hover_background_color']};
                color: {self.theme['item_hover_text_color']};
                padding: 5px 10px; 
            }}
            QMenu::separator {{
                height: 1px;
                background: {self.theme['separator_color']};
            }}
        """)