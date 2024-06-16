from ctypes import byref, c_int, sizeof, windll
import tkinter as tk
import customtkinter as ctk

import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from MainMenu import file_menu
from MainMenu import edit_menu
from Config import check

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

def custom_template():
    global template_window
    if not template_window:
        template_window = True
        create_template_window = ctk.CTk()
        create_template_window.title("CodeNimble - Create Templates")
        create_template_window.iconbitmap("images/logo.ico")
        
        fg_cl = "#2b2b2b"
        text_bg = "#4a4a4a"
        text = "white"
        if (int(check.get_config_value("theme")) == 0):
            fg_cl = "#2b2b2b"
            text_bg = "#4a4a4a"
            text = "white"
        elif (int(check.get_config_value("theme")) == 1):
            fg_cl = "white"
            text_bg = "#f0f0f0"
            text = "black"

        w = 500 
        h = 600 
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

        name_label = ctk.CTkLabel(create_template_window,text="Name:", font=("Arial", 20), fg_color=fg_cl, text_color=text).pack(pady=(40,0))
        name_box = tk.Entry(create_template_window, width=32, font=("Arial", 30), bg=text_bg, foreground=text, 
                            insertbackground='white',
                            selectbackground="#616161", borderwidth=0)
        name_box.pack()

        content_label = ctk.CTkLabel(create_template_window,text="Text:", font=("Arial", 20), fg_color=fg_cl, text_color=text).pack(pady=(20,0))
        text_box = ctk.CTkTextbox(create_template_window, width=350, height=380, font=("Arial", 16), fg_color=text_bg, text_color=text)
        text_box.pack()

        create_button = ctk.CTkButton(create_template_window, text="Create", width=200)
        create_button.pack(pady=(10,0))

        def on_closing():
            global template_window
            template_window = False
            create_template_window.destroy()

        tb_color = 0x333333
        if (int(check.get_config_value("theme")) == 0):
            tb_color = 0x333333
        elif (int(check.get_config_value("theme")) == 1):
            tb_color = 0xFFFFFF
        else:
            tb_color = 0x333333
        
        HWND = windll.user32.GetParent(create_template_window.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(
            HWND,
            35,
            byref(c_int(tb_color)),
            sizeof(c_int))

        create_template_window.protocol("WM_DELETE_WINDOW", on_closing)
        create_template_window.mainloop()