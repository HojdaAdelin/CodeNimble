import tkinter as tk
import customtkinter as ct

class Terminal(ct.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.h = 0
        self.configure(height=self.h)

        self.textbox = ct.CTkTextbox(self, state='disabled', height=self.h, font=("",18)) 
        self.textbox.pack(expand=True, fill=tk.BOTH,pady=5, padx=5)

    def return_height(self):
        return self.h
    
    def update_height(self, val):
        self.h = val
        self.configure(height=self.h)
        self.textbox.configure(height=self.h)

    def notification(self, message):
        self.textbox.configure(state='normal')
        self.textbox.insert(tk.END, message + "\n")  
        self.textbox.configure(state='disabled')