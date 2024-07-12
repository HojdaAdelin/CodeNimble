import tkinter as tk
import customtkinter as ct

class Terminal(ct.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.h = 150
        self.configure(height=self.h, fg_color="green", bg_color="green")

    def return_height(self):
        return self.h
    
    def update_height(self, val):
        self.h = val
