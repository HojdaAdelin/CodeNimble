import tkinter as tk

import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Config import check

def zoom_in(root):
    ante_size = check.get_config_value("zoom")
    if (int(ante_size) + 4 < 40):
        check.update_config_file("zoom", int(ante_size) + 4)
    root.redraw()

def zoom_out(root):
    ante_size = check.get_config_value("zoom")
    if (int(ante_size) - 4 > 20):
        check.update_config_file("zoom", int(ante_size) - 4)
    
    root.redraw()


