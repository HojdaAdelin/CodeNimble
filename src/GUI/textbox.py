import customtkinter as ct
import tkinter as tk

class TextBox(ct.CTkTextbox):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.pack(side="right", fill="both", expand=True)
        self.configure(fg_color="#222222", wrap='none', font=("Helvetica", 20))
        self.linenumbers = TextLineNumbers(master, width=110)
        self.linenumbers.configure(bg="#222222")
        self.linenumbers.attach(self)
        self.linenumbers.pack(side="left", fill="y")

    def update_line_numbers(self, *args):
        self.linenumbers.redraw()

class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs, highlightthickness=0)
        self.textwidget = None
        self.font = kwargs.get("font", ("Helvetica", 28))  # Fontul implicit

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        self.delete("all")
        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split('.')[0]
            x = self.winfo_width() - 2  # Calculați coordonata x folosind lățimea canvas-ului
            self.create_text(x, y, anchor="ne", text=linenum, fill="#888888", font=self.font)  # Specificați fontul aici
            i = self.textwidget.index("%s+1line" % i)
    