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

def run_cpp_file(text_widget):
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
    
    os.remove(temp_file_path)
    if os.path.exists(executable_name):
        os.remove(executable_name)
    if os.path.exists(error_log):
        os.remove(error_log)

def pre_input_run(root):
    file_path = file_menu.current_file()
    if file_path is None:
        messagebox.showerror("Error", "No files are open.")
        return
    
    if not file_path.endswith(".cpp"):
        messagebox.showerror("Error", "Only .cpp files can be run.")
        return
    code_content = root.scroll.text.get("1.0", "end-1c")
    
    pre_input = root.right_panel_frame.input_box.get("1.0", "end-1c")
    current_file_dir = os.path.dirname(file_path)
    
    try:
        cpp_file_path = os.path.join(current_file_dir, "temp_code.cpp")
        with open(cpp_file_path, 'w', encoding='utf-8') as cpp_file:
            cpp_file.write(code_content)
        
        executable_path = os.path.join(current_file_dir, "temp_code")

        compile_process = subprocess.run(["g++", cpp_file_path, "-o", executable_path], capture_output=True, text=True)
        
        if compile_process.returncode != 0:
            compile_errors = compile_process.stderr
            root.right_panel_frame.output_box.delete("1.0", "end")
            root.right_panel_frame.output_box.insert("1.0", f"Compilation failed:\n{compile_errors}")
            return

        run_process = subprocess.Popen(executable_path, 
                                       stdin=subprocess.PIPE, 
                                       stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE, 
                                       text=True)
        output, error = run_process.communicate(input=pre_input)

        if run_process.returncode != 0:
            root.right_panel_frame.output_box.delete("1.0", "end")
            root.right_panel_frame.output_box.insert("1.0", f"Runtime error:\n{error}")
            return

        root.right_panel_frame.output_box.delete("1.0", "end")
        root.right_panel_frame.output_box.insert("1.0", output)

    except Exception as e:
        root.right_panel_frame.output_box.delete("1.0", "end")
        root.right_panel_frame.output_box.insert("1.0", f"Exception occurred:\n{str(e)}")
    
    finally:
        if os.path.exists(cpp_file_path):
            os.remove(cpp_file_path)
        if os.path.exists(executable_path):
            os.remove(executable_path)