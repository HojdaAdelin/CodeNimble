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
        self.num_lines = tk.IntVar()
        self.num_words = tk.IntVar()
        self.configure(bg="#333333")
        font = ("Arial", font_size)
        
        self.new_version_label = tk.Label(self, text="New version available", font=font, bg="green", fg="black")
        self.num_stats_label = tk.Label(self, text="Lines: 0, Words: 0 ", font=font, anchor="e")
        self.status_label = tk.Label(self, textvariable=self.text, anchor="e", font=font, bg="#333333", fg="white")

        self.status_label.pack(side="right")
        self.num_stats_label.pack(side="right")

        if self.latest_version > self.current_version:
            self.new_version_label.pack(side="left")

    def update_text(self, new_text):
        self.text.set(new_text)

    def set_status(self, text):
        self.text.set(text)

    def update_stats(self, text_widget):
        content = text_widget.get("1.0", tk.END)
        lines = len(content.split("\n")) - 1
        words = len(content.split())
        self.num_lines.set(lines)
        self.num_words.set(words)
        stats_text = f"Lines: {lines}, Words: {words}"
        self.num_stats_label.config(text=stats_text)