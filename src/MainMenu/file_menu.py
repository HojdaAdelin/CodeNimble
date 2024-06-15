import shutil
import tkinter as tk
from tkinter import Menu
from tkinter import filedialog
import customtkinter as ctk
from ctypes import byref, sizeof, c_int, windll
import os

import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Config import check
from MainMenu import edit_menu

opened_filename = None
opened_folder_path = None
opened_input = None
opened_output = None

def new_file(text, window, status_bar):

    global opened_filename 
    opened_filename = None

    text.delete("1.0", tk.END)
    window.redraw()

    status_bar.update_text("New File")


def open_file(text, window, status_bar):
    global opened_filename

    filename = filedialog.askopenfilename(filetypes=[("All files", "*.*")])

    if filename:
        opened_filename = filename 

        with open(filename, "r") as file:
            file_content = file.read()

            text.delete("1.0", tk.END) 
            text.insert("1.0", file_content) 
            window.redraw()
        if not window.tab_bar.check_tab(filename):
            window.tab_bar.add_tab(filename)
        status_bar.update_text("Opened: " + filename)

def open_folder(treeview, status_bar, text, path=None):
    global opened_filename
    global opened_folder_path

    if path:
        opened_folder_path = path
        treeview.populate_treeview(opened_folder_path)
        status_bar.update_text("Opened folder: " + opened_folder_path)
        treeview.grid_forget()
        text.grid_forget()
        treeview.grid(row=1, column=0,sticky="nsw") 
        text.grid(row=1,column=0,columnspan=2,sticky="nswe", padx=(600,0))
        return 

    folder_path = filedialog.askdirectory()
    
    if folder_path:
        opened_folder_path = folder_path  
        treeview.populate_treeview(folder_path)
        status_bar.update_text("Opened folder: " + folder_path)
        treeview.grid_forget()
        text.grid_forget()
        treeview.grid(row=1, column=0,sticky="nsw") 
        text.grid(row=1,column=0,columnspan=2,sticky="nswe", padx=(600,0))

def close_folder(treeview_frame, text):
    global opened_filename
    global opened_folder_path

    if opened_folder_path:
        opened_folder_path = None  
        treeview_frame.clear_treeview()  # Clear the content of the Treeview
        treeview_frame.grid_forget()  # Hide the TreeviewFrame
        text.grid_forget()
        text.grid(row=1, column=0, columnspan=2, sticky="nswe")


def save_file(text, status_bar):
    global opened_filename  

    if opened_filename:
        content = text.get("1.0", tk.END)

        with open(opened_filename, "w") as file:
            file.write(content)
        status_bar.update_text("Saved: " + opened_filename)
    else:
        save_as_file(text, status_bar)

def save_as_file(text, status_bar):
    global opened_filename  
    global opened_folder_path

    content = text.get("1.0", tk.END)
    filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                                             initialdir=opened_folder_path if opened_folder_path else os.getcwd())

    if filename:
        opened_filename = filename 

        with open(filename, "w") as file:
            file.write(content)
        status_bar.update_text("Saved: " + opened_filename)


version_window_opened = False

def custom_file(statusbar, tree, custom_path=None):
    global version_window_opened
    global opened_folder_path
    global opened_filename

    if not version_window_opened:
        version_window_opened = True
        version_window = ctk.CTk()
        version_window.title("CodeNimble - New File")
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
        w = 300 
        h = 100 

        ws = version_window.winfo_screenwidth()
        hs = version_window.winfo_screenheight()

        x = (ws/2+500) - (w/2)
        y = (hs/2+200) - (h/2)

        version_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        version_window.resizable(False, False)
        version_window.iconbitmap("images/logo.ico")
        version_window.configure(fg_color = fg_cl)

        # Adaugă un Entry în fereastra version_window
        text_box = tk.Entry(version_window, width=25, font=("Arial", 30), bg=text_bg, foreground=text, 
                            insertbackground='white',
                            selectbackground="#616161", borderwidth=0)
        text_box.pack(pady=40)

        # Funcția care se activează la apăsarea butonului "Create"
        def create_file():
            global opened_folder_path
            global opened_filename

            filename = text_box.get().strip()  # Obține textul introdus de utilizator
            if filename:
                # Adaugă extensia .txt dacă utilizatorul nu a furnizat nicio extensie
                if not "." in filename:
                    filename += ".txt"
                try:
                    if custom_path:
                        filepath = os.path.join(custom_path, filename)
                    elif opened_folder_path:
                        filepath = os.path.join(opened_folder_path, filename)
                    else:
                        filepath = filename
                    with open(filepath, "x") as file:  # Creează fișierul cu numele introdus de utilizator
                        if custom_path is None:
                            opened_filename = filepath  # Actualizăm variabila globală opened_filename
                        statusbar.update_text("Created: " + filepath)
                        if opened_folder_path:
                            tree.reload_treeview(opened_folder_path if opened_folder_path else os.getcwd())
                            
                except FileExistsError:
                    pass

        # Adaugă un buton "Create" pentru a crea fișierul
        create_button = ctk.CTkButton(version_window, text="Create", command=create_file)
        create_button.pack()

        # Funcție pentru a reseta version_window_opened la False după ce închidem fereastra
        def on_closing():
            global version_window_opened
            version_window_opened = False
            version_window.destroy()

        tb_color = 0x333333
        if (int(check.get_config_value("theme")) == 0):
            tb_color = 0x333333
        elif (int(check.get_config_value("theme")) == 1):
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



