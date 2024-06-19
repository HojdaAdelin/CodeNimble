import customtkinter as ctk
import tkinter as tk
from ctypes import byref, sizeof, c_int, windll
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Config import check

class ServerPanel(ctk.CTk):
    def __init__(self):
        super().__init__()

        fg_cl = "#2b2b2b"
        text_bg = "#4a4a4a"
        text = "white"
        if int(check.get_config_value("theme")) == 0:
            fg_cl = "#2b2b2b"
            text_bg = "#4a4a4a"
            text = "white"
        elif int(check.get_config_value("theme")) == 1:
            fg_cl = "white"
            text_bg = "#f0f0f0"
            text = "black"

        self.configure(fg_color=fg_cl)
        self.title("Server Panel")
        self.geometry("1000x600")
        self.iconbitmap("images/logo.ico")
        self.resizable(False, False)

        tb_color = 0x333333
        if int(check.get_config_value("theme")) == 0:
            tb_color = 0x333333
        elif int(check.get_config_value("theme")) == 1:
            tb_color = 0xFFFFFF
        else:
            tb_color = 0x333333

        HWND = windll.user32.GetParent(self.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(
            HWND,
            35,
            byref(c_int(tb_color)),
            sizeof(c_int))