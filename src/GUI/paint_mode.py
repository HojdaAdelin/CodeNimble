import customtkinter as ctk
from tkinter import Canvas, Frame
import tkinter as tk
from ctypes import byref, sizeof, c_int, windll
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Config import check

class PaintApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Paint Mode")
        self.geometry("1000x600")  # Increased height to accommodate the tool_bar
        self.resizable(False, False)  # Make the window size fixed

        self.set_icon("images/logo.ico")  # Set the window icon

        if int(check.get_config_value("theme")) == 0:
            self.bg_color = "#333333"
        elif int(check.get_config_value("theme")) == 1:
            self.bg_color = "#f0f0f0"
        else:
            self.bg_color = "#333333"

        # Tool bar frame
        self.tool_bar = Frame(self, height=50, bg=self.bg_color)
        self.tool_bar.pack(fill=tk.X)

        # Button 1: Pencil
        self.btn_pencil = ctk.CTkButton(self.tool_bar, text="Pencil", command=self.use_pencil)
        self.btn_pencil.pack(side=tk.LEFT, padx=5, pady=5)

        # Button 2: Eraser
        self.btn_eraser = ctk.CTkButton(self.tool_bar, text="Eraser", command=self.use_eraser)
        self.btn_eraser.pack(side=tk.LEFT, padx=5, pady=5)

        # Button 3: Clear
        self.btn_clear = ctk.CTkButton(self.tool_bar, text="Clear", command=self.clear_canvas)
        self.btn_clear.pack(side=tk.LEFT, padx=5, pady=5)

        self.canvas = Canvas(self, bg='white', width=500, height=500)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

        self.old_x = None
        self.old_y = None
        self.current_tool = "pencil"  # Initializăm current_tool cu "pencil"

        # Title bar color handle
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

    def set_icon(self, icon_path):
        try:
            self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error setting icon: {e}")

    def paint(self, event):
        if self.old_x and self.old_y:
            if self.current_tool == "pencil":
                self.canvas.create_line(self.old_x, self.old_y, event.x, event.y, width=3, fill='black', capstyle=tk.ROUND, smooth=tk.TRUE)
            elif self.current_tool == "eraser":
                self.erase(event.x, event.y)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x = None
        self.old_y = None

    def clear_canvas(self):
        self.canvas.delete("all")

    def use_eraser(self):
        self.current_tool = "eraser"
        self.canvas.configure(cursor="circle")

    def use_pencil(self):
        self.current_tool = "pencil"
        self.canvas.configure(cursor="arrow")

    def erase(self, x, y):
        # Draw a white rectangle to simulate erasing
        erase_size = 20  # Size of the eraser
        self.canvas.create_rectangle(x - erase_size, y - erase_size, x + erase_size, y + erase_size, fill="white", outline="white")