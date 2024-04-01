from GUI.gui import *
from GUI.textbox import *
import customtkinter as ct
import tkinter as tk

if __name__ == "__main__":
    window = MainWindow()
    
    scroll = ScrollText(window)
    scroll.pack(fill="both", expand=True)
    scroll.text.focus()
    window.after(200, scroll.redraw())
    #text = TextBox(main_frame)
    #text.bind("<KeyRelease>", text.update_line_numbers)
    window.mainloop()
