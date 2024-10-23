import subprocess
import os
import sys
import tempfile
from PySide6.QtWidgets import QApplication, QMessageBox, QTextEdit, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt
import threading
import time


def run(text_widget, file_manager,win):
    file_path = file_manager.get_opened_filename()
    if file_path is None:
        win.status_bar.toggle_inbox_icon(f"No files are open.", "red")
        return
    if file_path.endswith(".cpp"):
        run_cpp_file(text_widget, file_manager)
    elif file_path.endswith(".py"):
        run_python_file(text_widget, file_manager)
    else:
        win.status_bar.toggle_inbox_icon(f"Only .cpp & .py files can be run.", "red")
        return

def run_cpp_file(text_widget, file_manager):
    file_path = file_manager.get_opened_filename()
    print(file_path)  # Verificăm calea fișierului
    code_content = text_widget.toPlainText()
    
    current_file_dir = os.path.dirname(file_path)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp", mode='w', encoding='utf-8', dir=current_file_dir) as temp_file:
        temp_file.write(code_content)
        temp_file_path = temp_file.name
    
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    executable_name = os.path.join(current_file_dir, f"{base_name}.exe")
    error_log = os.path.join(current_file_dir, f"{base_name}_error.log")
    
    # Folosim ghilimele pentru a gestiona calea corect
    compile_command = f'g++ "{temp_file_path}" -o "{executable_name}" 2> "{error_log}"'
    print(compile_command)  # Afișăm comanda pentru debugging
    
    compile_process = subprocess.run(compile_command, shell=True, cwd=current_file_dir)
    
    if compile_process.returncode != 0:
        run_command = f'start cmd /k type "{error_log}"'
        subprocess.run(run_command, shell=True, cwd=current_file_dir)
        time.sleep(1)
    else:
        run_command = f'start cmd /k "{os.path.basename(executable_name)}"'
        subprocess.run(run_command, shell=True, cwd=current_file_dir)
        time.sleep(1)
    
    # Curățăm fișierele temporare
    os.remove(temp_file_path)
    if os.path.exists(executable_name):
        os.remove(executable_name)
    if os.path.exists(error_log):
        os.remove(error_log)

def run_python_file(text_widget, file_manager):
    file_path = file_manager.get_opened_filename()
    code_content = text_widget.toPlainText()
    
    current_file_dir = os.path.dirname(file_path)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode='w', encoding='utf-8', dir=current_file_dir) as temp_file:
        temp_file.write(code_content)
        temp_file_path = temp_file.name
    
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    error_log = os.path.join(current_file_dir, f"{base_name}_error.log")
    
    # Folosim ghilimele pentru a gestiona corect căile de fișiere
    run_command = f'python "{temp_file_path}" 2> "{error_log}"'
    run_process = subprocess.run(run_command, shell=True, cwd=current_file_dir)
    
    if run_process.returncode != 0:
        show_errors_command = f'start cmd /k type "{error_log}"'
        subprocess.run(show_errors_command, shell=True, cwd=current_file_dir)
        time.sleep(1)
    else:
        result_command = f'start cmd /k python "{os.path.basename(temp_file_path)}"'
        subprocess.run(result_command, shell=True, cwd=current_file_dir)
        time.sleep(1)
    
    # Curățăm fișierele temporare
    os.remove(temp_file_path)
    if os.path.exists(error_log):
        os.remove(error_log)

def pre_input_run(text_widget, right_panel, file_manager, win):
    file_path = file_manager.get_opened_filename()
    if file_path is None:
        win.status_bar.toggle_inbox_icon(f"No files are open.", "red")
        return
    
    if not file_path.endswith(".cpp"):
        win.status_bar.toggle_inbox_icon(f"Only .cpp files can be run.", "red")
        return
    
    code_content = text_widget.toPlainText()
    pre_input = right_panel.input_box.toPlainText().strip()
    if len(pre_input) == 0:
        win.status_bar.toggle_inbox_icon(f"You need to set the pre-input from right panel!", "orange")
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
            right_panel.output_box.setPlainText(f"Compilation failed:\n{compile_errors}")
            return

        run_process = subprocess.Popen(executable_path, 
                                       stdin=subprocess.PIPE, 
                                       stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE, 
                                       text=True)
        output, error = run_process.communicate(input=pre_input)

        if run_process.returncode != 0:
            right_panel.output_box.setPlainText(f"Runtime error:\n{error}")
            return

        right_panel.output_box.setPlainText(output)

        expected_output = right_panel.expected_box.toPlainText().strip()
        passing = True
        if len(expected_output) != 0:
            new_output = right_panel.output_box.toPlainText().strip()
            
            expected_words = expected_output.split()
            new_words = new_output.split()
            
            if len(expected_words) != len(new_words):
                passing = False
                right_panel.output_label.setText("Different number of words")
                right_panel.output_label.setStyleSheet("color: red")
            else:
                for i in range(len(new_words)):
                    if expected_words[i] != new_words[i]:
                        passing = False
                        right_panel.output_label.setText(f"Wrong answer on test case {i + 1}")
                        right_panel.output_label.setStyleSheet("color: red")
                        break

        if passing:
            right_panel.output_label.setText("All test cases passed")
            right_panel.output_label.setStyleSheet("color: green")

    except Exception as e:
        right_panel.output_box.setPlainText(f"Exception occurred:\n{str(e)}")
    
    finally:
        if os.path.exists(cpp_file_path):
            os.remove(cpp_file_path)
        if os.path.exists(executable_path):
            os.remove(executable_path)
