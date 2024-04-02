import tkinter as tk
import customtkinter as ctk

def exit_application(root):
    root.quit() 

def version_info():
    # Creează o nouă fereastră
    version_window = ctk.CTkToplevel()
    version_window.title("CodeNimble - Version")

    w = 300 # width for the Tk root
    h = 200 # height for the Tk root

    # get screen width and height
    ws = version_window.winfo_screenwidth() # width of the screen
    hs = version_window.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2+500) - (w/2)
    y = (hs/2+200) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed
    version_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    #version_window.geometry('300x200')
    
    version_window.resizable(False, False)
    version_window.configure(fg_color = "#2b2b2b")
    # Adaugă un Label cu textul versiunii
    version_label = ctk.CTkLabel(version_window, text="Version: BETA 1.0", font=("Arial", 20), text_color="white")
    version_label.pack(pady=80)

