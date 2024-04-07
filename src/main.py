from GUI.gui import *
from GUI.textbox import *
from Config.check import *
import customtkinter as ct
import tkinter as tk

if __name__ == "__main__":
    window = MainWindow()
    config = check_config_file()
    if (config == False):
        create_config_file()
        
    window.mainloop()
