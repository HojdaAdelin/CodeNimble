import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog

import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from GUI import gui

def new_file(text, window):
    text.delete("1.0", tk.END)
    window.redraw()

def open_file(text, window):
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    if filename:
        
        with open(filename, "r") as file:
            file_content = file.read()

            text.delete("1.0", tk.END) 
            text.insert("1.0", file_content) 
            window.redraw()


def save_file():
    pass

def save_as_file():
    pass