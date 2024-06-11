import tkinter as tk
import os

def check_config_file():
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, "config.cfg")
    if os.path.exists(file_path):
        return True
    else:
        return False
    
def create_config_file():
    try:
        with open("config.cfg", "x") as file:
            pass
    except FileExistsError:
        pass

def pre_write_config():
    try:
        with open("config.cfg", "w") as file:
            file.write("zoom: 28\ntheme: 0\nstatus: 1\ndefault_file: 0\ndefault_folder: 0")
    except Exception as e:
        pass

def update_config_file(func, val):
    file_name = "config.cfg"
    try:
        with open(file_name, "r") as file:
            lines = file.readlines()

        with open(file_name, "w") as file:
            for line in lines:
                if line.startswith(func + ":"):
                    file.write(f"{func}: {val}\n")
                else:
                    file.write(line)
        
    except Exception as e:
        pass

def get_config_value(func):
    file_name = "config.cfg"
    try:
        with open(file_name, "r") as file:
            for line in file:
                if line.startswith(func + ":"):
                    value = line.split(":", 1)[1].strip()
                    return value
        
    except Exception as e:
        pass