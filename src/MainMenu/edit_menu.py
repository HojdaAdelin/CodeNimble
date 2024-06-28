import tkinter as tk
import customtkinter as ctk
from ctypes import byref, sizeof, c_int, windll

find_window_opened = False
replace_window_opened = False

import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from MainMenu import themes
from Config import check

def undo_text(widget, root):
    try:
        widget.edit_undo()
        root.redraw()
    except tk.TclError:
        pass

def redo_text(widget, root):
    try:
        widget.edit_redo()
        root.redraw()
    except tk.TclError:
        pass

def copy_text(text, root):
    selected_text = text.get(tk.SEL_FIRST, tk.SEL_LAST)
    text.clipboard_clear()
    text.clipboard_append(selected_text)
    root.redraw()

def paste_text(text, root):
    clipboard_text = text.clipboard_get()
    text.insert(tk.INSERT, clipboard_text)
    root.redraw()

def cut_text(text, root):
    copy_text(text, root)
    text.delete(tk.SEL_FIRST, tk.SEL_LAST)
    root.redraw()

def delete_text(text, root):
    try:
        start_index = text.index(tk.SEL_FIRST)
        end_index = text.index(tk.SEL_LAST)
        text.delete(start_index, end_index)
        root.redraw()
    except tk.TclError:
        pass

def select_all(text):
    text.tag_add(tk.SEL, "1.0", tk.END)
    text.mark_set(tk.INSERT, "1.0")
    text.see(tk.INSERT)

def find_text(scroll_text, scroll):
    global find_window_opened

    if not find_window_opened:
        find_window_opened = True
        find_window = ctk.CTk()
        find_window.title("CodeNimble - Find Text")

        fg_cl, text_bg, text, hover_color = themes.return_default_win_color(check.get_config_value("theme"))

        w = 300 
        h = 100 

        ws = find_window.winfo_screenwidth()
        hs = find_window.winfo_screenheight()

        x = (ws/2+500) - (w/2)
        y = (hs/2+200) - (h/2)

        find_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        find_window.resizable(False, False)
        find_window.iconbitmap("images/logo.ico")
        find_window.configure(fg_color = fg_cl)

        text_box = tk.Entry(find_window, width=25, font=("Arial", 30), bg=text_bg, foreground=text, 
                            insertbackground='white',
                            selectbackground="#616161", borderwidth=0)
        text_box.pack(pady=40)

        def find():
            search_text = text_box.get().strip()
            if search_text:
                start_index = "1.0"
                while True:
                    start_index = scroll_text.search(search_text, start_index, tk.END)
                    if not start_index:
                        break
                    end_index = f"{start_index}+{len(search_text)}c"
                    scroll_text.tag_add("found", start_index, end_index)
                    scroll_text.tag_configure("found", background="gray")
                    start_index = end_index
        
        find_button = ctk.CTkButton(find_window, text="Find", command=find)
        find_button.pack()

        def on_closing():
            global find_window_opened
            find_window_opened = False
            scroll.redraw()
            find_window.destroy()

        themes.title_bar_color_handle(find_window)

        find_window.protocol("WM_DELETE_WINDOW", on_closing)
        find_window.mainloop()

def replace_text(scroll_text, scroll):
    global replace_window_opened

    if not replace_window_opened:
        replace_window_opened = True
        replace_window = ctk.CTk()
        replace_window.title("CodeNimble - Replace Text")
        fg_cl, text_bg, text, hover_color = themes.return_default_win_color(check.get_config_value("theme"))
        w = 500 
        h = 140 

        ws = replace_window.winfo_screenwidth()
        hs = replace_window.winfo_screenheight()

        x = (ws/2+500) - (w/2)
        y = (hs/2+200) - (h/2)

        replace_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        replace_window.resizable(False, False)
        replace_window.iconbitmap("images/logo.ico")
        replace_window.configure(fg_color = fg_cl)

        find_frame = ctk.CTkFrame(replace_window)
        find_frame.pack()
        find_frame.configure(fg_color = fg_cl)
        find_box = tk.Entry(find_frame, width=25, font=("Arial", 30), bg=text_bg, foreground=text, 
                            insertbackground='white',
                            selectbackground="#616161", borderwidth=0)
        find_box.pack(side="left", pady=40)        
        find_button = ctk.CTkButton(find_frame, text="Find")
        find_button.pack(side="right", padx=(10, 0))

        replace_frame = ctk.CTkFrame(replace_window)
        replace_frame.pack()
        replace_frame.configure(fg_color = fg_cl)
        replace_box = tk.Entry(replace_frame, width=25, font=("Arial", 30), bg=text_bg, foreground=text, 
                            insertbackground='white',
                            selectbackground="#616161", borderwidth=0)
        replace_box.pack(side="left")       
        replace_button = ctk.CTkButton(replace_frame, text="Replace")
        replace_button.pack(side="right", padx=(10, 0))
        replace_all_button = ctk.CTkButton(replace_window, text="Replace all")
        replace_all_button.pack(side="right", padx=(10, 38), pady=(10, 0)) 
        

        def on_closing():
            global replace_window_opened
            replace_window_opened = False
            scroll.redraw()
            replace_window.destroy()

        def find():
            search_text = find_box.get().strip()
            if search_text:
                start_index = "1.0"
                scroll_text.tag_remove("found", "1.0", tk.END)
                while True:
                    start_index = scroll_text.search(search_text, start_index, tk.END)
                    if not start_index:
                        break
                    end_index = f"{start_index}+{len(search_text)}c"
                    scroll_text.tag_add("found", start_index, end_index)
                    scroll_text.tag_configure("found", background="gray")
                    start_index = end_index

        def replace():
            search_text = find_box.get().strip()
            replace_text = replace_box.get().strip()
            if search_text and replace_text:
                start_index = "1.0"
                while True:
                    start_index = scroll_text.search(search_text, start_index, tk.END)
                    if not start_index:
                        break
                    end_index = f"{start_index}+{len(search_text)}c"
                    scroll_text.delete(start_index, end_index)
                    scroll_text.insert(start_index, replace_text)
                    start_index = end_index
                    break  
        
        def replace_all():
            search_text = find_box.get().strip()
            replace_text = replace_box.get().strip()
            if search_text and replace_text:
                start_index = "1.0"
                while True:
                    start_index = scroll_text.search(search_text, start_index, tk.END)
                    if not start_index:
                        break
                    end_index = f"{start_index}+{len(search_text)}c"
                    scroll_text.delete(start_index, end_index)
                    scroll_text.insert(start_index, replace_text)
                    start_index = end_index

        find_button.configure(command=find)
        replace_button.configure(command=replace)
        replace_all_button.configure(command=replace_all)

        themes.title_bar_color_handle(replace_window)

        replace_window.protocol("WM_DELETE_WINDOW", on_closing)
        replace_window.mainloop()

def clear_text(text, root, status):
    text.delete("1.0", tk.END)
    root.redraw()
    status.update_text("Clear text")