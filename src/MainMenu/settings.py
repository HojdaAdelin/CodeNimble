import customtkinter as ct
import tkinter as tk
from tkinter import *
from ctypes import byref, sizeof, c_int, windll

import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Config import check
from MainMenu import view_menu
from MainMenu import themes

class SettingsApp(ct.CTk):
    def __init__(self, status):
        super().__init__()

        self.status = status

        fg_cl, text_bg, text, hover_color = themes.return_default_win_color(check.get_config_value("theme"))
        self.window(fg_cl)
        self.gui(fg_cl, text_bg, text)
        self.title_color()

    def title_color(self):
        themes.title_bar_color_handle(self)

    def window(self, fg_cl):
        self.configure(fg_color = fg_cl)
        self.title("Settings")
        self.geometry("900x460")
        self.iconbitmap("images/logo.ico")
        self.resizable(False, False)
    
    def gui(self, fg_cl, text_bg, text):
        self.left_frame = ct.CTkFrame(self, width=300, height=460, fg_color=fg_cl, corner_radius=0)
        self.left_frame.pack(side="left",anchor="nw", padx=(0, 100))
        self.center_frame = ct.CTkFrame(self, width=300, height=460, fg_color=fg_cl, corner_radius=0)
        self.center_frame.pack(side="left",anchor="nw")
        self.right_frame = ct.CTkFrame(self, width=300, height=460, fg_color=fg_cl, corner_radius=0)
        self.right_frame.pack(side="right",anchor="nw")

        """ LEFT FRAME """

        self.status_label = ct.CTkLabel(self.left_frame, font=("", 24), text_color=text, text="Status Bar")
        self.status_label.pack(padx=5,pady=5)

        initial_value = int(check.get_config_value("timer"))
        self.timer_var = tk.IntVar(value=initial_value)
        self.timer_box = ct.CTkCheckBox(self.left_frame, text="Timer", checkbox_width=20, checkbox_height=20, text_color=text,
                                        variable=self.timer_var, command=self.update_timer)
        self.timer_box.pack(padx=5,pady=5)

        initial_value = int(check.get_config_value("words_count"))
        self.words_var = tk.IntVar(value=initial_value)
        self.char_line_box = ct.CTkCheckBox(self.left_frame, text="Words", checkbox_width=20, checkbox_height=20, text_color=text,
                                            variable=self.words_var, command=self.update_words)
        self.char_line_box.pack(padx=5,pady=5)

        initial_value = int(check.get_config_value("status_run"))
        self.run_var = tk.IntVar(value=initial_value)
        self.run_box = ct.CTkCheckBox(self.left_frame, text="Run", checkbox_width=20, checkbox_height=20, text_color=text,
                                      variable=self.run_var, command=self.update_run)
        self.run_box.pack(padx=5,pady=5)

        initial_value = int(check.get_config_value("notifications"))
        self.notifications_var = tk.IntVar(value=initial_value)
        self.not_box = ct.CTkCheckBox(self.left_frame, text="Notifications", checkbox_width=20, checkbox_height=20, text_color=text,
                                      variable=self.notifications_var, command=self.update_notifications)
        self.not_box.pack(padx=5,pady=5)

        initial_value = int(check.get_config_value("server_status"))
        self.server_var = tk.IntVar(value=initial_value)
        self.server_box = ct.CTkCheckBox(self.left_frame, text="Server status", checkbox_width=20, checkbox_height=20, text_color=text,
                                      variable=self.server_var, command=self.update_server)
        self.server_box.pack(padx=5,pady=5)

        """ CENTER FRAME """
        self.misc_lab = ct.CTkLabel(self.center_frame, font=("", 24), text_color=text, text="Misc")
        self.misc_lab.pack(padx=5,pady=5)

        initial_value = int(check.get_config_value("auto_save"))
        self.auto_save_var = tk.IntVar(value=initial_value)
        self.auto_save_box = ct.CTkCheckBox(self.center_frame, text="Auto save", checkbox_width=20, checkbox_height=20, text_color=text,
                                      variable=self.auto_save_var, command=self.update_auto_save)
        self.auto_save_box.pack(padx=5,pady=5)

        initial_value = int(check.get_config_value("session"))
        self.session_var = tk.IntVar(value=initial_value)
        self.session_box = ct.CTkCheckBox(self.center_frame, text="Session", checkbox_width=20, checkbox_height=20, text_color=text,
                                      variable=self.session_var, command=self.update_session)
        self.session_box.pack(padx=5,pady=5)

        self.reset_session = ct.CTkButton(self.center_frame,text="Reset Session", width=100)
        self.reset_session.pack(padx=5,pady=5)

    def update_notifications(self):
        view_menu.notifications(self.status)

    def update_timer(self):
        view_menu.hide_unhide_timer(self.status)

    def update_run(self):
        view_menu.hide_unhide_run(self.status)

    def update_words(self):
        view_menu.hide_unhide_words(self.status)

    def update_server(self):
        view_menu.hide_unhide_server_status(self.status)

    def update_auto_save(self):
        if int(check.get_config_value("auto_save")) == 0:
            check.update_config_file("auto_save", 1)
        elif int(check.get_config_value("auto_save")) == 1:
            check.update_config_file("auto_save", 0)
        
    def update_session(self):
        if int(check.get_config_value("session")) == 0:
            check.update_config_file("session", 1)
        elif int(check.get_config_value("session")) == 1:
            check.update_config_file("session", 0)