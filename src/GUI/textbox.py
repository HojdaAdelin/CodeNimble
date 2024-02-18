import customtkinter as ct
import tkinter as tk

class TextBox(ct.CTkTextbox):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.pack(side="right", fill="both", expand=True)
        self.configure(fg_color="#222222", wrap='none', font=("Helvetica", 18))
        self.linenumbers = TextLineNumbers(master, width=5, height=self.cget("height"))
        self.linenumbers.configure(background="#333333", foreground="white", font=("Helvetica", 28))
        self.linenumbers.attach(self)
        self.linenumbers.pack(side="left", fill="y")
    def update_line_numbers(self, *args):
        self.linenumbers.redraw()

class TextLineNumbers(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textwidget = None
        self.config(state="disabled", pady=10)  # Adăugăm un padding în partea de sus

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        self.config(state="normal")  # Activăm textul pentru a putea fi modificat
        self.delete("1.0", "end")
        i = self.textwidget.index("@0,0")
        line_count = int(self.textwidget.index("end-1c").split('.')[0])
        for linenum in range(1, line_count + 1):
            self.insert("end", str(linenum) + "\n")
        self.config(state="disabled")  # Redăm textul inactiv pentru a-l face doar pentru vizualizare
        self.tag_add("right", "1.0", "end")  # Adăugăm un tag pentru a alinia textul la dreapta
        self.tag_config("right", justify="right")  # Configurăm tagul pentru aliniere la dreapta
