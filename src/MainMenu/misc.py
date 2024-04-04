import tkinter as tk
import customtkinter as ctk
import webbrowser

def exit_application(root):
    root.quit() 

def version_info():
    # Creează o nouă fereastră
    version_window = ctk.CTkToplevel()
    version_window.title("CodeNimble - Version")

    w = 300 
    h = 200 

    ws = version_window.winfo_screenwidth()
    hs = version_window.winfo_screenheight()

    x = (ws/2+500) - (w/2)
    y = (hs/2+200) - (h/2)

    version_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    #version_window.geometry('300x200')
    
    version_window.resizable(False, False)
    version_window.configure(fg_color = "#2b2b2b")
    
    version_label = ctk.CTkLabel(version_window, text="Version: BETA 1.0", font=("Arial", 20), text_color="white")
    version_label.pack(pady=80)

def changelog_inf():
    changelog_window = ctk.CTkToplevel()
    changelog_window.title("CodeNimble - Change log")

    w = 500 
    h = 400 

    ws = changelog_window.winfo_screenwidth()
    hs = changelog_window.winfo_screenheight()

    x = (ws/2+500) - (w/2)
    y = (hs/2+200) - (h/2)

    changelog_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    #version_window.geometry('300x200')
    
    changelog_window.resizable(False, False)
    changelog_window.configure(fg_color = "#2b2b2b")

    version_label = ctk.CTkLabel(changelog_window, text="Version: BETA 1.0", font=("Arial", 20), text_color="white")
    version_label.pack(pady=10)

def open_links(url):
    webbrowser.open(url)