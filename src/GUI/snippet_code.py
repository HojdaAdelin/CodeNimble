import customtkinter as ct
import tkinter as tk

import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from MainMenu import themes
from Config import check

class SnippetsCode(ct.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Snippets Code")
        self.geometry("800x600")
        self.fg, self.text_bg, self.text, self.hover = themes.return_default_win_color(check.get_config_value("theme"))
        self.configure(fg_color=self.fg, bg_color=self.fg)
        # Crearea Entry în partea de sus
        self.entry = ct.CTkEntry(self, width=760, fg_color=self.text_bg, text_color=self.text)
        self.entry.pack(fill=ct.X, padx=10, pady=10)
        
        # Frame pentru partea de jos (stânga și dreapta)
        bottom_frame = ct.CTkFrame(self, fg_color=self.fg, bg_color=self.fg)
        bottom_frame.pack(fill=ct.BOTH, expand=True, padx=10, pady=10)
        
        # Textbox în stânga
        self.textbox = ct.CTkTextbox(bottom_frame, fg_color=self.text_bg, bg_color=self.text_bg, text_color=self.text)
        self.textbox.pack(side=ct.LEFT, fill=ct.BOTH, expand=True, padx=10, pady=10)
        
        # Listbox în dreapta
        self.listbox = ct.CTkFrame(bottom_frame, fg_color=self.fg, bg_color=self.fg)
        self.listbox.pack(side=ct.RIGHT, fill=ct.BOTH, expand=True, padx=10, pady=10)
    

        self.listbox_list = tk.Listbox(self.listbox, bg=self.text_bg, fg=self.text)
        self.listbox_list.pack(fill=ct.BOTH, expand=True)
        
        
        # Frame pentru butoanele de jos
        button_frame = ct.CTkFrame(self, fg_color=self.fg, bg_color=self.fg)
        button_frame.pack(fill=ct.X, padx=10, pady=10)
        
        # Butoanele Create, Edit, Save
        create_button = ct.CTkButton(button_frame, text="Create")
        create_button.pack(side=ct.LEFT, padx=10)
        
        edit_button = ct.CTkButton(button_frame, text="Edit")
        edit_button.pack(side=ct.LEFT, padx=10)
        
        save_button = ct.CTkButton(button_frame, text="Save")
        save_button.pack(side=ct.LEFT, padx=10)
        
        self.minsize(width=800, height=600)