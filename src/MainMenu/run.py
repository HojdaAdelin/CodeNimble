import subprocess
import os
import sys
import tkinter as tk
from tkinter import messagebox
import threading
import time

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from MainMenu import file_menu

def run_cpp_file(tree):
    file_path = file_menu.current_file()
    if file_path is None:
        messagebox.showerror("Error", "No files are open.")
        return

    if not file_path.endswith(".cpp"):
        messagebox.showerror("Error", "Only .cpp files can be run.")
        return
    
    # Compilarea fișierului .cpp
    executable_name = file_path.replace(".cpp", ".exe")
    error_log = file_path.replace(".cpp", "_error.log")
    compile_command = f"g++ {file_path} -o {executable_name} 2> {error_log}"
    
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