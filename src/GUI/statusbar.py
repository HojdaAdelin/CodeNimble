import tkinter as tk

class StatusBar(tk.Frame):
    def __init__(self, master, text="", font_size=28, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.text = tk.StringVar(value=text)
        self.configure(bg="#333333")
        # Specificați dimensiunea fontului utilizând o tuplă cu numele fontului și dimensiunea
        font = ("Arial", font_size)
        
        self.status_label = tk.Label(self, textvariable=self.text, anchor="e", padx=40, font=font, bg="#333333", fg="white")
        self.status_label.pack(side="right", fill="both")
        
        self.pack(side="bottom", fill="x")

    def set_status(self, text):
        self.text.set(text)
    def update_text(self, new_text):
        self.text.set(new_text)