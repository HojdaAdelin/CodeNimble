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

class MainWindow(ct.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Main menu
        menu = CTkMenuBar(self, bg_color="#333333")
        home = menu.add_cascade("Home")
        file = menu.add_cascade("File")
        edit = menu.add_cascade("Edit")
        view = menu.add_cascade("View")

        home_drop = CustomDropdownMenu(widget=home, padx=-5, pady=-25, bg_color="#333333", font=("", 14), corner_radius=4)
        home_drop.add_option(option="Version")
        home_drop.add_option(option="Change log")
        home_drop.add_option(option="Source")
        home_drop.add_option(option="Exit", command=lambda: misc.exit_application(self))

        file_drop = CustomDropdownMenu(widget=file, padx=-55, pady=-25, bg_color="#333333", font=("", 14), corner_radius=4)
        file_drop.add_option(option="New window")
        file_drop.add_option(option="New")
        file_drop.add_option(option="Open")
        file_drop.add_option(option="Save")
        file_drop.add_option(option="Save as")

        edit_drop = CustomDropdownMenu(widget=edit, padx=-95, pady=-25, bg_color="#333333", font=("", 14), corner_radius=4)
        edit_drop.add_option(option="Undo")
        edit_drop.add_option(option="Redo")
        edit_drop.add_option(option="Cut")
        edit_drop.add_option(option="Copy")
        edit_drop.add_option(option="Paste")
        edit_drop.add_option(option="Delete")
        edit_drop.add_option(option="Select all")
        edit_drop.add_option(option="Find")
        edit_drop.add_option(option="Replace")

        view_drop = CustomDropdownMenu(widget=view, padx=-135, pady=-25, bg_color="#333333", font=("", 14), corner_radius=4)
        view_drop.add_option(option="Zoom in")
        view_drop.add_option(option="Zoom out")

        # General configuration
        ct.set_default_color_theme("dark-blue")
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
