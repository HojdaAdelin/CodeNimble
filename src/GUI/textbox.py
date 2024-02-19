import customtkinter as ct
import tkinter as tk

class TextBox(ct.CTkTextbox):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.vertical_scrollbar = ct.CTkScrollbar(master, command=self.multi_scroll)
        self.vertical_scrollbar.pack(side="right", fill="y")
        self.pack(side="right", fill="both", expand=True)
        self.configure(fg_color="#222222", wrap='none', font=("Helvetica", 18))
        self.linenumbers = TextLineNumbers(master, width=50, height=self.cget("height"))
        self.linenumbers.configure(fg_color="#333333", font=("Helvetica", 18), corner_radius=0, pady=5)
        self.linenumbers.attach(self)
        self.linenumbers._scrollbars_activated = False
        self._scrollbars_activated = False
        self.linenumbers.pack(side="left", fill="y")
        self.configure(yscrollcommand=self.vertical_scrollbar.set)
        self.linenumbers.configure(yscrollcommand=self.vertical_scrollbar.set)
    def update_line_numbers(self, *args):
        self.linenumbers.redraw()
    def multi_scroll(self, *args):
        self.yview(*args)
        self.linenumbers.yview(*args)
class TextLineNumbers(ct.CTkTextbox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textwidget = None
        self.configure(state="disabled")  # Configurăm textul ca fiind dezactivat pentru a fi doar pentru vizualizare

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        self.configure(state="normal")  # Activăm textul pentru a putea fi modificat
        self.delete("1.0", "end")

        # Obținem dimensiunea maximă a unui număr de linie
        max_linenum_width = len(str(self.textwidget.index("end").split(".")[0]))

        i = self.textwidget.index("@0,0")
        line_count = int(self.textwidget.index("end-1c").split('.')[0])
        for linenum in range(1, line_count + 1):
            self.insert("end", str(linenum).rjust(max_linenum_width) + "\n")  # Aliniem la dreapta numărul de linie
            self.tag_add("right", f"{linenum}.0", f"{linenum}.end")  # Adăugăm tagul pentru aliniere la dreapta
            self.tag_config("right", justify="right")  # Configurăm tagul pentru aliniere la dreapta
        self.configure(state="disabled")  # Redăm textul inactiv pentru a-l face doar pentru vizualizare
