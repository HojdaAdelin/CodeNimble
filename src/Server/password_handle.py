import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from ctypes import byref, sizeof, c_int, windll

import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Config import check
from MainMenu import themes

class PasswordHandle(ctk.CTk):
    def __init__(self, textbox):
        super().__init__()
        self.textbox = textbox
        fg_cl, text_bg, text, hover_color = themes.return_default_win_color(check.get_config_value("theme"))
        self.window(fg_cl)
        self.gui(fg_cl, text_bg, text)
        self.title_color()

    def title_color(self):
        themes.title_bar_color_handle(self)

    def window(self, fg_cl):
        self.configure(fg_color = fg_cl)
        self.title("Password Handle")
        self.geometry("400x220")
        self.iconbitmap("images/logo.ico")
        self.resizable(False, False)

    def gui(self, fg_cl, text_bg, text):
        self.label = ctk.CTkLabel(self, text="Password",text_color=text)
        self.label.pack(pady=(40, 10))

        self.entry = ctk.CTkEntry(self, width=300, fg_color=text_bg, text_color=text)
        self.entry.pack(pady=10)

        self.save_button = ctk.CTkButton(self, text="Enter", command=self.password_handle)
        self.save_button.pack(pady=20)

        self.statusbar = ctk.CTkLabel(self, text="", fg_color=fg_cl, text_color=text)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def password_handle(self):
        password = self.entry.get().strip()
        if password:
            self.textbox.server_password(password)
            self.after(2, self.quit())
        else:
            messagebox.showerror("Error", "Password entry cannot be empty.")