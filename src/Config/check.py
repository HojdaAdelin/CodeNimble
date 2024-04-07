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