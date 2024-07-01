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
    
    # Obținem directorul fișierului curent
    current_file_dir = os.path.dirname(file_path)
    
    # Creăm un fișier temporar în directorul curent al fișierului
    with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp", mode='w', encoding='utf-8', dir=current_file_dir) as temp_file:
        temp_file.write(code_content)
        temp_file_path = temp_file.name
    
    # Compilarea fișierului temporar .cpp
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    executable_name = os.path.join(current_file_dir, f"{base_name}.exe")
    error_log = os.path.join(current_file_dir, f"{base_name}_error.log")
    compile_command = f"g++ {temp_file_path} -o {executable_name} 2> {error_log}"
    
    # Rularea comenzii de compilare
    compile_process = subprocess.run(compile_command, shell=True, cwd=current_file_dir)
    
    if compile_process.returncode != 0:
        # Dacă există erori de compilare, deschidem cmd și afișăm erorile
        run_command = f"start cmd /k type {error_log}"
        subprocess.run(run_command, shell=True, cwd=current_file_dir)
    else:
        # Dacă compilarea reușește, rulăm fișierul executabil în cmd
        run_command = f"start cmd /k {os.path.basename(executable_name)}"
        subprocess.run(run_command, shell=True, cwd=current_file_dir)
        time.sleep(1)
        output = file_menu.return_output()
        if output and os.path.exists(output):
            with open(output, "r") as file:
                file_content = file.read()
                tree.output.configure(state="normal")
                tree.output.delete("1.0", tk.END)
                tree.output.insert("1.0", file_content)
                tree.output.configure(state="disabled")
    
    # Ștergem fișierul temporar după rulare
    os.remove(temp_file_path)
    if os.path.exists(executable_name):
        os.remove(executable_name)
    if os.path.exists(error_log):
        os.remove(error_log)

# Exemplu de utilizare într-o funcție sau într-un buton:
# run_cpp_file(tree, text_widget)