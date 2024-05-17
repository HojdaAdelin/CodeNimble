import subprocess
import os

import sys

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from MainMenu import file_menu

def run_cpp_file():
    file_path = file_menu.current_file()
    if not file_path.endswith(".cpp"):
        print("Doar fișierele .cpp pot fi rulate.")
        return
    
    # Compilarea fișierului .cpp
    executable_name = file_path.replace(".cpp", ".exe")
    compile_command = f"g++ {file_path} -o {executable_name}"
    
    # Rularea comenzii de compilare
    compile_process = subprocess.run(compile_command, shell=True)
    
    if compile_process.returncode != 0:
        return
    
    # Rularea fișierului executabil în cmd
    run_command = f"start cmd /k {executable_name}"
    subprocess.run(run_command, shell=True)