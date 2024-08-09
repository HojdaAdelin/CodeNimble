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

def run(text_widget):
    file_path=file_menu.current_file()
    if file_path is None:
        messagebox.showerror("Error", "No files are open.")
        return
    if file_path.endswith(".cpp"):
        run_cpp_file(text_widget)
    elif file_path.endswith(".py"):
        run_python_file(text_widget)
    else:
        messagebox.showerror("Error", "Only .cpp & .py files can be run.")
        return

def run_cpp_file(text_widget):
    file_path = file_menu.current_file()
    
    code_content = text_widget.get("1.0", "end-1c")
    
    current_file_dir = os.path.dirname(file_path)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp", mode='w', encoding='utf-8', dir=current_file_dir) as temp_file:
        temp_file.write(code_content)
        temp_file_path = temp_file.name
    
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    executable_name = os.path.join(current_file_dir, f"{base_name}.exe")
    error_log = os.path.join(current_file_dir, f"{base_name}_error.log")
    compile_command = f"g++ {temp_file_path} -o {executable_name} 2> {error_log}"
    
    compile_process = subprocess.run(compile_command, shell=True, cwd=current_file_dir)
    
    if compile_process.returncode != 0:
        run_command = f"start cmd /k type {error_log}"
        subprocess.run(run_command, shell=True, cwd=current_file_dir)
        time.sleep(1)
    else:
        run_command = f"start cmd /k {os.path.basename(executable_name)}"
        subprocess.run(run_command, shell=True, cwd=current_file_dir)
        time.sleep(1)
    
    os.remove(temp_file_path)
    if os.path.exists(executable_name):
        os.remove(executable_name)
    if os.path.exists(error_log):
        os.remove(error_log)

def run_python_file(text_widget):
    file_path = file_menu.current_file()  
    code_content = text_widget.get("1.0", "end-1c")
    
    current_file_dir = os.path.dirname(file_path)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode='w', encoding='utf-8', dir=current_file_dir) as temp_file:
        temp_file.write(code_content)
        temp_file_path = temp_file.name
    
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    error_log = os.path.join(current_file_dir, f"{base_name}_error.log")
    run_command = f"python {temp_file_path} 2> {error_log}"
    
    run_process = subprocess.run(run_command, shell=True, cwd=current_file_dir)
    
    if run_process.returncode != 0:
        show_errors_command = f"start cmd /k type {error_log}"
        subprocess.run(show_errors_command, shell=True, cwd=current_file_dir)
        time.sleep(1)
    else:
        result_command = f"start cmd /k python {os.path.basename(temp_file_path)}"
        subprocess.run(result_command, shell=True, cwd=current_file_dir)
        time.sleep(1)
    
    os.remove(temp_file_path)
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
    pre_input = root.right_panel_frame.input_box.get("1.0", "end-1c").strip()
    if len(pre_input) == 0:
        messagebox.showerror("Error", "You need to set the pre-input from right panel!")
        return
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

        expected_output = root.right_panel_frame.expected_box.get("1.0", "end-1c").strip()
        passing = True
        if len(expected_output) != 0:
            new_output = root.right_panel_frame.output_box.get("1.0", "end-1c").strip()
            
            expected_words = expected_output.split()
            new_words = new_output.split()
            
            if len(expected_words) != len(new_words):
                passing = False
                root.right_panel_frame.output_label.configure(text_color="red", text="Different number of words")
            else:
                for i in range(len(new_words)):
                    if expected_words[i] != new_words[i]:
                        passing = False
                        root.right_panel_frame.output_label.configure(text_color="red", text=f"Wrong answer on test case {i + 1}")
                        break

        if passing:
            root.right_panel_frame.output_label.configure(text_color="green", text="All test cases passed")

                    

    except Exception as e:
        root.right_panel_frame.output_box.delete("1.0", "end")
        root.right_panel_frame.output_box.insert("1.0", f"Exception occurred:\n{str(e)}")
    
    finally:
        if os.path.exists(cpp_file_path):
            os.remove(cpp_file_path)
        if os.path.exists(executable_path):
            os.remove(executable_path)