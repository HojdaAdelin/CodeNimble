from ctypes import byref, c_int, sizeof, windll
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from MainMenu import file_menu
from MainMenu import edit_menu
from Config import check
from MainMenu import themes

template_window = None

cpp_text = """#include <iostream>

int main()
{
    std::cout << "Hello World";
    return 0;
}"""

c_text = """#include <stdio.h>

int main()
{
    printf("Hello World");

    return 0;
}"""

java_text = """public class Main
{
	public static void main(String[] args) {
		System.out.println("Hello World");
	}
}"""

html_text = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    
</body>
</html>"""

competitive_text = """#include <bits/stdc++.h>

using namespace std;

#define ll long long

void solution() {
    
}

int main()
{
    solution();

    return 0;
}"""

def create_template(textbox, root, statusbar, op):
    template_text = """"""
    ext = ""
    ext_misc = ""
    if (op == "cpp"):
        template_text = cpp_text
        ext_misc = "C++"
        ext = ".cpp"
    elif (op == "c"):
        template_text = c_text
        ext_misc = "C"
        ext = ".c"
    elif (op == "java"):
        template_text = java_text
        ext_misc = "Java"
        ext = ".java"
    elif (op == "html"):
        template_text = html_text
        ext_misc = "HTML"
        ext = ".html"
    elif (op == "com"):
        template_text = competitive_text
        ext_misc = "C++ Competitive"
        ext = ".cpp"
    # Inserarea textului în textbox
    edit_menu.clear_text(textbox, root, statusbar)
    textbox.insert("1.0", template_text)
    file_menu.create_file(template_text, ext)
    statusbar.update_text("Used " + ext_misc + " template")
    root.redraw()
    root.tab_bar.add_tab(file_menu.current_file())
    root.highlight_all()

def custom_template():
    global template_window
    if template_window:
        return
    template_window = True

    create_template_window = ctk.CTk()
    create_template_window.title("CodeNimble - Create Templates")
    create_template_window.iconbitmap("images/logo.ico")
    
    fg_cl, text_bg, text, hover_color, button_color, button_hover_color, button_text_color = themes.return_default_win_color(check.get_config_value("theme"))

    w = 460 
    h = 560 
    ws = create_template_window.winfo_screenwidth()
    hs = create_template_window.winfo_screenheight()
    x = (ws / 2 + 500) - (w / 2)
    y = (hs / 2 + 200) - (h / 2)
    create_template_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    create_template_window.resizable(False, False)
    create_template_window.configure(fg_color=fg_cl)

    curr_dir = os.getcwd()
    tmp_folder = os.path.join(curr_dir, 'Templates')
    if not os.path.isdir(tmp_folder):
        os.makedirs(tmp_folder)

    name_label = ctk.CTkLabel(create_template_window, text="Name:", font=("Arial", 20), fg_color=fg_cl, text_color=text)
    name_label.pack(pady=(20, 0))
    name_box = tk.Entry(create_template_window, width=32, font=("Arial", 30), bg=text_bg, foreground=text, 
                        insertbackground='white',
                        selectbackground="#616161", borderwidth=0)
    name_box.pack()

    content_label = ctk.CTkLabel(create_template_window, text="Text:", font=("Arial", 20), fg_color=fg_cl, text_color=text)
    content_label.pack(pady=(20, 0))
    text_box = ctk.CTkTextbox(create_template_window, width=350, height=380, font=("Arial", 16), fg_color=text_bg, text_color=text)
    text_box.pack()

    def create_template():
        template_name_full = name_box.get().strip()
        if '.' in template_name_full:
            template_name, extension = template_name_full.rsplit('.', 1)
        else:
            template_name = template_name_full
            extension = 'txt'  # Default extension if none provided

        template_content = text_box.get("1.0", tk.END).strip()

        if not template_name:
            messagebox.showerror("Error", "Template name cannot be empty!")
            return
        
        template_path = os.path.join(tmp_folder, f"{template_name}.{extension}")

        if os.path.exists(template_path):
            messagebox.showerror("Error", f"Template '{template_name}' already exists!")
            return

        if not template_content:
            messagebox.showerror("Error", "Template content cannot be empty!")
            return

        with open(template_path, 'w') as template_file:
            template_file.write(template_content)
        
        messagebox.showinfo("Success", f"Template '{template_name}.{extension}' created successfully!")

    create_button = ctk.CTkButton(create_template_window, text="Create", width=200, command=create_template, fg_color=button_color, hover_color=button_hover_color, text_color=button_text_color)
    create_button.pack(pady=(10, 0))

    def on_closing():
        global template_window
        template_window = False
        create_template_window.destroy()

    themes.title_bar_color_handle(create_template_window)

    create_template_window.protocol("WM_DELETE_WINDOW", on_closing)
    create_template_window.mainloop()

use_template_window = None

def use_template(textbox, root, statusbar):
    global use_template_window
    if use_template_window:
        return
    
    use_template_window = True
    select_template_window = ctk.CTk()
    select_template_window.title("CodeNimble - Use Templates")
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
    tmp_folder = os.path.join(curr_dir, 'Templates')
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

    def use_selected_template():
        global use_template_window  
        selected = listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No template selected!")
            return
        
        template_file = listbox.get(selected[0])
        template_path = os.path.join(tmp_folder, template_file)
        
        with open(template_path, 'r') as file:
            template_content = file.read()
        
        template_name, extension = os.path.splitext(template_file)
        
        edit_menu.clear_text(textbox, root, statusbar)
        textbox.insert("1.0", template_content)
        file_menu.create_file(template_content, extension)
        statusbar.update_text(f"Used template {template_file}")
        root.redraw()
        root.tab_bar.add_tab(file_menu.current_file())
        root.highlight_all()
        
    use_button = ctk.CTkButton(select_template_window, text="Use", width=200, command=use_selected_template, fg_color=button_color, hover_color=button_hover_color, text_color=button_text_color)
    use_button.pack(pady=(10, 0))

    def on_closing():
        global use_template_window
        select_template_window.destroy()
        use_template_window = False  # Resetăm variabila în cazul în care fereastra este închisă fără a utiliza un template

    themes.title_bar_color_handle(select_template_window)

    select_template_window.protocol("WM_DELETE_WINDOW", on_closing)
    select_template_window.mainloop()