def return_file():
    global opened_filename
    
    if opened_filename:
        return os.path.splitext(opened_filename)[1] 
    else:
        return ".txt"  

def create_file(text, ext):
    global opened_filename

    filename = "template" + ext  # Numele de fișier implicit

    # Verifică dacă fișierul cu numele implicit există deja
    count = 1
    while os.path.exists(filename):
        filename = f"template{count}" + ext
        count += 1

    # Creează fișierul .cpp și deschide-l pentru scriere
    with open(filename, "w") as file:
        file.write(text)
    # Actualizează variabila globală opened_filename
    opened_filename = filename

def open_default_file(text, window, status_bar):
    global opened_filename
    opened_filename = check.get_config_value("default_file")
    open_file_by_path(text, status_bar, opened_filename)
    window.tab_bar.add_tab(opened_filename)
    window.redraw()

def save_as_default(statusbar):
    global opened_filename

    global opened_filename
    if opened_filename:
        check.update_config_file("default_file", opened_filename)
        statusbar.update_text("Saved default file location")
    else:
        statusbar.update_text("No files are opened!")

def delete_file(file_name, statusbar):
    global opened_filename  # Specificăm că vrem să folosim variabila globală

    try:
        os.remove(file_name)
        statusbar.update_text("Removed: " + file_name)
        if opened_filename == file_name:
            opened_filename = None  # Setăm opened_filename la None dacă fișierul șters este fișierul deschis
            
    except OSError as e:
        pass


def current_file():
    global opened_filename
    return opened_filename

def update_path(new_path):
    global opened_folder_path
    opened_folder_path = new_path

def update_file_path(new_path):
    global opened_filename
    opened_filename = new_path

def insert_text(text, textbox):
    textbox.delete("1.0", tk.END)
    textbox.insert("1.0", text)

def open_file_by_path(textbox, status_bar, path):
  global opened_filename

  if path:
    
    if os.path.exists(path):
      try:
        
        with open(path, "r") as file:
          file_content = file.read()

        opened_filename = path

        textbox.delete("1.0", tk.END)

        textbox.insert(tk.END, file_content)

        status_bar.update_text("Opened: " + path)
      except FileNotFoundError:
        
        status_bar.update_text("File not found: " + path)
    else:
      
      status_bar.update_text("Invalid file path: " + path)

def return_current_path():
    global opened_folder_path
    return opened_folder_path

def delete_folder(folder_path, statusbar, text, root):
    global opened_filename  # Specificăm că vrem să folosim variabila globală

    try:
        shutil.rmtree(folder_path)
        statusbar.update_text("Removed: " + folder_path)
        if opened_filename and opened_filename.startswith(folder_path):
            opened_filename = None  # Resetăm opened_filename dacă fișierul deschis se află în folderul șters
            text.delete("1.0", tk.END)
            root.redraw()
    except OSError as e:
        statusbar.update_text("Error removing folder: " + str(e))
