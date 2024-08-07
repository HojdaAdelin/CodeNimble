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

def hide_unhide_treeview(treeview_frame: TreeviewFrame, text, r_panel):
    if treeview_frame.winfo_ismapped(): 
        treeview_frame.grid_forget() 
        text.grid_forget()
        if r_panel.winfo_ismapped(): 
            text.grid(row=1, column=0,columnspan=2,sticky="nswe", padx=(0,440))
        else:
            text.grid(row=1, column=0,columnspan=2,sticky="nswe")
    else:
        text.grid_forget()
        treeview_frame.grid(row=1, column=0, sticky="nsw") 
        if r_panel.winfo_ismapped():
            text.grid(row=1, column=0,columnspan=2,sticky="nswe", padx=(600,440))
        else:
            text.grid(row=1, column=0,columnspan=2,sticky="nswe", padx=(600,0))

def hide_unhide_right_panel(text, panel, tree):
    if panel.winfo_ismapped():
        panel.grid_forget()
        text.grid_forget()
        if tree.winfo_ismapped():
            text.grid(row=1, column=0,columnspan=2,sticky="nswe", padx=(600,0))
        else:
            text.grid(row=1, column=0,columnspan=2,sticky="nswe")
    else:
        text.grid_forget()
        panel.grid(row=1,column=1,sticky="nse")
        if tree.winfo_ismapped():
            text.grid(row=1, column=0,columnspan=2,sticky="nswe", padx=(600,440))
        else:
            text.grid(row=1, column=0,columnspan=2,sticky="nswe", padx=(0,440))

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
        if int(check.get_config_value("words_count")) == 1:
            status.num_stats_label.pack_forget()
        if int(check.get_config_value("status_run")) == 1:
            status.run_img.pack_forget()
        if int(check.get_config_value("server_status")) == 1:
            status.server_status.pack_forget()
        status.status_label.pack(side="right")
        if int(check.get_config_value("words_count")) == 1:
            status.num_stats_label.pack(side="right")
        if int(check.get_config_value("status_run")) == 1:
            status.run_img.pack(side="right", padx=10)
        if int(check.get_config_value("server_status")) == 1:
            status.server_status.pack(side="right")
    elif int(check.get_config_value("notifications")) == 1:
        check.update_config_file("notifications", 0)
        status.status_label.pack_forget()
    else:
        check.update_config_file("notifications", 1)
        if int(check.get_config_value("words_count")) == 1:
            status.num_stats_label.pack_forget()
        if int(check.get_config_value("status_run")) == 1:
            status.run_img.pack_forget()
        if int(check.get_config_value("server_status")) == 1:
            status.server_status.pack_forget()
        status.status_label.pack(side="right")
        if int(check.get_config_value("words_count")) == 1:
            status.num_stats_label.pack(side="right")
        if int(check.get_config_value("status_run")) == 1:
            status.run_img.pack(side="right", padx=10)
        if int(check.get_config_value("server_status")) == 1:
            status.server_status.pack(side="right")

def hide_unhide_timer(status):
    if int(check.get_config_value("timer")) == 0:
        check.update_config_file("timer", 1)
        status.timer_frame.pack(side="left", anchor="w")
    elif int(check.get_config_value("timer")) == 1:
        check.update_config_file("timer", 0)
        status.timer_frame.pack_forget()
    else:
        check.update_config_file("timer", 1)
        status.timer_frame.pack(side="left", anchor="w")

def hide_unhide_run(status):
    if int(check.get_config_value("status_run")) == 0:
        check.update_config_file("status_run", 1)
        if int(check.get_config_value("server_status")) == 1:
            status.server_status.pack_forget()
        status.run_img.pack(side="right", padx=10)
        if int(check.get_config_value("server_status")) == 1:
            status.server_status.pack(side="right")
    elif int(check.get_config_value("status_run")) == 1:
        check.update_config_file("status_run", 0)
        status.run_img.pack_forget()
    else:
        check.update_config_file("status_run", 1)
        if int(check.get_config_value("server_status")) == 1:
            status.server_status.pack_forget()
        status.run_img.pack(side="right", padx=10)
        if int(check.get_config_value("server_status")) == 1:
            status.server_status.pack(side="right")

def hide_unhide_words(status):
    if int(check.get_config_value("words_count")) == 0:
        check.update_config_file("words_count", 1)
        if int(check.get_config_value("status_run")) == 1:
            status.run_img.pack_forget()
        if int(check.get_config_value("server_status")) == 1:
            status.server_status.pack_forget()
        status.num_stats_label.pack(side="right")
        if int(check.get_config_value("status_run")) == 1:
            status.run_img.pack(side="right", padx=10)
        if int(check.get_config_value("server_status")) == 1:
            status.server_status.pack(side="right")
    elif int(check.get_config_value("words_count")) == 1:
        check.update_config_file("words_count", 0)
        status.num_stats_label.pack_forget()
    else:
        check.update_config_file("words_count", 1)
        if int(check.get_config_value("status_run")) == 1:
            status.run_img.pack_forget()
        if int(check.get_config_value("server_status")) == 1:
            status.server_status.pack_forget()
        status.num_stats_label.pack(side="right")
        if int(check.get_config_value("status_run")) == 1:
            status.run_img.pack(side="right", padx=10)
        if int(check.get_config_value("server_status")) == 1:
            status.server_status.pack(side="right")

def hide_unhide_server_status(status):
    if int(check.get_config_value("server_status")) == 0:
        check.update_config_file("server_status", 1)
        status.server_status.pack(side="right")
    elif int(check.get_config_value("server_status")) == 1:
        check.update_config_file("server_status", 0)
        status.server_status.pack_forget()
    else:
        check.update_config_file("server_status", 1)
        status.server_status.pack(side="right")