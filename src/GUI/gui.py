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
        home = menu.add_cascade("Home")
        file_m = menu.add_cascade("File")
        edit = menu.add_cascade("Edit")
        view = menu.add_cascade("View")
        home_drop = CustomDropdownMenu(widget=home, padx=-5, pady=-25, bg_color="#333333", font=("", 14), corner_radius=4, separator_color="gray",hover_color="#4d4d4d")
        home_drop.add_option(option="Version", command=lambda:misc.version_info())
        home_drop.add_option(option="Change log", command=lambda:misc.changelog_inf())
        home_drop.add_option(option="Source",command=lambda:misc.open_links("https://github.com/HojdaAdelin/CodeNimble"))
        home_drop.add_separator()
        home_drop.add_option(option="Exit", command=lambda: misc.exit_application(self))

        # Config values
    
        file_drop = CustomDropdownMenu(widget=file_m, padx=-55, pady=-25, bg_color="#333333", font=("", 14), corner_radius=4, separator_color="gray",hover_color="#4d4d4d")
        #file_drop.add_option(option="New window", command=lambda:file_menu.new_window())
        file_drop.add_option(option="New", command=lambda: file_menu.new_file(scroll.text, scroll, statusbar_instance))
        file_drop.add_option(option="Open",command=lambda:file_menu.open_file(scroll.text, scroll, statusbar_instance))
        file_drop.add_option(option="Save",command=lambda:file_menu.save_file(scroll.text, statusbar_instance))
        file_drop.add_option(option="Save as",command=lambda:file_menu.save_as_file(scroll.text))
 
        edit_drop = CustomDropdownMenu(widget=edit, padx=-95, pady=-25, bg_color="#333333", font=("", 14), corner_radius=4, separator_color="gray",hover_color="#4d4d4d")
        edit_drop.add_option(option="Undo", command=lambda:edit_menu.undo_text(scroll.text, scroll))
        edit_drop.add_option(option="Redo", command=lambda:edit_menu.redo_text(scroll.text, scroll))
        edit_drop.add_separator()
        edit_drop.add_option(option="Cut", command=lambda:edit_menu.cut_text(scroll.text, scroll))
        edit_drop.add_option(option="Copy", command=lambda:edit_menu.copy_text(scroll.text, scroll))
        edit_drop.add_option(option="Paste", command=lambda:edit_menu.paste_text(scroll.text, scroll))
        edit_drop.add_option(option="Delete",command=lambda:edit_menu.delete_text(scroll.text, scroll))
        edit_drop.add_option(option="Select all", command=lambda:edit_menu.select_all(scroll.text))
        edit_drop.add_separator()
        edit_drop.add_option(option="Find")
        edit_drop.add_option(option="Replace")

        view_drop = CustomDropdownMenu(widget=view, padx=-135, pady=-25, bg_color="#333333", font=("", 14), corner_radius=4, separator_color="gray",hover_color="#4d4d4d")
        view_drop.add_option(option="Zoom in", command=lambda:view_menu.zoom_in(scroll))
        view_drop.add_option(option="Zoom out", command=lambda:view_menu.zoom_out(scroll))
        
        # TextBox
        scroll.pack(fill="both", expand=True)
        
        scroll.text.focus()
        self.after(200, scroll.redraw())
        self.configure(border_color = "red")
        # General configuration
        #ct.set_default_color_theme("dark-blue")
        self.title("CodeNimble")
        self.geometry("1200x700")
        # Title bar color handle
        HWND = windll.user32.GetParent(self.winfo_id())
        tb_color = 0x333333
        windll.dwmapi.DwmSetWindowAttribute(
            HWND,
            35,
            byref(c_int(tb_color)),
            sizeof(c_int))
