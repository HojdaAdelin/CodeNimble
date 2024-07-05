from tkinter import *
import customtkinter as ctk
import re

import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from MainMenu import file_menu
from Config import check

def save_session(files):
    folder = file_menu.return_current_path()
    if folder is None:
        folder = "0"

    current_file = file_menu.current_file()
    if current_file is None:
        current_file = "0"

    check.update_config_file("default_file", current_file)
    check.update_config_file("default_folder", folder)
    check.update_config_file("files", files)

def reset_session():
    check.update_config_file("default_file", 0)
    check.update_config_file("default_folder", 0)
    check.update_config_file("files", 0)

def load_file_tab(file_tab):
    if int(check.get_config_value("session")) == 1:
        files = check.get_config_value("files")
        
        pattern = r"'(.*?)': <GUI\.filetab\.ClosableTab object"
        
        paths = re.findall(pattern, files)
        
        for path in paths:
            file_tab.add_tab(path)
    