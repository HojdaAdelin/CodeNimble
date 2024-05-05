import tkinter as tk
import customtkinter as ctk
import webbrowser

version_window_opened = False
changelog_window_opened = False

import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Config import check

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
        h = 80 

        ws = version_window.winfo_screenwidth()
        hs = version_window.winfo_screenheight()

        x = (ws/2+500) - (w/2)
        y = (hs/2+200) - (h/2)

        version_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        version_window.iconbitmap("images/logo.ico")
        version_window.resizable(False, False)
        version_window.configure(fg_color = fg_cl)

        version_label = ctk.CTkLabel(version_window, text="Version: 1.2", font=("Arial", 20), text_color=text)
        version_label.pack(pady=25)

        # Funcție pentru a reseta version_window_opened la False după ce închidem fereastra
        def on_closing():
            global version_window_opened
            version_window_opened = False
            version_window.destroy()

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
        h = 400 

        ws = changelog_window.winfo_screenwidth()
        hs = changelog_window.winfo_screenheight()

        x = (ws/2+500) - (w/2)
        y = (hs/2+200) - (h/2)

        changelog_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        changelog_window.resizable(False, False)
        changelog_window.configure(fg_color = fg_cl)

        version_label = ctk.CTkLabel(changelog_window, text="Version: 1.2", font=("Arial", 20), text_color=text)
        version_label.pack(pady=10)
        content_label = ctk.CTkLabel(changelog_window, text="• New templates: C, Java, Html, C++ Competitive\n• Save default file location\n• Remove default file\n• Replace all\n• Fix save as file\n• Binds", font=("Arial", 20), text_color=text)
        content_label.pack()

        # Funcție pentru a reseta changelog_window_opened la False după ce închidem fereastra
        def on_closing():
            global changelog_window_opened
            changelog_window_opened = False
            changelog_window.destroy()

        changelog_window.protocol("WM_DELETE_WINDOW", on_closing)
        changelog_window.mainloop()

def open_links(url):
    webbrowser.open(url)
