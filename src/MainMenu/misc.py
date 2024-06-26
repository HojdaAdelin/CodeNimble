import tkinter as tk
import customtkinter as ctk
import webbrowser
from ctypes import byref, sizeof, c_int, windll

version_window_opened = False
changelog_window_opened = False
guide_window_opened = False

import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Config import check
from API import get_version
from MainMenu import themes

def exit_application(root):
    root.quit()

def version_info():
    global version_window_opened
    if not version_window_opened:
        version_window_opened = True
        version_window = ctk.CTk()
        version_window.title("CodeNimble - Version")
        fg_cl, text_bg, text, hover_color = themes.return_default_win_color(check.get_config_value("theme"))
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

        current_version_label = ctk.CTkLabel(version_window, text="Current version: 1.5", font=("Arial", 20), text_color=text)
        current_version_label.pack(pady=(25,0))
        version_label = ctk.CTkLabel(version_window, text="Latest version: "+get_version.get_latest_version_from_github("HojdaAdelin", "CodeNimble"), font=("Arial", 20), text_color=text)
        version_label.pack(pady=0)
        # Funcție pentru a reseta version_window_opened la False după ce închidem fereastra
        def on_closing():
            global version_window_opened
            version_window_opened = False
            version_window.destroy()

        themes.title_bar_color_handle(version_window)

        version_window.protocol("WM_DELETE_WINDOW", on_closing)
        version_window.mainloop()

def changelog_inf():
    
    global changelog_window_opened
    if not changelog_window_opened:
        changelog_window_opened = True
        changelog_window = ctk.CTk()
        changelog_window.title("CodeNimble - Change log")
        changelog_window.iconbitmap("images/logo.ico")
        fg_cl, text_bg, text, hover_color = themes.return_default_win_color(check.get_config_value("theme"))
        w = 500 
        h = 600 

        ws = changelog_window.winfo_screenwidth()
        hs = changelog_window.winfo_screenheight()

        x = (ws/2+500) - (w/2)
        y = (hs/2+200) - (h/2)

        changelog_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        changelog_window.resizable(False, False)
        changelog_window.configure(fg_color = fg_cl)
        
        version_label = ctk.CTkLabel(changelog_window, text="Version: 1.5", font=("Arial", 20), text_color=text)
        version_label.pack(pady=10)
        content_label = ctk.CTkLabel(changelog_window, text="• Paint Mode\n• Integrate paint window in app\n• Change colors in paint mode\n• Local Server\n• Profile\n• Fixed autocompletion when list isn't mapped\n• Connected users list in panel\n• Fix Ctrl+Backspace\n• Autocomplete for CPP when ENTER\n• Button 2 bind in file tab\n• Tabs in paint mode\n• Text highlighted for python\n• Autocomplete \", \', \*\n• Settings\n• Settings for status bar\n• Design updates\n• Fixed save\n• Added \"*\" in file tab\n• New theme system\n• Ocean theme\n• Documentation", font=("Arial", 20), text_color=text)
        content_label.pack()

        # Funcție pentru a reseta changelog_window_opened la False după ce închidem fereastra
        def on_closing():
            global changelog_window_opened
            changelog_window_opened = False
            changelog_window.destroy()

        themes.title_bar_color_handle(changelog_window)

        changelog_window.protocol("WM_DELETE_WINDOW", on_closing)
        changelog_window.mainloop()

def open_links(url):
    webbrowser.open(url)

def guide():
    global guide_window_opened
    if not guide_window_opened:
        guide_window_opened = True
        guide_window = ctk.CTk()
        guide_window.title("CodeNimble - Change log")
        guide_window.iconbitmap("images/logo.ico")
        
        fg_cl, text_bg, text, hover_color = themes.return_default_win_color(check.get_config_value("theme"))

        w = 500 
        h = 600 
        ws = guide_window.winfo_screenwidth()
        hs = guide_window.winfo_screenheight()
        x = (ws / 2 + 500) - (w / 2)
        y = (hs / 2 + 200) - (h / 2)
        guide_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        guide_window.resizable(False, False)
        guide_window.configure(fg_color=fg_cl)

        version_label = ctk.CTkLabel(guide_window, text="Guide", font=("Arial", 24), text_color=text)
        version_label.pack(pady=10)

        # Adăugarea label-urilor în fiecare frame
        h1 = ctk.CTkLabel(guide_window, text="Autocompletion - type keywords with caps then ENTER:\nKeywords: FOR, IF, WHILE, DO, INT, VOID, LONG\n\n Input & output - this is a useful feature, to use this\n open input & output file from File menu then save input text\n and run, then in output you will se the output file.\nOBS: this work when you use ifstream & ofstream in C++", font=("Arial", 18), text_color=text)
        h1.pack(pady=10, padx=10)

        # Funcție pentru a reseta changelog_window_opened la False după ce închidem fereastra
        def on_closing():
            global guide_window_opened
            guide_window_opened = False
            guide_window.destroy()

        themes.title_bar_color_handle(guide_window)

        guide_window.protocol("WM_DELETE_WINDOW", on_closing)
        guide_window.mainloop()