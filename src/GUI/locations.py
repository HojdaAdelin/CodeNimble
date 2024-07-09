import tkinter as tk
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Config import check
from MainMenu import themes

class RecentDrop:
    def __init__(self, master, lista_elemente):
        self.master = master
        self.lista_elemente = lista_elemente
        self.visible = False
        
        self.frame = tk.Frame(self.master, width=750, height=460, bd=1, relief='solid')
        self.listbox = tk.Listbox(self.frame, selectmode=tk.SINGLE, height=len(self.lista_elemente),
                                  font=("", 34))
        for item in self.lista_elemente:
            self.listbox.insert(tk.END, item)
        
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.frame.pack_propagate(False)
        
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.frame.bind("<FocusOut>", self.hide_dropdown)
        self.master.bind("<Escape>", self.hide_dropdown)
        self.master.bind("<Button-1>", self.check_click_outside)

        fg_color, text_bg, text, hover_color = themes.return_default_win_color(check.get_config_value("theme"))
        self.listbox.configure(bg=fg_color, fg=text)
    
    def toggle_visibility(self):
        if self.visible:
            self.hide_dropdown(None)
        else:
            self.frame.lift()
            self.visible = True
    
    def hide_dropdown(self, event):
        self.frame.lower()
        self.visible = False
    
    def check_click_outside(self, event):
        if not (self.frame.winfo_containing(event.x_root, event.y_root) == self.frame or self.frame.winfo_toplevel() == event.widget):
            self.hide_dropdown(None)