import tkinter as tk
import customtkinter as ct

class Terminal(ct.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(height=150, fg_color="green", bg_color="green")
