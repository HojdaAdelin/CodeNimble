import tkinter as tk
import customtkinter as ct
from ctypes import byref, sizeof, c_int, windll

import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Config import check

def dark_theme(menu_bar, cascade1, cascade2, 
               cascade3, cascade4, cascade5, cascade6,
               cascade7,
               drop1, drop2, drop3, drop4, drop5, drop6,
               drop7,
               status, text, win, tree):
    check.update_config_file("theme", 0)
    menu_bar.configure(bg_color="#333333")
    cascade1.configure(hover_color="#4d4d4d", text_color="white")
    cascade2.configure(hover_color="#4d4d4d", text_color="white")
    cascade3.configure(hover_color="#4d4d4d", text_color="white")
    cascade4.configure(hover_color="#4d4d4d", text_color="white")
    cascade5.configure(hover_color="#4d4d4d", text_color="white")
    cascade6.configure(hover_color="#4d4d4d", text_color="white")
    cascade7.configure(hover_color="#4d4d4d", text_color="white")

    drop1.configure(fg_color="#333333", text_color="white",hover_color="#4d4d4d", bg_color="#333333")
    drop2.configure(fg_color="#333333", text_color="white",hover_color="#4d4d4d", bg_color="#333333")
    drop3.configure(fg_color="#333333", text_color="white",hover_color="#4d4d4d", bg_color="#333333")
    drop4.configure(fg_color="#333333", text_color="white",hover_color="#4d4d4d", bg_color="#333333")
    drop5.configure(fg_color="#333333", text_color="white",hover_color="#4d4d4d", bg_color="#333333")
    drop6.configure(fg_color="#333333", text_color="white",hover_color="#4d4d4d", bg_color="#333333")
    drop7.configure(fg_color="#333333", text_color="white",hover_color="#4d4d4d", bg_color="#333333")
    status.configure(bg="#333333")
    status.status_label.configure(bg="#333333", fg="white")
    text.text.configure(bg="#2b2b2b", foreground="white",insertbackground='white',selectbackground="#4d4d4d")
    text.scrollbar.configure(fg_color="#2b2b2b", button_color="#5c5c5c", button_hover_color="#858585")
    text.scrollhor.configure(fg_color="#2b2b2b", button_color="#5c5c5c", button_hover_color="#858585")
    text.numberLines.configure(bg='#333333')
    win.configure(fg_color="#333333")
    HWND = windll.user32.GetParent(win.winfo_id())
    windll.dwmapi.DwmSetWindowAttribute(
            HWND,
            35,
            byref(c_int(0x333333)),
            sizeof(c_int))
    text.redraw()
    text.pack_forget()
    text.pack(fill="both", expand=True, side="right")

    tree.treestyle.configure(
            "Treeview",
            background="#333333",  # Schimba culoarea de fundal
            fieldbackground="#333333",
            foreground = "white",
            bordercolor = "#333333"   # Schimba culoarea textului
        )
    tree.treestyle.map('Treeview', 
                           background=[('selected', "#858585")],
                           foreground=[('selected', "white")])

def light_theme(menu_bar, cascade1, cascade2, 
               cascade3, cascade4, cascade5, cascade6,
               cascade7,
               drop1, drop2, drop3, drop4, drop5, drop6,
               drop7,
               status, text, win, tree):
    
    check.update_config_file("theme", 1)
    menu_bar.configure(bg_color="white")
    cascade1.configure(hover_color="#ebebeb", text_color="black")
    cascade2.configure(hover_color="#ebebeb", text_color="black")
    cascade3.configure(hover_color="#ebebeb", text_color="black")
    cascade4.configure(hover_color="#ebebeb", text_color="black")
    cascade5.configure(hover_color="#ebebeb", text_color="black")
    cascade6.configure(hover_color="#ebebeb", text_color="black")
    cascade7.configure(hover_color="#ebebeb", text_color="black")
    drop1.configure(fg_color="white", text_color="black",hover_color="#ebebeb", bg_color="white")
    drop2.configure(fg_color="white", text_color="black",hover_color="#ebebeb", bg_color="white")
    drop3.configure(fg_color="white", text_color="black",hover_color="#ebebeb", bg_color="white")
    drop4.configure(fg_color="white", text_color="black",hover_color="#ebebeb", bg_color="white")
    drop5.configure(fg_color="white", text_color="black",hover_color="#ebebeb", bg_color="white")
    drop6.configure(fg_color="white", text_color="black",hover_color="#ebebeb", bg_color="white")
    drop7.configure(fg_color="white", text_color="black",hover_color="#ebebeb", bg_color="white")
    status.configure(bg="white")
    status.status_label.configure(bg="white", fg="black")
    text.text.configure(bg="#f0f0f0", foreground="black",insertbackground='black',selectbackground="#d6d6d6")
    text.scrollbar.configure(fg_color="#f0f0f0", button_color="#b0b0b0", button_hover_color="#cccccc")
    text.scrollhor.configure(fg_color="#f0f0f0", button_color="#b0b0b0", button_hover_color="#cccccc")
    text.numberLines.configure(bg='white')
    win.configure(fg_color="white")
    HWND = windll.user32.GetParent(win.winfo_id())
    windll.dwmapi.DwmSetWindowAttribute(
            HWND,
            35,
            byref(c_int(0xFFFFFF)),
            sizeof(c_int))
    text.redraw()
    text.pack_forget()
    text.pack(fill="both", expand=True, side="right")

    tree.treestyle.configure(
            "Treeview",
            background="white",  # Schimba culoarea de fundal
            fieldbackground="white",
            foreground = "black",
            bordercolor = "white"  # Schimba culoarea textului
        )
    tree.treestyle.map('Treeview', 
                           background=[('selected', "#ebebeb")],
                           foreground=[('selected', "black")])