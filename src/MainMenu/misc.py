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
from MainMenu import themes

def exit_application(root):
    exit()

def version_info():
    global version_window_opened
    if not version_window_opened:
        version_window_opened = True
        version_window = ctk.CTk()
        version_window.title("CodeNimble - Version")
        fg_cl, text_bg, text, hover_color, button_color, button_hover_color, button_text_color = themes.return_default_win_color(check.get_config_value("theme"))
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

        current_version_label = ctk.CTkLabel(version_window, text="Current version: 2.0", font=("Arial", 20), text_color=text)
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

def create_card(parent, title, description, bg_color, row, col):
    card = ctk.CTkFrame(
        parent,
        width=250,
        height=250,
        corner_radius=15, 
        fg_color=bg_color 
    )
    card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    # Titlu
    title_label = ctk.CTkLabel(card, text=title, font=("Arial", 20), text_color="white")
    title_label.pack(pady=(5, 10))

    # Descriere
    description_label = ctk.CTkLabel(card, text=description, font=("Arial", 16), text_color="white")
    description_label.pack(pady=(0, 10))

def changelog_inf():
    
    global changelog_window_opened
    if not changelog_window_opened:
        changelog_window_opened = True
        changelog_window = ctk.CTk()
        changelog_window.title("CodeNimble - Change log")
        changelog_window.iconbitmap("images/logo.ico")
        fg_cl, text_bg, text, hover_color, button_color, button_hover_color, button_text_color = themes.return_default_win_color(check.get_config_value("theme"))
        w = 900 
        h = 650 

        ws = changelog_window.winfo_screenwidth()
        hs = changelog_window.winfo_screenheight()

        x = (ws/2+500) - (w/2)
        y = (hs/2+200) - (h/2)

        changelog_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        changelog_window.resizable(False, False)
        changelog_window.configure(fg_color = fg_cl)
        
        changelog_window.grid_rowconfigure(1, weight=1)
        changelog_window.grid_rowconfigure(2, weight=1)
        changelog_window.grid_columnconfigure(0, weight=1)
        changelog_window.grid_columnconfigure(1, weight=1)
        changelog_window.grid_columnconfigure(2, weight=1)

        title_label = ctk.CTkLabel(changelog_window, text="Change log - major features", font=("Arial", 24), text_color=text)
        title_label.grid(row=0, column=1, pady=20)

        create_card(changelog_window, "Local Server", "Local server now\n have only one\n interface where\n you can find all\n functionalities in\n the same place.\nAlso the security have\nbeen improved by adding\na password when starting\nthe local server.", "lightblue", 1, 0)
        create_card(changelog_window, "Snippets code", "Now you can create\nyour own code \"shortcut\"\nby creating a snippet\ncode.\nYou can find the\nnew snippet code in\nthe suggestion list\nwith the tag \"snippet\".", "lightgreen", 1, 1)
        create_card(changelog_window, "Python support", "New python support\nincluding code suggestions,\ncode highlight\nand code run.", "lightcoral", 2, 0)
        create_card(changelog_window, "New input & output,", "New input & output system.\nIn the right panel\nyou cand find input,\noutput, expected output.\nYou can set the input\n and expected output then you can\nuse run with pre-input\n and this will display the\noutput from the source code\nand then it will be\ncompared witht the expected\noutput.", "lightgoldenrod", 2, 1)
        create_card(changelog_window, "Submit code", "With this new feature\nyou no longer need to use\nthe browser to submit code.\nYou can submit code on\npbinfo.ro for now but in the\nfuture will be more platforms.", "gray", 1, 2)
        create_card(changelog_window, "Fetch test cases", "You can now use this\nfeature to fetch pre-test\nsamples from different platforms\nto the input & expected output.\nSupported platforms: pbinfo.ro,\nkilonova.ro, codeforces.com, atcoder.jp.", "pink", 2, 2)
        
        def open_l():
            open_links("https://hojdaadelin.github.io/code-nimble/src/blogs.html")

        view_more = ctk.CTkButton(changelog_window, text="View more >", font=("Arial", 16), text_color=button_text_color, command=open_l, fg_color=button_color, hover_color=button_hover_color)
        view_more.grid(row=3, column=2, pady=(0,5), sticky="e", padx=10)

        def on_closing():
            global changelog_window_opened
            changelog_window_opened = False
            changelog_window.destroy()

        themes.title_bar_color_handle(changelog_window)

        changelog_window.protocol("WM_DELETE_WINDOW", on_closing)
        changelog_window.mainloop()

def open_links(url):
    webbrowser.open(url)