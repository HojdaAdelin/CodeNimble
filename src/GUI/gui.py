from typing import Any, Tuple
import customtkinter as ct
from CTkMenuBar import *
from ctypes import byref, sizeof, c_int, windll
import tkinter as tk

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
from API import get_version
from MainMenu import run
from GUI import treeview

class MainWindow(ct.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Main menu
        statusbar_instance = statusbar.StatusBar(self, text="")
        scroll = textbox.ScrollText(self)
        treeview_frame = treeview.TreeviewFrame(self, scroll.text, statusbar_instance, scroll)
        menu = CTkMenuBar(self, bg_color="#333333")
        home = menu.add_cascade("Home", hover_color="#4d4d4d", font=("", 20))
        file_m = menu.add_cascade("File", hover_color="#4d4d4d", font=("", 20))
        edit = menu.add_cascade("Edit", hover_color="#4d4d4d", font=("", 20))
        view = menu.add_cascade("View", hover_color="#4d4d4d", font=("", 20))
        template = menu.add_cascade("Templates", hover_color="#4d4d4d", font=("", 20))
        textures = menu.add_cascade("Textures", hover_color="#4d4d4d", font=("", 20))
        utility = menu.add_cascade("Utility", hover_color="#4d4d4d", font=("", 20))

        home_drop = CustomDropdownMenu(widget=home, bg_color="#333333", font=("", 20), corner_radius=4, separator_color="#b0b0b0",hover_color="#4d4d4d")
        home_drop.add_option(option="Version", command=lambda:misc.version_info())
        home_drop.add_option(option="Change log", command=lambda:misc.changelog_inf())
        home_drop.add_option(option="Source",command=lambda:misc.open_links("https://github.com/HojdaAdelin/CodeNimble"))
        home_drop.add_option(option="Report bugs",command=lambda:misc.open_links("https://github.com/HojdaAdelin/CodeNimble/issues"))
        home_drop.add_separator()
        home_drop.add_option(option="Exit", command=lambda: misc.exit_application(self))
        
        # Config values
    
        file_drop = CustomDropdownMenu(widget=file_m, bg_color="#333333", font=("", 20), corner_radius=4, separator_color="#b0b0b0",hover_color="#4d4d4d")
        #file_drop.add_option(option="New window", command=lambda:file_menu.new_window())
        file_drop.add_option(option="New File", command=lambda: file_menu.custom_file(statusbar_instance, treeview_frame))
        file_drop.add_option(option="New                            Ctrl+N", command=lambda: file_menu.new_file(scroll.text, scroll, statusbar_instance))
        file_drop.add_option(option="Open                          Ctrl+O",command=lambda:file_menu.open_file(scroll.text, scroll, statusbar_instance))
        file_drop.add_option(option="Open Folder               Ctrl+K",command=lambda:file_menu.open_folder(treeview_frame, statusbar_instance))
        file_drop.add_option(option="Close Folder", command=lambda:file_menu.close_folder(treeview_frame))
        file_drop.add_separator()
        file_drop.add_option(option="Save                           Ctrl+S",command=lambda:file_menu.save_file(scroll.text, statusbar_instance))
        file_drop.add_option(option="Save as             Ctrl+Shift+S",command=lambda:file_menu.save_as_file(scroll.text, statusbar_instance))
        file_drop.add_option(option="Save as default file",command=lambda:file_menu.save_as_default(statusbar_instance))
        file_drop.add_option(option="Remove default file",command=lambda:file_menu.delete_file("default_file.txt",statusbar_instance))
 
        edit_drop = CustomDropdownMenu(widget=edit, bg_color="#333333", font=("", 20), corner_radius=4, separator_color="#b0b0b0",hover_color="#4d4d4d")
        edit_drop.add_option(option="Undo                           Ctrl+Z", command=lambda:edit_menu.undo_text(scroll.text, scroll))
        edit_drop.add_option(option="Redo                           Ctrl+Y", command=lambda:edit_menu.redo_text(scroll.text, scroll))
        edit_drop.add_separator()
        edit_drop.add_option(option="Cut                              Ctrl+X", command=lambda:edit_menu.cut_text(scroll.text, scroll))
        edit_drop.add_option(option="Copy                           Ctrl+C", command=lambda:edit_menu.copy_text(scroll.text, scroll))
        edit_drop.add_option(option="Paste                          Ctrl+V", command=lambda:edit_menu.paste_text(scroll.text, scroll))
        edit_drop.add_option(option="Delete                         Ctrl+D",command=lambda:edit_menu.delete_text(scroll.text, scroll))
        edit_drop.add_option(option="Clear                    Ctrl+Alt+C", command=lambda:edit_menu.clear_text(scroll.text, scroll, statusbar_instance))
        edit_drop.add_option(option="Select all                     Ctrl+A", command=lambda:edit_menu.select_all(scroll.text))
        edit_drop.add_separator()
        edit_drop.add_option(option="Find                             Ctrl+F", command=lambda:edit_menu.find_text(scroll.text))
        edit_drop.add_option(option="Replace                      Ctrl+H", command=lambda:edit_menu.replace_text(scroll.text))

        view_drop = CustomDropdownMenu(widget=view, bg_color="#333333", font=("", 20), corner_radius=4, separator_color="#b0b0b0",hover_color="#4d4d4d")
        view_drop.add_option(option="Zoom in                        Ctrl+ =", command=lambda:view_menu.zoom_in(scroll))
        view_drop.add_option(option="Zoom out                      Ctrl+ -", command=lambda:view_menu.zoom_out(scroll))
        view_drop.add_option(option="Reset zoom", command=lambda:view_menu.reset_zoom(scroll))
        view_drop.add_separator()
        view_drop.add_option(option="Fullscreen                         F11", command=lambda:view_menu.toggle_fullscreen(self))
        view_drop.add_option(option="Treeview                       Ctrl+B", command=lambda:view_menu.hide_unhide_treeview(treeview_frame))
        view_drop.add_option(option="Output & Input", command=lambda:treeview_frame.toggle_textboxes())

        template_drop = CustomDropdownMenu(widget=template, bg_color="#333333", font=("", 20), corner_radius=4, separator_color="#b0b0b0",hover_color="#4d4d4d")
        template_drop.add_option(option="C++", command=lambda:template_menu.create_template(scroll.text, scroll, statusbar_instance, "cpp"))
        template_drop.add_option(option="C", command=lambda:template_menu.create_template(scroll.text, scroll, statusbar_instance, "c"))
        template_drop.add_option(option="Java", command=lambda:template_menu.create_template(scroll.text, scroll, statusbar_instance, "java"))
        template_drop.add_option(option="Html", command=lambda:template_menu.create_template(scroll.text, scroll, statusbar_instance, "html"))
        template_drop.add_option(option="C++ Competitive", command=lambda:template_menu.create_template(scroll.text, scroll, statusbar_instance, "com"))

        textures_drop = CustomDropdownMenu(widget=textures, bg_color="#333333", font=("", 20), corner_radius=4, separator_color="#b0b0b0",hover_color="#4d4d4d")
        textures_drop.add_option(option="Light theme", command=lambda:themes.light_theme(menu, home, file_m, edit, view, template, textures, utility,
                                                                                         home_drop, file_drop, edit_drop, view_drop, template_drop, textures_drop,
                                                                                         utility_drop,
                                                                                         statusbar_instance, scroll, self, treeview_frame))
        textures_drop.add_option(option="Dark theme", command=lambda:themes.dark_theme(menu, home, file_m, edit, view, template, textures, utility,
                                                                                         home_drop, file_drop, edit_drop, view_drop, template_drop, textures_drop,
                                                                                         utility_drop,
                                                                                         statusbar_instance, scroll, self, treeview_frame))
        
        utility_drop = CustomDropdownMenu(widget=utility, bg_color="#333333", font=("", 20), corner_radius=4, separator_color="#b0b0b0",hover_color="#4d4d4d")
        utility_drop.add_option(option="Run                         F5", command=lambda:run.run_cpp_file())
        # Treeview
        # TextBox
        treeview_frame.pack_forget()
        scroll.pack(fill="both", expand=True, side="right")
        scroll.text.focus()
        self.after(200, scroll.redraw())
        scroll.text.bind("<Control-n>", lambda event: file_menu.new_file(scroll.text, scroll, statusbar_instance))
        scroll.text.bind("<Control-o>", lambda event: file_menu.open_file(scroll.text, scroll, statusbar_instance))
        scroll.text.bind("<Control-s>", lambda event: file_menu.save_file(scroll.text, statusbar_instance))
        scroll.text.bind("<Control-Shift-s>", lambda event: file_menu.save_as_file(scroll.text, statusbar_instance))
        #scroll.text.bind("<Control-z>", lambda event: edit_menu.undo_text(scroll.text, scroll))
        scroll.text.bind("<Control-y>", lambda event: edit_menu.redo_text(scroll.text, scroll))
        scroll.text.bind("<Control-x>", lambda event: edit_menu.cut_text(scroll.text, scroll))
        scroll.text.bind("<Control-d>", lambda event: edit_menu.delete_text(scroll.text, scroll))
        scroll.text.bind("<Control-Alt-c>", lambda event: edit_menu.clear_text(scroll.text, scroll, statusbar_instance))
        scroll.text.bind("<Control-=>", lambda event: view_menu.zoom_in(scroll))
        scroll.text.bind("<Control-minus>", lambda event: view_menu.zoom_out(scroll))
        scroll.text.bind("<Control-f>", lambda event: edit_menu.find_text(scroll.text))
        scroll.text.bind("<Control-h>", lambda event:edit_menu.replace_text(scroll.text))
        scroll.text.bind("<F11>", lambda event: view_menu.toggle_fullscreen(self))
        scroll.text.bind("<Control-k>",lambda event:file_menu.open_folder(treeview_frame, statusbar_instance))
        scroll.text.bind("<Control-b>", lambda event: view_menu.hide_unhide_treeview(treeview_frame))
        scroll.text.bind("<F5>", lambda event:run.run_cpp_file())

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
                                utility,
                                home_drop, file_drop, edit_drop, view_drop, template_drop, textures_drop,
                                utility_drop,
                                statusbar_instance, scroll, self, treeview_frame)
            
        elif(current_theme == 1):
            themes.light_theme(menu, home, file_m, edit, view, template, textures,
                                utility,
                                home_drop, file_drop, edit_drop, view_drop, template_drop, textures_drop,
                                utility_drop,
                                statusbar_instance, scroll, self, treeview_frame)
            
        else:
            themes.dark_theme(menu, home, file_m, edit, view, template, textures,
                                utility,
                                home_drop, file_drop, edit_drop, view_drop, template_drop, textures_drop,
                                utility_drop,
                                statusbar_instance, scroll, self, treeview_frame)
            
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