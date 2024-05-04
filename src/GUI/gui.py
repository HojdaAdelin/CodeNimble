from typing import Any, Tuple
import customtkinter as ct
from CTkMenuBar import *
from ctypes import byref, sizeof, c_int, windll

import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from MainMenu import misc
from MainMenu import file_menu
from MainMenu import edit_menu
from MainMenu import view_menu
from MainMenu import template_menu
from MainMenu import themes
from GUI import textbox
from GUI import statusbar
from Config import check

class MainWindow(ct.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Main menu
        statusbar_instance = statusbar.StatusBar(self, text="")

        scroll = textbox.ScrollText(self)
        menu = CTkMenuBar(self, bg_color="#333333")
        home = menu.add_cascade("Home", hover_color="#4d4d4d")
        file_m = menu.add_cascade("File", hover_color="#4d4d4d")
        edit = menu.add_cascade("Edit", hover_color="#4d4d4d")
        view = menu.add_cascade("View", hover_color="#4d4d4d")
        template = menu.add_cascade("Templates", hover_color="#4d4d4d")
        textures = menu.add_cascade("Textures", hover_color="#4d4d4d")

        home_drop = CustomDropdownMenu(widget=home, bg_color="#333333", font=("", 14), corner_radius=4, separator_color="#b0b0b0",hover_color="#4d4d4d")
        home_drop.add_option(option="Version", command=lambda:misc.version_info())
        home_drop.add_option(option="Change log", command=lambda:misc.changelog_inf())
        home_drop.add_option(option="Source",command=lambda:misc.open_links("https://github.com/HojdaAdelin/CodeNimble"))
        home_drop.add_separator()
        home_drop.add_option(option="Exit", command=lambda: misc.exit_application(self))
        
        # Config values
    
        file_drop = CustomDropdownMenu(widget=file_m, bg_color="#333333", font=("", 14), corner_radius=4, separator_color="#b0b0b0",hover_color="#4d4d4d")
        #file_drop.add_option(option="New window", command=lambda:file_menu.new_window())
        file_drop.add_option(option="New File", command=lambda: file_menu.custom_file(statusbar_instance))
        file_drop.add_option(option="New", command=lambda: file_menu.new_file(scroll.text, scroll, statusbar_instance))
        file_drop.add_option(option="Open",command=lambda:file_menu.open_file(scroll.text, scroll, statusbar_instance))
        file_drop.add_separator()
        file_drop.add_option(option="Save",command=lambda:file_menu.save_file(scroll.text, statusbar_instance))
        file_drop.add_option(option="Save as",command=lambda:file_menu.save_as_file(scroll.text))
        file_drop.add_option(option="Save as default file",command=lambda:file_menu.save_as_default(statusbar_instance))
 
        edit_drop = CustomDropdownMenu(widget=edit, bg_color="#333333", font=("", 14), corner_radius=4, separator_color="#b0b0b0",hover_color="#4d4d4d")
        edit_drop.add_option(option="Undo", command=lambda:edit_menu.undo_text(scroll.text, scroll))
        edit_drop.add_option(option="Redo", command=lambda:edit_menu.redo_text(scroll.text, scroll))
        edit_drop.add_separator()
        edit_drop.add_option(option="Cut", command=lambda:edit_menu.cut_text(scroll.text, scroll))
        edit_drop.add_option(option="Copy", command=lambda:edit_menu.copy_text(scroll.text, scroll))
        edit_drop.add_option(option="Paste", command=lambda:edit_menu.paste_text(scroll.text, scroll))
        edit_drop.add_option(option="Delete",command=lambda:edit_menu.delete_text(scroll.text, scroll))
        edit_drop.add_option(option="Clear", command=lambda:edit_menu.clear_text(scroll.text, scroll, statusbar_instance))
        edit_drop.add_option(option="Select all", command=lambda:edit_menu.select_all(scroll.text))
        edit_drop.add_separator()
        edit_drop.add_option(option="Find", command=lambda:edit_menu.find_text(scroll.text))
        edit_drop.add_option(option="Replace", command=lambda:edit_menu.replace_text(scroll.text))

        view_drop = CustomDropdownMenu(widget=view, bg_color="#333333", font=("", 14), corner_radius=4, separator_color="#b0b0b0",hover_color="#4d4d4d")
        view_drop.add_option(option="Zoom in", command=lambda:view_menu.zoom_in(scroll))
        view_drop.add_option(option="Zoom out", command=lambda:view_menu.zoom_out(scroll))
        view_drop.add_option(option="Reset zoom", command=lambda:view_menu.reset_zoom(scroll))

        template_drop = CustomDropdownMenu(widget=template, bg_color="#333333", font=("", 14), corner_radius=4, separator_color="#b0b0b0",hover_color="#4d4d4d")
        template_drop.add_option(option="C++", command=lambda:template_menu.create_template(scroll.text, scroll, statusbar_instance, "cpp"))
        template_drop.add_option(option="C", command=lambda:template_menu.create_template(scroll.text, scroll, statusbar_instance, "c"))
        template_drop.add_option(option="Java", command=lambda:template_menu.create_template(scroll.text, scroll, statusbar_instance, "java"))
        template_drop.add_option(option="Html", command=lambda:template_menu.create_template(scroll.text, scroll, statusbar_instance, "html"))
        template_drop.add_option(option="C++ Competitive", command=lambda:template_menu.create_template(scroll.text, scroll, statusbar_instance, "com"))

        textures_drop = CustomDropdownMenu(widget=textures, bg_color="#333333", font=("", 14), corner_radius=4, separator_color="#b0b0b0",hover_color="#4d4d4d")
        textures_drop.add_option(option="Light theme", command=lambda:themes.light_theme(menu, home, file_m, edit, view, template, textures,
                                                                                         home_drop, file_drop, edit_drop, view_drop, template_drop, textures_drop,
                                                                                         statusbar_instance, scroll, self))
        textures_drop.add_option(option="Dark theme", command=lambda:themes.dark_theme(menu, home, file_m, edit, view, template, textures,
                                                                                         home_drop, file_drop, edit_drop, view_drop, template_drop, textures_drop,
                                                                                         statusbar_instance, scroll, self))
        
        # TextBox
        scroll.pack(fill="both", expand=True)
        
        scroll.text.focus()
        self.after(200, scroll.redraw())
        # General configuration
        ct.set_appearance_mode("dark")
        self.title("CodeNimble")
        self.iconbitmap("images/logo.ico")
        self.geometry("1200x700")
        # Default file
        
        if not hasattr(MainWindow, 'default_file_opened'):
            file_menu.open_default_file(scroll.text, scroll, statusbar_instance)
            scroll.redraw()
            MainWindow.default_file_opened = True
        # Theme
        current_theme = check.get_config_value("theme")
        if (current_theme == 0):
            themes.dark_theme(menu, home, file_m, edit, view, template, textures,
                                home_drop, file_drop, edit_drop, view_drop, template_drop, textures_drop,
                                statusbar_instance, scroll, self)
        elif(current_theme == 1):
            themes.light_theme(menu, home, file_m, edit, view, template, textures,
                                home_drop, file_drop, edit_drop, view_drop, template_drop, textures_drop,
                                statusbar_instance, scroll, self)
        else:
            themes.dark_theme(menu, home, file_m, edit, view, template, textures,
                                home_drop, file_drop, edit_drop, view_drop, template_drop, textures_drop,
                                statusbar_instance, scroll, self)
        # Title bar color handle
        tb_color = 0x333333
        if (check.get_config_value("theme") == 0):
            tb_color = 0x333333
        elif (check.get_config_value("theme") == 1):
            tb_color = 0xFFFFFF
        else:
            tb_color = 0x333333
        
        HWND = windll.user32.GetParent(self.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(
            HWND,
            35,
            byref(c_int(tb_color)),
            sizeof(c_int))

