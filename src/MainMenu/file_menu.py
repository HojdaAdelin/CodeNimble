import tkinter as tk
from tkinter import filedialog

# Definim o variabilă globală pentru a ține numele fișierului deschis
opened_filename = None

def new_file(text, window):
    global opened_filename  # Specificăm că vrem să folosim variabila globală

    # Resetează numele fișierului deschis anterior
    opened_filename = None

    text.delete("1.0", tk.END)
    window.redraw()

def open_file(text, window):
    global opened_filename  # Specificăm că vrem să folosim variabila globală

    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    if filename:
        opened_filename = filename  # Actualizăm numele fișierului deschis

        with open(filename, "r") as file:
            file_content = file.read()

            text.delete("1.0", tk.END) 
            text.insert("1.0", file_content) 
            window.redraw()

def save_file(text):
    global opened_filename  # Specificăm că vrem să folosim variabila globală

    if opened_filename:
        content = text.get("1.0", tk.END)

        with open(opened_filename, "w") as file:
            file.write(content)
    else:
        # Dacă nu există un fișier deschis anterior, apelăm funcția save_as_file()
        save_as_file(text)

def save_as_file(text):
    global opened_filename  # Specificăm că vrem să folosim variabila globală

    content = text.get("1.0", tk.END)
    filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    if filename:
        opened_filename = filename  # Actualizăm numele fișierului deschis

        with open(filename, "w") as file:
            file.write(content)
