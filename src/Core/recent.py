from tkinter import *
import os

def check_file():
    if not os.path.isfile("recent_dir.txt"):
        with open("recent_dir.txt", "w") as file:
            pass

def write_lines(path):
    
    with open("recent_dir.txt", "r") as file:
        lines = file.readlines()
    lines.insert(0, path+"\n")
    with open("recent_dir.txt", "w") as file:
        file.writelines(lines)

def return_lines():
    check_file()
    with open("recent_dir.txt", "r") as file:
            lines = file.readlines()
    return lines