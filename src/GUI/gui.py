import threading
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
from GUI import paint_mode
from Server import panel
from MainMenu import profile
from MainMenu import settings
from MainMenu import session

class MainWindow(ct.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Main menu
        menu = CTkMenuBar(master=self, border_width=0)
        home = menu.add_cascade("Home", hover_color="#4d4d4d", font=("", 20))
        file_m = menu.add_cascade("File", hover_color="#4d4d4d", font=("", 20))
        edit = menu.add_cascade("Edit", hover_color="#4d4d4d", font=("", 20))
        view = menu.add_cascade("View", hover_color="#4d4d4d", font=("", 20))
        template = menu.add_cascade("Templates", hover_color="#4d4d4d", font=("", 20))
        textures = menu.add_cascade("Textures", hover_color="#4d4d4d", font=("", 20))
        utility = menu.add_cascade("Utility", hover_color="#4d4d4d", font=("", 20))

        home_drop = CustomDropdownMenu(widget=home, font=("", 20), corner_radius=4, separator_color="#b0b0b0")
        home_drop.add_option(option="Guide", command=lambda:misc.guide())
        home_drop.add_option(option="Version", command=lambda:misc.version_info())
        home_drop.add_option(option="Change log", command=lambda:misc.changelog_inf())
        home_drop.add_option(option="Source",command=lambda:misc.open_links("https://github.com/HojdaAdelin/CodeNimble"))
        home_drop.add_option(option="Report bugs",command=lambda:misc.open_links("https://github.com/HojdaAdelin/CodeNimble/issues"))
        home_drop.add_separator()
        home_drop.add_option(option="Profile", command=lambda:open_profile_window(self))
        home_drop.add_option(option="Settings", command=lambda:open_settings_window(self))
        home_drop.add_separator()
        home_drop.add_option(option="Exit", command=lambda: misc.exit_application(self))
    
        file_drop = CustomDropdownMenu(widget=file_m, font=("", 20), corner_radius=4, separator_color="#b0b0b0")
        file_drop.add_option(option="New File                     Ctrl+N", command=lambda: file_menu.custom_file(statusbar_instance, treeview_frame))
        file_drop.add_option(option="Open                          Ctrl+O",command=lambda:file_menu.open_file(scroll.text, scroll, statusbar_instance))
        file_drop.add_separator()
        file_drop.add_option(option="Open Input",command=lambda:file_menu.open_input(treeview_frame))
        file_drop.add_option(option="Save Input",command=lambda:file_menu.save_input(treeview_frame))
        file_drop.add_option(option="Open Output",command=lambda:file_menu.open_output(treeview_frame))
        file_drop.add_separator()
        file_drop.add_option(option="Open Folder               Ctrl+K",command=lambda:file_menu.open_folder(treeview_frame, statusbar_instance, scroll))
        file_drop.add_option(option="Close Folder", command=lambda:file_menu.close_folder(treeview_frame, scroll))
        file_drop.add_separator()
        file_drop.add_option(option="Save                           Ctrl+S",command=lambda:file_menu.save_file(scroll.text, statusbar_instance))
        file_drop.add_option(option="Save as             Ctrl+Shift+S",command=lambda:file_menu.save_as_file(scroll.text, statusbar_instance))
        file_drop.add_separator()
        file_drop.add_option(option="Save as default file",command=lambda:file_menu.save_as_default(statusbar_instance))
        file_drop.add_option(option="Remove default file",command=lambda:file_menu.remove_default_file(statusbar_instance))
        file_drop.add_option(option="Save as default folder", command=lambda:file_menu.save_as_default_folder(statusbar_instance))
        file_drop.add_option(option="Remove default folder", command=lambda:file_menu.remove_default_folder(statusbar_instance))
        file_drop.add_separator()
        file_drop.add_option(option="Save session", command=lambda:session.save_session(scroll.tab_bar.tabs))

        edit_drop = CustomDropdownMenu(widget=edit, font=("", 20), corner_radius=4, separator_color="#b0b0b0")
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
        edit_drop.add_option(option="Find                             Ctrl+F", command=lambda:edit_menu.find_text(scroll.text, scroll))
        edit_drop.add_option(option="Replace                      Ctrl+H", command=lambda:edit_menu.replace_text(scroll.text, scroll))

        view_drop = CustomDropdownMenu(widget=view, font=("", 20), corner_radius=4, separator_color="#b0b0b0")
        view_drop.add_option(option="Zoom in                        Ctrl+ =", command=lambda:view_menu.zoom_in(scroll))
        view_drop.add_option(option="Zoom out                      Ctrl+ -", command=lambda:view_menu.zoom_out(scroll))
        view_drop.add_option(option="Reset zoom", command=lambda:view_menu.reset_zoom(scroll))
        view_drop.add_option(option="Fullscreen                         F11", command=lambda:view_menu.toggle_fullscreen(self))
        view_drop.add_separator()
        view_drop.add_option(option="Status Bar",command=lambda:view_menu.hide_unhide_statusbar(statusbar_instance))
        view_drop.add_option(option="Notifications",command=lambda:view_menu.notifications(statusbar_instance))
        view_drop.add_option(option="Left Panel                     Ctrl+B", command=lambda:view_menu.hide_unhide_treeview(treeview_frame, scroll))
        view_drop.add_option(option="Input & Output", command=lambda:view_menu.hide_unhide_input_output(treeview_frame))
        view_drop.add_separator()
        view_drop.add_option(option="Refresh editor     Ctrl+Shift+R", command=lambda:scroll.redraw())

        template_drop = CustomDropdownMenu(widget=template, font=("", 20), corner_radius=4, separator_color="#b0b0b0")
        template_drop.add_option(option="C++", command=lambda:template_menu.create_template(scroll.text, scroll, statusbar_instance, "cpp"))
        template_drop.add_option(option="C", command=lambda:template_menu.create_template(scroll.text, scroll, statusbar_instance, "c"))
        template_drop.add_option(option="Java", command=lambda:template_menu.create_template(scroll.text, scroll, statusbar_instance, "java"))
        template_drop.add_option(option="Html", command=lambda:template_menu.create_template(scroll.text, scroll, statusbar_instance, "html"))
        template_drop.add_option(option="C++ Competitive", command=lambda:template_menu.create_template(scroll.text, scroll, statusbar_instance, "com"))
        template_drop.add_separator()
        template_drop.add_option(option="Create Template", command=lambda:template_menu.custom_template())
        template_drop.add_option(option="Use Template           Ctrl+Shift+T", command=lambda:template_menu.use_template(scroll.text, scroll, statusbar_instance))

        textures_drop = CustomDropdownMenu(widget=textures, font=("", 20), corner_radius=4, separator_color="#b0b0b0")
        textures_drop.add_option(option="Light theme", command=lambda:themes.use_theme("light",menu, home, file_m, edit, view, template, textures, utility,
                                                                                         home_drop, file_drop, edit_drop, view_drop, template_drop, textures_drop,
                                                                                         utility_drop,
                                                                                         statusbar_instance, scroll, self, treeview_frame, treeview_frame.menu, treeview_frame.folder_menu,
                                                                                         scroll.tab_bar))
        textures_drop.add_option(option="Dark theme", command=lambda:themes.use_theme("dark",menu, home, file_m, edit, view, template, textures, utility,
                                                                                         home_drop, file_drop, edit_drop, view_drop, template_drop, textures_drop,
                                                                                         utility_drop,
                                                                                         statusbar_instance, scroll, self, treeview_frame, treeview_frame.menu, treeview_frame.folder_menu,
                                                                                         scroll.tab_bar))
        textures_drop.add_option(option="Ocean theme", command=lambda:themes.use_theme("ocean",menu, home, file_m, edit, view, template, textures, utility,
                                                                                         home_drop, file_drop, edit_drop, view_drop, template_drop, textures_drop,
                                                                                         utility_drop,
                                                                                         statusbar_instance, scroll, self, treeview_frame, treeview_frame.menu, treeview_frame.folder_menu,
                                                                                         scroll.tab_bar))
        
        utility_drop = CustomDropdownMenu(widget=utility, font=("", 20), corner_radius=4, separator_color="#b0b0b0")
        utility_drop.add_option(option="Run                                F5", command=lambda:run.run_cpp_file(treeview_frame, scroll.text))
        utility_drop.add_option(option="Paint Mode              Ctrl+P", command=lambda:open_paint_mode(self))
        utility_drop.add_separator()
        utility_drop.add_option(option="Start Server (Beta)", command= lambda:scroll.start_server())
        utility_drop.add_option(option="Join Local Server (Beta)", command=lambda:scroll.start_client())
        utility_drop.add_option(option="Disconnect (Beta)", command=lambda:scroll.disconnect_client())
        utility_drop.add_option(option="Server Panel (Beta)", command=lambda:open_server_panel(self))
        
        statusbar_instance = statusbar.StatusBar(self, text="")
        self.statusbar_instance = statusbar_instance
        scroll = textbox.ScrollText(self, statusbar_instance)
        self.scroll = scroll
        treeview_frame = treeview.TreeviewFrame(self, scroll, statusbar_instance, scroll)

        
        self.auto_save_option()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        treeview_frame.grid_forget()
        menu.grid(row=0, column=0,columnspan=2, sticky="ew")
        scroll.grid(row=1, column=0,columnspan=2,sticky="nswe")
        if (int(check.get_config_value("status")) == 1):
            statusbar_instance.grid(row=2, column=0,columnspan=2, sticky="ew")

        scroll.text.focus()
        self.after(200, scroll.redraw())
        statusbar_instance.run_img.bind("<Button-1>", lambda event: run.run_cpp_file(treeview_frame, scroll.text))
        scroll.text.bind("<Control-n>", lambda event: file_menu.custom_file(statusbar_instance, treeview_frame))
        scroll.text.bind("<Control-o>", lambda event: file_menu.open_file(scroll.text, scroll, statusbar_instance))
        scroll.text.bind("<Control-s>", lambda event: file_menu.save_file(scroll.text, statusbar_instance))
        scroll.text.bind("<Control-Shift-s>", lambda event: file_menu.save_as_file(scroll.text, statusbar_instance))
        scroll.text.bind("<Control-y>", lambda event: edit_menu.redo_text(scroll.text, scroll))
        scroll.text.bind("<Control-x>", lambda event: edit_menu.cut_text(scroll.text, scroll))
        scroll.text.bind("<Control-d>", lambda event: edit_menu.delete_text(scroll.text, scroll))
        scroll.text.bind("<Control-Alt-c>", lambda event: edit_menu.clear_text(scroll.text, scroll, statusbar_instance))
        scroll.text.bind("<Control-=>", lambda event: view_menu.zoom_in(scroll))
        scroll.text.bind("<Control-minus>", lambda event: view_menu.zoom_out(scroll))
        scroll.text.bind("<Control-f>", lambda event: edit_menu.find_text(scroll.text, scroll))
        scroll.text.bind("<Control-h>", lambda event:edit_menu.replace_text(scroll.text, scroll))
        scroll.text.bind("<F11>", lambda event: view_menu.toggle_fullscreen(self))
        scroll.text.bind("<Control-k>",lambda event:file_menu.open_folder(treeview_frame, statusbar_instance, scroll))
        scroll.text.bind("<Control-b>", lambda event: view_menu.hide_unhide_treeview(treeview_frame, scroll))
        scroll.text.bind("<Control-Shift-T>", lambda event: template_menu.use_template(scroll.text, scroll, statusbar_instance))
        scroll.text.bind("<F5>", lambda event:run.run_cpp_file(treeview_frame, scroll.text))
        scroll.text.bind("<Control-p>", lambda event:open_paint_mode(self))
        treeview_frame.input.bind("<Control-s>", lambda event:file_menu.save_input(treeview_frame))
        scroll.text.bind("<Control-Shift-R>", lambda event:scroll.redraw())
        scroll.text.bind("<Control-MouseWheel>", lambda event:self.mouse_wheel(event=event))

        # General configuration
        ct.set_appearance_mode("dark")
        self.title("CodeNimble")
        self.iconbitmap("images/logo.ico")
        self.geometry("1200x700")
        
        if not check.get_config_value("default_file") == "0":
            file_menu.open_default_file(scroll.text, scroll, statusbar_instance)

        if not check.get_config_value("default_folder") == "0":
            file_menu.open_folder(treeview_frame, statusbar_instance, scroll, check.get_config_value("default_folder"))

        # Theme
        current_theme = check.get_config_value("theme")
        themes.use_theme(current_theme,menu, home, file_m, edit, view, template, textures,
                                utility,
                                home_drop, file_drop, edit_drop, view_drop, template_drop, textures_drop,
                                utility_drop,
                                statusbar_instance, scroll, self, treeview_frame, treeview_frame.menu, treeview_frame.folder_menu,
                                scroll.tab_bar)
        
        def open_paint_mode(self):
            paint_window = paint_mode.PaintApp()
            paint_window.mainloop()
        
        def open_profile_window(self):
            profil = profile.ProfileApp()
            profil.mainloop()

        def open_server_panel(self):
            panel_window = panel.ServerPanel(self.scroll.server)
            panel_window.mainloop()

        def open_settings_window(self):
            settings_window = settings.SettingsApp(status=statusbar_instance)
            settings_window.mainloop()

    def auto_save_option(self):
        if file_menu.opened_file_status() and int(check.get_config_value("auto_save")) == 1:
            file_menu.save_file(self.scroll.text, self.statusbar_instance)
        
        self.after(5000, self.auto_save_option)

    def mouse_wheel(self,event):
        
        if event.num == 5 or event.delta == -120:
            view_menu.zoom_out(self.scroll)
        if event.num == 4 or event.delta == 120:
            view_menu.zoom_in(self.scroll)