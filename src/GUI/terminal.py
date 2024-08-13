import tkinter as tk
import customtkinter as ct

class Terminal(ct.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.h = 0
        self.configure(height=self.h)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1,weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.textbox = ct.CTkTextbox(self, state='disabled', height=self.h, font=("",18)) 
        #self.textbox.pack(expand=True, fill=tk.BOTH,pady=5, padx=5)
        self.textbox.grid(row=1,column=0,columnspan=2,padx=5,pady=5,sticky="nswe")
        self.clear_button = ct.CTkButton(self,text="Clear", font=("",16),height=20,width=40, corner_radius=0, command=self.clear_terminal)
        self.clear_button.grid(row=0,column=1, padx=5,pady=(5,0),sticky="ne")
        self.notification("Code Nimble - Version 2.0 / 2024")

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

    def clear_terminal(self):
        self.textbox.configure(state='normal')
        self.textbox.delete("1.0", "end")
        self.notification("Code Nimble - Version 2.0 / 2024")