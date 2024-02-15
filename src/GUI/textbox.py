import customtkinter as ct

class TextBox(ct.CTkTextbox):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.configure(fg_color="#222222", wrap='none', font=("Helvetica", 20))