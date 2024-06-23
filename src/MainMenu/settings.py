import customtkinter as ct
from tkinter import *
from ctypes import byref, sizeof, c_int, windll

import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Config import check

class SettingsApp(ct.CTk):
    def __init__(self):
        super().__init__()

        fg_cl, text_bg, text = self.theme()
        self.window(fg_cl)
        self.gui(fg_cl, text_bg, text)
        self.title_color()

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
        self.title("Settings")
        self.geometry("900x460")
        self.iconbitmap("images/logo.ico")
        self.resizable(False, False)

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
    
    def gui(self, fg_cl, text_bg, text):
        self.left_frame = ct.CTkFrame(self, width=300, height=460, fg_color=fg_cl, corner_radius=0)
        self.left_frame.pack(side="left",anchor="nw")
        self.center_frame = ct.CTkFrame(self, width=300, height=460, fg_color=fg_cl, corner_radius=0)
        self.center_frame.pack(side="left",anchor="nw")
        self.right_frame = ct.CTkFrame(self, width=300, height=460, fg_color=fg_cl, corner_radius=0)
        self.right_frame.pack(side="right",anchor="nw")

        self.status_label = ct.CTkLabel(self.left_frame, font=("", 24), text_color=text, text="Status Bar")
        self.status_label.pack(padx=5,pady=5)
        self.timer_box = ct.CTkCheckBox(self.left_frame, text="Timer", checkbox_width=20, checkbox_height=20, text_color=text)
        self.timer_box.pack(padx=5,pady=5)
        self.char_line_box = ct.CTkCheckBox(self.left_frame, text="Words", checkbox_width=20, checkbox_height=20, text_color=text)
        self.char_line_box.pack(padx=5,pady=5)
        self.run_box = ct.CTkCheckBox(self.left_frame, text="Run", checkbox_width=20, checkbox_height=20, text_color=text)
        self.run_box.pack(padx=5,pady=5)
        self.not_box = ct.CTkCheckBox(self.left_frame, text="Notifications", checkbox_width=20, checkbox_height=20, text_color=text)
        self.not_box.pack(padx=5,pady=5)