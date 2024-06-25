import subprocess
import os
import sys
import tkinter as tk
from tkinter import messagebox
import threading
import time
import tempfile

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from MainMenu import file_menu

def run_cpp_file(tree, text_widget):
    file_path = file_menu.current_file()
    if file_path is None:
        messagebox.showerror("Error", "No files are open.")
        return

    if not file_path.endswith(".cpp"):
        messagebox.showerror("Error", "Only .cpp files can be run.")
        return

    # Extragem conținutul din text_widget
    code_content = text_widget.get("1.0", "end-1c")
    
    # Creăm un fișier temporar pentru a scrie codul
    with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp", mode='w', encoding='utf-8') as temp_file:
        temp_file.write(code_content)
        temp_file_path = temp_file.name
    
    # Compilarea fișierului temporar .cpp
    executable_name = temp_file_path.replace(".cpp", ".exe")
    error_log = temp_file_path.replace(".cpp", "_error.log")
    compile_command = f"g++ {temp_file_path} -o {executable_name} 2> {error_log}"
    
    # Rularea comenzii de compilare
    compile_process = subprocess.run(compile_command, shell=True)
    
    if compile_process.returncode != 0:
        # Dacă există erori de compilare, deschidem cmd și afișăm erorile
        run_command = f"start cmd /k type {error_log}"
        subprocess.run(run_command, shell=True)
    else:
        # Dacă compilarea reușește, rulăm fișierul executabil în cmd
        run_command = f"start cmd /k {executable_name}"
        subprocess.run(run_command, shell=True)
        time.sleep(1)
        output = file_menu.return_output()
        if output:
            with open(output, "r") as file:
                file_content = file.read()
                tree.output.configure(state="normal")
                tree.output.delete("1.0", tk.END)
                tree.output.insert("1.0", file_content)
                tree.output.configure(state="disabled")
    
    # Ștergem fișierul temporar după rulare
    os.remove(temp_file_path)
    os.remove(executable_name)
    if os.path.exists(error_log):
        os.remove(error_log)

# Exemplu de utilizare într-o funcție sau într-un buton:
# run_cpp_file(tree, text_widget)
