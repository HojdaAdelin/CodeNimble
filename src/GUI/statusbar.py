import tkinter as tk
import sys
import os
from PIL import Image, ImageTk
from datetime import datetime, timedelta

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from API import get_version
from Config import check

class StatusBar(tk.Frame):
    def __init__(self, master, text="", font_size=32, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.current_version = "2.0"
        self.latest_version = get_version.get_latest_version_from_github("HojdaAdelin", "CodeNimble")
        self.text = tk.StringVar(value=text)
        self.hv_color = tk.StringVar(value="#4d4d4d")
        self.based_color = tk.StringVar(value="#333333")
        self.num_lines = tk.IntVar()
        self.num_words = tk.IntVar()
        self.start_time = None
        self.running = False
        self.timer_paused = False
        self.elapsed_time = timedelta(0)
        self.configure(bg="#333333")
        self.gui(font_size)

    def gui(self, font_size):
        font = ("Arial", font_size)
        
        self.new_version_label = tk.Label(self, text="New version available", font=font, bg="green", fg="black")
        self.num_stats_label = tk.Label(self, text="Lines: 0, Words: 0 ", font=font, anchor="e")
        self.status_label = tk.Label(self, textvariable=self.text, anchor="e", font=font, bg="#333333", fg="white")

        if int(check.get_config_value("notifications")) == 1:
            self.status_label.pack(side="right")
        if int(check.get_config_value("words_count")) == 1:
            self.num_stats_label.pack(side="right")
        
        # Load the image and resize it
        image_path = "images/run.png"  # Update this path if necessary
        image = Image.open(image_path)
        resized_image = image.resize((45, 45), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized_image)
        
        # Create a label to display the image
        self.run_img = tk.Label(self, image=self.image, cursor="hand2")
        if int(check.get_config_value("status_run")) == 1:
            self.run_img.pack(side="right", padx=10)
        
        self.server_status = tk.Label(self, text="Server: none", font=font)
        if int(check.get_config_value("server_status")) == 1:
            self.server_status.pack(side="right")

        self.run_img.bind("<Enter>", self.on_hover)
        self.run_img.bind("<Leave>", self.off_hover)

        if self.latest_version > self.current_version:
            self.new_version_label.pack(side="left")

        self.timer_frame = tk.Frame(self)
        if int(check.get_config_value("timer")) == 1:
            self.timer_frame.pack(side="left", anchor="w")
        self.timer = tk.Label(self.timer_frame, text="00:00:00", font=font)
        self.timer.pack(padx=(0,5))
        self.timer.bind("<Button-1>", self.start_timer)
        self.timer.bind("<Button-2>", self.stop_timer)
        self.timer.bind("<Enter>", self.timer_hover)
        self.timer.bind("<Leave>", self.timer_off_hover)

    def timer_hover(self, event):
        self.timer.config(bg=self.hv_color.get())
        self.timer.config(cursor="hand2")

    def timer_off_hover(self, event):
        self.timer.config(bg=self.based_color.get())
        self.timer.config(cursor="arrow")

    def stop_timer(self, event):
        self.running = False
        self.timer_paused = False
        self.elapsed_time = timedelta(0)
        self.timer.config(text="00:00:00")

    def start_timer(self, event):
        if not self.running:
            self.start_time = datetime.now() - self.elapsed_time
            self.running = True
            self.update_timer()
        else:
            self.timer_paused = not self.timer_paused
            if self.timer_paused:
                self.elapsed_time = datetime.now() - self.start_time
            else:
                self.start_time = datetime.now() - self.elapsed_time
                self.update_timer()
            

    def update_timer(self):
        if self.running and not self.timer_paused:
            elapsed_time = datetime.now() - self.start_time
            hours, remainder = divmod(elapsed_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
            self.timer.config(text=time_str)
            self.after(1000, self.update_timer)

    def on_hover(self, event):
        self.run_img.config(bg=self.hv_color.get())

    def off_hover(self, event):
        self.run_img.config(bg=self.based_color.get())

    def update_text(self, new_text):
        self.text.set(new_text)

    def set_color(self, color):
        self.hv_color.set(color)

    def set_based_color(self, color):
        self.based_color.set(color)

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

    def update_server(self, status):
        status_text = "Server: " + status
        self.server_status.config(text=status_text)