version_window = None
def rename_file(statusbar, tree, path):
    global version_window
    global opened_filename
    if version_window is None:
        file_path = path
        version_window = ctk.CTk()
        version_window.title("CodeNimble - Rename File")
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
        w = 300 
        h = 100 

        ws = version_window.winfo_screenwidth()
        hs = version_window.winfo_screenheight()

        x = (ws/2+500) - (w/2)
        y = (hs/2+200) - (h/2)

        version_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        version_window.resizable(False, False)
        version_window.iconbitmap("images/logo.ico")
        version_window.configure(fg_color = fg_cl)

        # Adaugă un Entry în fereastra version_window
        text_box = tk.Entry(version_window, width=25, font=("Arial", 30), bg=text_bg, foreground=text, 
                            insertbackground='white',
                            selectbackground="#616161", borderwidth=0)
        text_box.pack(pady=40)

        # Funcția care se activează la apăsarea butonului "Rename"
        def rename(file_path):
            global opened_filename

            new_filename = text_box.get().strip()  # Obține noul nume de fișier introdus de utilizator
            if new_filename:
                # Verifică dacă noul nume nu este același cu cel vechi
                if new_filename != os.path.basename(file_path):
                    new_path = os.path.join(os.path.dirname(file_path), new_filename)
                    try:
                        os.rename(file_path, new_path)  # Redenumește fișierul
                        statusbar.update_text("Renamed: " + file_path + " to " + new_path)
                        tree.reload_treeview(os.path.dirname(file_path))  # Reîncarcă arborele de fișiere pentru directorul părinte
                        
                        # Verifică dacă fișierul redenumit este același cu fișierul deschis în prezent în textbox
                        if opened_filename == file_path:
                            opened_filename = new_path  # Actualizează opened_filename cu noul nume de fișier
                        file_path = new_path  # Actualizează calea fișierului cu noua cale
                        
                    except Exception as e:
                        pass


        # Adaugă un buton "Rename" pentru a redenumi fișierul
        rename_button = ctk.CTkButton(version_window, text="Rename", command=lambda: rename(file_path))
        rename_button.pack()

        # Funcție pentru a reseta version_window la None după ce fereastra se închide
        def on_closing():
            global version_window
            version_window.destroy()
            version_window = None

        tb_color = 0x333333
        if (int(check.get_config_value("theme")) == 0):
            tb_color = 0x333333
        elif (int(check.get_config_value("theme")) == 1):
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

def opened_file_status():
    global opened_filename
    if opened_filename:
        return True
    else:
        return False

def get_content_of_current_file(path=None):
    global opened_filename
    if path:
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        if opened_filename:
            with open(opened_filename, 'r', encoding='utf-8') as file:
                return file.read()
version_windoww = None
def rename_folder(statusbar, tree, folder_path):
    global version_windoww
    global opened_filename
    
    if version_windoww is None:
        version_windoww = ctk.CTk()
        version_windoww.title("CodeNimble - Rename Folder")
        fg_cl = "#2b2b2b"
        text_bg = "#4a4a4a"
        text = "white"
        if int(check.get_config_value("theme")) == 0:
            fg_cl = "#2b2b2b"
            text_bg = "#4a4a4a"
            text = "white"
        elif int(check.get_config_value("theme")) == 1:
            fg_cl = "white"
            text_bg = "#f0f0f0"
            text = "black"
        w = 300 
        h = 100 

        ws = version_windoww.winfo_screenwidth()
        hs = version_windoww.winfo_screenheight()

        x = (ws/2+500) - (w/2)
        y = (hs/2+200) - (h/2)

        version_windoww.geometry('%dx%d+%d+%d' % (w, h, x, y))
        version_windoww.resizable(False, False)
        version_windoww.iconbitmap("images/logo.ico")
        version_windoww.configure(fg_color=fg_cl)

        text_box = tk.Entry(version_windoww, width=25, font=("Arial", 30), bg=text_bg, foreground=text, 
                            insertbackground='white', selectbackground="#616161", borderwidth=0)
        text_box.pack(pady=40)

        def rename(folder_path):
            global opened_filename

            new_foldername = text_box.get().strip()
            if new_foldername:
                if new_foldername != os.path.basename(folder_path):
                    new_path = os.path.join(os.path.dirname(folder_path), new_foldername)
                    try:
                        os.rename(folder_path, new_path)
                        statusbar.update_text("Renamed folder: " + folder_path + " to " + new_path)
                        tree.reload_treeview(os.path.dirname(folder_path))

                        if opened_filename and opened_filename.startswith(folder_path):
                            opened_filename = opened_filename.replace(folder_path, new_path, 1)
                        
                        folder_path = new_path
                    except Exception as e:
                        pass

        rename_button = ctk.CTkButton(version_windoww, text="Rename", command=lambda: rename(folder_path))
        rename_button.pack()

        def on_closing():
            global version_windoww
            version_windoww.destroy()
            version_windoww = None

        tb_color = 0x333333
        if (int(check.get_config_value("theme")) == 0):
            tb_color = 0x333333
        elif (int(check.get_config_value("theme")) == 1):
            tb_color = 0xFFFFFF
        else:
            tb_color = 0x333333
        
        HWND = windll.user32.GetParent(version_windoww.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(tb_color)), sizeof(c_int))

        version_windoww.protocol("WM_DELETE_WINDOW", on_closing)
        version_windoww.mainloop()

