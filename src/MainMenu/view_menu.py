import tkinter as tk

import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Config import check
from GUI.treeview import TreeviewFrame


def zoom_in(root):
    ante_size = check.get_config_value("zoom")
    if (int(ante_size) + 4 < 52):
        check.update_config_file("zoom", int(ante_size) + 4)
    root.redraw()
    root.pack_forget()
    root.pack(fill="both", expand=True, side="right")


def zoom_out(root):
    ante_size = check.get_config_value("zoom")
    if (int(ante_size) - 4 > 20):
        check.update_config_file("zoom", int(ante_size) - 4)
    
    root.redraw()
    root.pack_forget()
    root.pack(fill="both", expand=True, side="right")

def reset_zoom(root):
    check.update_config_file("zoom", 28)
    root.redraw()
    root.pack_forget()
    root.pack(fill="both", expand=True, side="right")

def toggle_fullscreen(window):
    if window.state() == "zoomed":
        window.state("normal")
    else:
        window.state("zoomed")

def hide_unhide_treeview(treeview_frame: TreeviewFrame):

    if treeview_frame.winfo_ismapped():  # Verificăm dacă TreeviewFrame-ul este vizibil
        treeview_frame.pack_forget()  # Dacă da, îl ascundem
    else:
        treeview_frame.pack(fill="both", expand=True) 