import tkinter as tk
import customtkinter as ctk
import webbrowser
from ctypes import byref, sizeof, c_int, windll

version_window_opened = False
changelog_window_opened = False

import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Config import check
from API import get_version

def exit_application(root):
    root.quit() 

def version_info():
    global version_window_opened
    if not version_window_opened:
        version_window_opened = True
        version_window = ctk.CTk()
        version_window.title("CodeNimble - Version")
        fg_cl = "#2b2b2b"
        text = "white"
        if (check.get_config_value("theme") == 0):
            fg_cl = "#2b2b2b"
            text = "white"
        elif (check.get_config_value("theme") == 1):
            fg_cl = "white"
            text = "black"
        w = 300 
        h = 100 

        ws = version_window.winfo_screenwidth()
        hs = version_window.winfo_screenheight()

        x = (ws/2+500) - (w/2)
        y = (hs/2+200) - (h/2)

        version_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        version_window.iconbitmap("images/logo.ico")
        version_window.resizable(False, False)
        version_window.configure(fg_color = fg_cl)

        current_version_label = ctk.CTkLabel(version_window, text="Current version: 1.3", font=("Arial", 20), text_color=text)
        current_version_label.pack(pady=(25,0))
        version_label = ctk.CTkLabel(version_window, text="Latest version: "+get_version.get_latest_version_from_github("HojdaAdelin", "CodeNimble"), font=("Arial", 20), text_color=text)
        version_label.pack(pady=0)
        # Funcție pentru a reseta version_window_opened la False după ce închidem fereastra
        def on_closing():
            global version_window_opened
            version_window_opened = False
            version_window.destroy()

        tb_color = 0x333333
        if (check.get_config_value("theme") == 0):
            tb_color = 0x333333
        elif (check.get_config_value("theme") == 1):
            tb_color = 0xFFFFFF
        else:
            tb_color = 0x333333
        
        HWND = windll.user32.GetParent(version_window.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(
            HWND,
            35,
            byref(c_int(tb_color)),
            sizeof(c_int))

        version_window.protocol("WM_DELETE_WINDOW", on_closing)
        version_window.mainloop()

def changelog_inf():
    
    global changelog_window_opened
    if not changelog_window_opened:
        changelog_window_opened = True
        changelog_window = ctk.CTk()
        changelog_window.title("CodeNimble - Change log")
        changelog_window.iconbitmap("images/logo.ico")
        fg_cl = "#2b2b2b"
        text = "white"
        if (check.get_config_value("theme") == 0):
            fg_cl = "#2b2b2b"
            text = "white"
        elif (check.get_config_value("theme") == 1):
            fg_cl = "white"
            text = "black"
        w = 500 
        h = 500 

        ws = changelog_window.winfo_screenwidth()
        hs = changelog_window.winfo_screenheight()

        x = (ws/2+500) - (w/2)
        y = (hs/2+200) - (h/2)

        changelog_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        changelog_window.resizable(False, False)
        changelog_window.configure(fg_color = fg_cl)
        
        version_label = ctk.CTkLabel(changelog_window, text="Version: 1.3", font=("Arial", 20), text_color=text)
        version_label.pack(pady=10)
        content_label = ctk.CTkLabel(changelog_window, text="• Utility menu\n• Run code\n• Bind for Ctrl+Backspace\n• New version available notify in status bar\n• Binds for replace & find\n• Treeview\n• Open folder\n• Close folder\n• Open files from treeview\n• Delete files from Treeview\n• Move files & folders in treeview\n• Toggle treeview\n• Fix zoom\n• Bind for Run\n• Add file in treeview folders\n• Change all windows title bars", font=("Arial", 20), text_color=text)
        content_label.pack()

        # Funcție pentru a reseta changelog_window_opened la False după ce închidem fereastra
        def on_closing():
            global changelog_window_opened
            changelog_window_opened = False
            changelog_window.destroy()

        tb_color = 0x333333
        if (check.get_config_value("theme") == 0):
            tb_color = 0x333333
        elif (check.get_config_value("theme") == 1):
            tb_color = 0xFFFFFF
        else:
            tb_color = 0x333333
        
        HWND = windll.user32.GetParent(changelog_window.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(
            HWND,
            35,
            byref(c_int(tb_color)),
            sizeof(c_int))

        changelog_window.protocol("WM_DELETE_WINDOW", on_closing)
        changelog_window.mainloop()

def open_links(url):
    webbrowser.open(url)