def add_folder(statusbar, tree, custom_path=None):
    global version_window_opened

    if not version_window_opened:
        version_window_opened = True
        version_window = ctk.CTk()
        version_window.title("CodeNimble - New Folder")
        fg_cl = "#2b2b2b"
        text_bg = "#4a4a4a"
        text = "white"
        if int(check.get_config_value("theme")) == 0:
            fg_cl = "#2b2b2b"
            text_bg = "#4a4a4a"
            text = "white"
        elif int(check.get_config_value("theme")) == 1:
            fg_cl = "white"
            text_bg = "#f0f0f0"
            text = "black"
        w = 300 
        h = 100 

        ws = version_window.winfo_screenwidth()
        hs = version_window.winfo_screenheight()

        x = (ws/2 + 500) - (w/2)
        y = (hs/2 + 200) - (h/2)

        version_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        version_window.resizable(False, False)
        version_window.iconbitmap("images/logo.ico")
        version_window.configure(fg_color=fg_cl)

        # Adaugă un Entry în fereastra version_window
        text_box = tk.Entry(version_window, width=25, font=("Arial", 30), bg=text_bg, foreground=text, 
                            insertbackground='white',
                            selectbackground="#616161", borderwidth=0)
        text_box.pack(pady=40)

        # Funcția care se activează la apăsarea butonului "Create"
        def create_folder():
            foldername = text_box.get().strip()  # Obține textul introdus de utilizator
            if foldername:
                try:
                    if custom_path:
                        folderpath = os.path.join(custom_path, foldername)
                    elif opened_folder_path:
                        folderpath = os.path.join(opened_folder_path, foldername)
                    else:
                        folderpath = foldername
                    os.makedirs(folderpath, exist_ok=True)  # Creează folderul cu numele introdus de utilizator
                    statusbar.update_text("Created folder: " + folderpath)
                    tree.reload_treeview(opened_folder_path if opened_folder_path else os.getcwd())
                except Exception as e:
                    pass

        # Adaugă un buton "Create" pentru a crea folderul
        create_button = ctk.CTkButton(version_window, text="Create", command=create_folder)
        create_button.pack()

        # Funcție pentru a reseta version_window_opened la False după ce închidem fereastra
        def on_closing():
            global version_window_opened
            version_window_opened = False
            version_window.destroy()

        tb_color = 0x333333
        if (int(check.get_config_value("theme")) == 0):
            tb_color = 0x333333
        elif (int(check.get_config_value("theme")) == 1):
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

def open_input(tree, path=None):
    global opened_input
    if path:
        opened_input = path
        with open(path, "r") as file:
            file_content = file.read()
            tree.input.delete("1.0", tk.END) 
            tree.input.insert("1.0", file_content)
            tree.input_label.configure(text=os.path.basename(path)) 
        return

    filename = filedialog.askopenfilename(filetypes=[("All files", "*.*")])

    if filename:
        opened_input = filename 

        with open(filename, "r") as file:
            file_content = file.read()
            tree.input.delete("1.0", tk.END) 
            tree.input.insert("1.0", file_content) 
            tree.input_label.configure(text=os.path.basename(filename))

def open_output(tree, path=None):
    global opened_output

    if path:
        opened_output = path
        with open(path, "r") as file:
            file_content = file.read()
            tree.output.configure(state="normal")
            tree.output.delete("1.0", tk.END) 
            tree.output.insert("1.0", file_content)
            tree.output.configure(state="disabled")
            tree.output_label.configure(text=os.path.basename(path)) 
        return

    filename = filedialog.askopenfilename(filetypes=[("All files", "*.*")])

    if filename:
        opened_output = filename 

        with open(filename, "r") as file:
            file_content = file.read()
            tree.output.configure(state="normal")
            tree.output.delete("1.0", tk.END) 
            tree.output.insert("1.0", file_content)
            tree.output.configure(state="disabled")
            tree.output_label.configure(text=os.path.basename(filename)) 

def save_input(tree):
    global opened_input
    if opened_input:
        content = tree.input.get("1.0", tk.END)
        with open(opened_input, "w") as file:
            file.write(content)
    else:
        open_input(tree)

        
def return_input():
    global opened_input
    return opened_input

def return_output():
    global opened_output
    return opened_output

def remove_default_file(status):
    check.update_config_file("default_file", 0)
    status.update_text("Removed default file")

def save_as_default_folder(status):
    global opened_folder_path
    if opened_folder_path:
        check.update_config_file("default_folder", opened_folder_path)
        status.update_text("Saved default folder location")
    else:
        status.update_text("No folder is opened!")

def remove_default_folder(status):
    check.update_config_file("default_folder", 0)
    status.update_text("Removed default folder")