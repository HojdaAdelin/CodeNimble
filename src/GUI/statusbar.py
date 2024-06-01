import tkinter as tk
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from API import get_version

class StatusBar(tk.Frame):
    def __init__(self, master, text="", font_size=28, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.current_version = "1.4"
        self.latest_version = get_version.get_latest_version_from_github("HojdaAdelin", "CodeNimble")
        self.text = tk.StringVar(value=text)
        self.configure(bg="#333333")
        font = ("Arial", font_size)
        
        self.new_version_label = tk.Label(self, text="New version available", font=font, bg="green", fg="black")
        self.status_label = tk.Label(self, textvariable=self.text, anchor="e", padx=40, font=font, bg="#333333", fg="white")
        self.status_label.grid(row=0, column=1, sticky="e") 

        self.grid_columnconfigure(1, weight=1)  

        if self.latest_version > self.current_version:
            self.new_version_label.grid(row=0, column=0, sticky="w") 

    def update_text(self, new_text):
        self.text.set(new_text)
    def set_status(self, text):
        self.text.set(text)