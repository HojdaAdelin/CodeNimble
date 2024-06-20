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

class ProfileApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        fg_cl, text_bg, text = self.theme()
        self.window(fg_cl)
        self.gui(fg_cl, text_bg, text)
        self.title_color()
        self.check_profile()

    def title_color(self):
        tb_color = 0x333333
        if (int(check.get_config_value("theme")) == 0):
            tb_color = 0x333333
        elif (int(check.get_config_value("theme")) == 1):
            tb_color = 0xFFFFFF
        else:
            tb_color = 0x333333
        
        HWND = windll.user32.GetParent(self.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(
            HWND,
            35,
            byref(c_int(tb_color)),
            sizeof(c_int))

    def window(self, fg_cl):
        self.configure(fg_color = fg_cl)
        self.title("Profile")
        self.geometry("400x220")
        self.iconbitmap("images/logo.ico")
        self.resizable(False, False)

    def gui(self, fg_cl, text_bg, text):
        self.label = ctk.CTkLabel(self, text="Profile Name",text_color=text)
        self.label.pack(pady=(40, 10))

        self.entry = ctk.CTkEntry(self, width=300, fg_color=text_bg, text_color=text)
        self.entry.pack(pady=10)

        self.save_button = ctk.CTkButton(self, text="Save", command=self.save_profile)
        self.save_button.pack(pady=20)

        self.statusbar = ctk.CTkLabel(self, text="", fg_color=fg_cl, text_color=text)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def theme(self):
        fg_cl = "#2b2b2b"
        text_bg = "#4a4a4a"
        text = "white"
        if (int(check.get_config_value("theme")) == 0):
            fg_cl = "#2b2b2b"
            text_bg = "#4a4a4a"
            text = "white"
        elif (int(check.get_config_value("theme")) == 1):
            fg_cl = "white"
            text_bg = "#f0f0f0"
            text = "black"
        return fg_cl,text_bg,text

    def save_profile(self):
        profile_name = self.entry.get().strip()
        if profile_name:
            with open("profile.txt", "w") as file:
                file.write(f'name: "{profile_name}"')
            self.statusbar.configure(text="Profile saved successfully.")
        else:
            messagebox.showerror("Error", "Profile name cannot be empty.")

    def check_profile(self):
        if os.path.exists("profile.txt"):
            with open("profile.txt", "r") as file:
                content = file.read().strip()
                if content.startswith('name: "'):
                    profile_name = content[7:-1]
                    self.entry.insert(0, profile_name)
