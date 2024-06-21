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

        self.theme()

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

        # Color squares
        self.color_squares = []
        colors = ["black", "red", "yellow", "green", "blue"]
        for color in colors:
            square = ctk.CTkButton(self.tool_bar, text="", bg_color=color, fg_color=color, hover_color=color, width=20, height=20, command=lambda c=color: self.change_pencil_color(c))
            square.pack(side=tk.LEFT, padx=5, pady=5)
            self.color_squares.append(square)

        # Tab buttons
        self.tab_buttons = []
        for i in range(5):
            tab_button = ctk.CTkButton(self.tool_bar, text=f"#{i+1}", width=20, height=20, command=lambda i=i: self.switch_tab(i))
            tab_button.pack(side=tk.LEFT, padx=5, pady=5)
            self.tab_buttons.append(tab_button)

        # Canvas frames for each tab
        self.canvases = []
        for i in range(5):
            canvas_frame = Frame(self)
            canvas = Canvas(canvas_frame, bg='white', width=500, height=500)
            canvas.pack(fill=tk.BOTH, expand=True)
            canvas.bind("<B1-Motion>", self.paint)
            canvas.bind("<ButtonRelease-1>", self.reset)
            self.canvases.append((canvas_frame, canvas))

        self.old_x = None
        self.old_y = None
        self.current_tool = "pencil"  # Initializăm current_tool cu "pencil"
        self.pencil_color = "black"  # Culorea default pentru creion

        self.current_canvas_index = 0
        self.show_canvas(self.current_canvas_index)

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

    def theme(self):
        if int(check.get_config_value("theme")) == 0:
            self.bg_color = "#333333"
        elif int(check.get_config_value("theme")) == 1:
            self.bg_color = "#f0f0f0"
        else:
            self.bg_color = "#333333"

    def set_icon(self, icon_path):
        try:
            self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error setting icon: {e}")

    def paint(self, event):
        canvas = self.canvases[self.current_canvas_index][1]
        if self.old_x and self.old_y:
            if self.current_tool == "pencil":
                canvas.create_line(self.old_x, self.old_y, event.x, event.y, width=3, fill=self.pencil_color, capstyle=tk.ROUND, smooth=tk.TRUE)
            elif self.current_tool == "eraser":
                self.erase(event.x, event.y)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x = None
        self.old_y = None

    def clear_canvas(self):
        canvas = self.canvases[self.current_canvas_index][1]
        canvas.delete("all")

    def use_eraser(self):
        self.current_tool = "eraser"
        self.canvases[self.current_canvas_index][1].configure(cursor="circle")

    def use_pencil(self):
        self.current_tool = "pencil"
        self.canvases[self.current_canvas_index][1].configure(cursor="arrow")

    def erase(self, x, y):
        canvas = self.canvases[self.current_canvas_index][1]
        # Draw a white rectangle to simulate erasing
        erase_size = 20  # Size of the eraser
        canvas.create_rectangle(x - erase_size, y - erase_size, x + erase_size, y + erase_size, fill="white", outline="white")

    def change_pencil_color(self, color):
        self.pencil_color = color

    def switch_tab(self, index):
        self.show_canvas(index)

    def show_canvas(self, index):
        self.canvases[self.current_canvas_index][0].pack_forget()
        self.current_canvas_index = index
        self.canvases[self.current_canvas_index][0].pack(fill=tk.BOTH, expand=True)

        # Update tab button states
        for i, button in enumerate(self.tab_buttons):
            if i == index:
                button.configure(fg_color="blue")  # Highlight active tab
            else:
                button.configure(fg_color="gray")  # Default color for inactive tabs