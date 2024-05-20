import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import os

import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Config import check

# Definim o variabilă globală pentru a ține numele fișierului deschis
opened_filename = None

def new_file(text, window, status_bar):
    global opened_filename  # Specificăm că vrem să folosim variabila globală

    opened_filename = None

    text.delete("1.0", tk.END)
    window.redraw()

    # Actualizează textul status barului
    status_bar.update_text("New File")


def open_file(text, window, status_bar):
    global opened_filename  # Specificăm că vrem să folosim variabila globală

    filename = filedialog.askopenfilename(filetypes=[("All files", "*.*")])

    if filename:
        opened_filename = filename  # Actualizăm numele fișierului deschis

        with open(filename, "r") as file:
            file_content = file.read()

            text.delete("1.0", tk.END) 
            text.insert("1.0", file_content) 
            window.redraw()
        status_bar.update_text("Opened: " + filename)
    
def open_folder(treeview, status_bar):
    global opened_filename
    
    # Deschide dialogul pentru selectarea unui director
    folder_path = filedialog.askdirectory()
    
    if folder_path:
        
        opened_filename = folder_path
        
        treeview.populate_treeview(folder_path)
        
        status_bar.update_text("Opened folder: " + folder_path)


def save_file(text, status_bar):
    global opened_filename  # Specificăm că vrem să folosim variabila globală

    if opened_filename:
        content = text.get("1.0", tk.END)

        with open(opened_filename, "w") as file:
            file.write(content)
        status_bar.update_text("Saved: " + opened_filename)
    else:
        # Dacă nu există un fișier deschis anterior, apelăm funcția save_as_file()
        save_as_file(text, status_bar)

def save_as_file(text, status_bar):
    global opened_filename  # Specificăm că vrem să folosim variabila globală

    content = text.get("1.0", tk.END)
    filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    if filename:
        opened_filename = filename  # Actualizăm numele fișierului deschis

        with open(filename, "w") as file:
            file.write(content)
        status_bar.update_text("Saved: " + opened_filename)

version_window_opened = False

def custom_file(statusbar):
    global version_window_opened

    if not version_window_opened:
        version_window_opened = True
        version_window = ctk.CTk()
        version_window.title("CodeNimble - New File")
        fg_cl = "#2b2b2b"
        text_bg = "#4a4a4a"
        text = "white"
        if (check.get_config_value("theme") == 0):
            fg_cl = "#2b2b2b"
            text_bg = "#4a4a4a"
            text = "white"
        elif (check.get_config_value("theme") == 1):
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
            filename = text_box.get().strip()  # Obține textul introdus de utilizator
            if filename:
                # Adaugă extensia .txt dacă utilizatorul nu a furnizat nicio extensie
                if not "." in filename:
                    filename += ".txt"
                try:
                    with open(filename, "x") as file:  # Creează fișierul cu numele introdus de utilizator
                        statusbar.update_text("Created: " + filename)
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
    # Directorul curent
    current_dir = os.getcwd()

    # Numele fișierului de configurare
    default_file = "default_file.txt"

    # Calea către fișierul de configurare
    config_file_path = os.path.join(current_dir, default_file)

    # Verificăm dacă fișierul de configurare există
    if os.path.exists(config_file_path):
        # Dacă există, citim locația fișierului curent din fișierul de configurare
        with open(config_file_path, "r") as file:
            saved_filename = file.read().strip()
            # Verificăm dacă locația este validă și dacă există fișierul
            if os.path.exists(saved_filename):
                opened_filename = saved_filename  # Actualizăm numele fișierului deschis

                with open(saved_filename, "r") as file:
                    file_content = file.read()

                    text.delete("1.0", tk.END) 
                    text.insert("1.0", file_content) 
                    window.redraw()
                status_bar.update_text("Opened default file: " + saved_filename)
                
                return
            else:
                # Dacă locația nu este validă sau fișierul nu există, nu facem nimic
                pass

def save_as_default(statusbar):
    global opened_filename

    # Directorul curent
    current_dir = os.getcwd()

    # Numele fișierului de configurare
    default_file = "default_file.txt"

    # Calea către fișierul de configurare
    config_file_path = os.path.join(current_dir, default_file)

    # Verificăm dacă există o locație salvată în variabila globală opened_filename
    if opened_filename:
        # Salvăm locația fișierului curent în fișierul de configurare
        with open(config_file_path, "w") as file:
            file.write(opened_filename)
        statusbar.update_text("Saved default file location")

def delete_file(file_name, statusbar):
    try:
        os.remove(file_name)
        statusbar.update_text("Removed default file")
    except OSError as e:
        pass

def current_file():
    global opened_filename
    return opened_filename
