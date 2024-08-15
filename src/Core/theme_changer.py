import os
import sys
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Config import check
from Core import themes

use_template_window = None

def update_theme(menu, home, file_m, edit, view, template, textures, utility,
                home_drop, file_drop, edit_drop, view_drop, template_drop, textures_drop,
                utility_drop,
                statusbar_instance, scroll, self, treeview_frame, treeview_frame_menu, treeview_frame_folder_menu,
                scroll_tab_bar):
    global use_template_window
    if use_template_window:
        return
    
    use_template_window = True
    select_template_window = ctk.CTk()
    select_template_window.title("CodeNimble - Update theme")
    select_template_window.iconbitmap("images/logo.ico")
    
    fg_cl, text_bg, text, hover_color, button_color, button_hover_color, button_text_color = themes.return_default_win_color(check.get_config_value("theme"))

    w = 400 
    h = 500 
    ws = select_template_window.winfo_screenwidth()
    hs = select_template_window.winfo_screenheight()
    x = (ws / 2 + 500) - (w / 2)
    y = (hs / 2 + 200) - (h / 2)
    select_template_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    select_template_window.resizable(False, False)
    select_template_window.configure(fg_color=fg_cl)

    curr_dir = os.getcwd()
    tmp_folder = os.path.join(curr_dir, 'Themes')
    if not os.path.isdir(tmp_folder):
        os.makedirs(tmp_folder)

    def update_listbox(event=None):
        search_term = search_box.get().strip().lower()
        listbox.delete(0, tk.END)
        for file in os.listdir(tmp_folder):
            if search_term in file.lower():
                listbox.insert(tk.END, file)

    search_label = ctk.CTkLabel(select_template_window, text="Search:", font=("Arial", 20), fg_color=fg_cl, text_color=text)
    search_label.pack(pady=(20, 0))
    search_box = tk.Entry(select_template_window, width=30, font=("Arial", 30), bg=text_bg, foreground=text, 
                          insertbackground='white', selectbackground="#616161", borderwidth=0)
    search_box.pack()
    search_box.bind("<KeyRelease>", update_listbox)

    listbox = tk.Listbox(select_template_window, width=30, height=15, font=("Arial", 30), bg=text_bg, foreground=text,
                         selectbackground="#616161", borderwidth=0)
    listbox.pack(pady=(20, 0))

    update_listbox()

    def update_theme():
        new_theme = listbox.curselection()
        if not new_theme:
            messagebox.showerror("Error", "No theme selected!")
            return
        theme = listbox.get(new_theme[0])
        theme = theme[:-5]
        check.update_config_file("theme", theme)
        themes.use_theme(check.get_config_value("theme"),menu, home, file_m, edit, view, template, textures, utility,
                                                                                         home_drop, file_drop, edit_drop, view_drop, template_drop, textures_drop,
                                                                                         utility_drop,
                                                                                         statusbar_instance, scroll, self, treeview_frame, treeview_frame_menu, treeview_frame_folder_menu,
                                                                                         scroll_tab_bar)
        
    use_button = ctk.CTkButton(select_template_window, text="Use", width=200, command=update_theme, fg_color=button_color, hover_color=button_hover_color, text_color=button_text_color)
    use_button.pack(pady=(10, 0))

    def on_closing():
        global use_template_window
        select_template_window.destroy()
        use_template_window = False 

    themes.title_bar_color_handle(select_template_window)

    select_template_window.protocol("WM_DELETE_WINDOW", on_closing)
    select_template_window.mainloop()