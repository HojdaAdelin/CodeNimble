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

    #root.pack_forget()
    root.redraw()
    #root.pack(fill="both", expand=True, side="right")


def zoom_out(root):
    ante_size = check.get_config_value("zoom")
    if (int(ante_size) - 4 > 20):
        check.update_config_file("zoom", int(ante_size) - 4)
    
    #root.pack_forget()
    root.redraw()
    #root.pack(fill="both", expand=True, side="right")

def reset_zoom(root):
    check.update_config_file("zoom", 28)
    
    #root.pack_forget()
    root.redraw()
    #root.pack(fill="both", expand=True, side="right")

def toggle_fullscreen(window):
    if window.state() == "zoomed":
        window.state("normal")
    else:
        window.state("zoomed")

def hide_unhide_treeview(treeview_frame: TreeviewFrame, text):

    if treeview_frame.winfo_ismapped():  # Verificăm dacă TreeviewFrame-ul este vizibil
        treeview_frame.grid_forget()  # Dacă da, îl ascundem
        text.grid_forget()
        text.grid(row=1, column=0,columnspan=2,sticky="nswe")
    else:
        text.grid_forget()
        treeview_frame.grid(row=1, column=0, sticky="nsw") 
        text.grid(row=1, column=0,columnspan=2,sticky="nswe", padx=(600,0))

def hide_unhide_input_output(tree):
    if tree.input_label.winfo_ismapped():
        tree.input_label.grid_forget()
        tree.output_label.grid_forget()
        tree.input.grid_forget()
        tree.output.grid_forget()
    else:
        tree.input_label.grid(row=1, column=0, padx=(5, 5))
        tree.input.grid(row=2, column=0, sticky="nsew", padx=(5, 5))
        tree.output_label.grid(row=3, column=0, padx=(5, 5))
        tree.output.grid(row=4, column=0, sticky="nsew", padx=(5, 5))

def hide_unhide_statusbar(status):

    if status.winfo_ismapped():
        status.grid_forget()
        check.update_config_file("status", int(0))
    else:
        status.grid(row=2, column=0,columnspan=2, sticky="ew")
        check.update_config_file("status", int(1))

def notifications(status):
    if int(check.get_config_value("notifications")) == 0:
        check.update_config_file("notifications", 1)
        status.num_stats_label.pack_forget()
        status.run_img.pack_forget()
        status.status_label.pack(side="right")
        status.num_stats_label.pack(side="right")
        status.run_img.pack(side="right", padx=10)
    elif int(check.get_config_value("notifications")) == 1:
        check.update_config_file("notifications", 0)
        status.status_label.pack_forget()
    else:
        check.update_config_file("notifications", 1)
        status.num_stats_label.pack_forget()
        status.run_img.pack_forget()
        status.status_label.pack(side="right")
        status.num_stats_label.pack()
        status.run_img.pack(side="right", padx=10)