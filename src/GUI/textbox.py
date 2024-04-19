import tkinter as tk
import customtkinter as ct
import re
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Config import check

#font_size = check.get_config_value("zoom")

class ScrollText(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        
        font_size = check.get_config_value("zoom")

        if font_size is None:
            font_size = 28

        self.text = tk.Text(self, bg='#2b2b2b', foreground="#d1dce8", 
                            insertbackground='white',
                            selectbackground="#4d4d4d", font=("Consolas", font_size),
                            undo=True, maxundo=-1, autoseparators=True, borderwidth=0, wrap="none")
        self.configure(bg="#2b2b2b")
        self.scrollbar = ct.CTkScrollbar(self.text, orientation=tk.VERTICAL, command=self.text.yview)
        self.scrollhor = ct.CTkScrollbar(self.text, orientation=tk.HORIZONTAL, command=self.text.xview)
        self.text.configure(yscrollcommand=self.scrollbar.set, xscrollcommand=self.scrollhor.set)

        self.numberLines = TextLineNumbers(self, width=4*int(check.get_config_value("zoom")), bg='#313335')
        self.numberLines.attach(self.text)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollhor.pack(side=tk.BOTTOM, fill=tk.X)
        self.numberLines.pack(side=tk.LEFT, fill=tk.Y)
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.text.bind("<Key>", self.onPressDelay)
        self.text.bind("<Button-1>", self.numberLines.redraw)
        self.scrollbar.bind("<Button-1>", self.onScrollPress)
        self.text.bind("<MouseWheel>", self.onPressDelay)
        self.text.bind("<KeyRelease>", lambda event: self.highlight_syntax())

    def onScrollPress(self, *args):
        self.scrollbar.bind("<B1-Motion>", self.numberLines.redraw)

    def onScrollRelease(self, *args):
        self.scrollbar.unbind("<B1-Motion>", self.numberLines.redraw)

    def onPressDelay(self, *args):
        self.after(2, self.numberLines.redraw)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.text.index(*args, **kwargs)

    def redraw(self):
        self.highlight_syntax()
        self.numberLines.redraw()
        self.font_size = check.get_config_value("zoom")
        self.text.configure(font=("Consolas", self.font_size))
    def highlight_syntax(self):
        # Definirea culorilor pentru evidențierea sintaxei
        
        keyword_colors = {
            "keyword1": "#0e72b5",
            "keyword2": "#573e9c",
            "keyword3": "#d1dce8",
            "keyword4": "#d1dce8",
            "keyword5": "#2d5f9c",  # Culorea pentru primul grup de cuvinte cheie
            "keyword6": "#cc6600",  # Culorea pentru al doilea grup de cuvinte cheie
            "keyword7": "#8f5c14",
            "keyword8": "#7cafcf",
            "keyword9": "#3f8a16",
            "comment_line": "#008000",  # Verde pentru comentarii de linie
            "comment_block": "#008000",  # Verde pentru comentarii de bloc
            "string": "#008000",
            "quote": "#008000",
            "include": "#008000"  # culoarea pentru "#"
        }

        # Șterge toate tag-urile pentru a evita păstrarea evidențierii sintaxei pentru textul modificat
        for tag in self.text.tag_names():
            self.text.tag_remove(tag, "1.0", tk.END)

        # Definește tag-uri pentru fiecare grup de cuvinte cheie și pentru comentarii
        for keyword_group, color in keyword_colors.items():
            self.text.tag_configure(keyword_group, foreground=color)

        # Lista de cuvinte cheie pentru fiecare grup
        keywords = {
            "keyword1": ["{", "}", "\\[", "\\]", "\\(", "\\)"],
            "keyword2": ["\\<", "\\>", "\\=", "\\%", "\\+", "\\-", "\\*"],
            "keyword3": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
                        "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", ";"],
            "keyword4": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
            "keyword5": ["int", "float", "double", "char", "if", "else", "for", "while", "return", "do", "string", "const", "using"],
            "keyword6": ["struct", "class", "public", "private", "protected"],
            "keyword7": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
            "keyword8": ["void"],
            "keyword9": [re.escape("\""), re.escape("//"), re.escape("/*"), re.escape("*/"), re.escape("\'")],
            
        }

        # Parcurge fiecare grup de cuvinte cheie și caută-le în text
        for keyword_group, keyword_list in keywords.items():
            for keyword in keyword_list:
                start_index = "1.0"
                while True:
                    start_index = self.text.search(keyword, start_index, tk.END, regexp=True)
                    if not start_index:
                        break
                    end_index = self.text.index(f"{start_index}+{len(keyword)}c")
                    self.text.tag_add(keyword_group, start_index, end_index)
                    start_index = end_index

        # Evidențiază comentariile de linie
        self.highlight_line_comments()

        # Evidențiază comentariile de bloc
        self.highlight_block_comments()

        self.highlight_strings()

        self.highlight_quotes()

        self.highlight_include()

    def highlight_include(self):
        # Identifică caracterul "#" și evidențiază textul după el în altă culoare
        start_index = "1.0"
        while True:
            start_index = self.text.search("#", start_index, tk.END, regexp=True)
            if not start_index:
                break
            end_index = self.text.index(f"{start_index} lineend")
            self.text.tag_add("include", start_index, end_index)
            start_index = end_index



    def highlight_line_comments(self):
        # Identifică comentariile de linie și evidențiază întreaga linie în verde
        start_index = "1.0"
        while True:
            start_index = self.text.search("//", start_index, tk.END, regexp=True)
            if not start_index:
                break
            end_index = self.text.index(f"{start_index} lineend")
            self.text.tag_add("comment_line", start_index, end_index)
            start_index = end_index


    def highlight_block_comments(self):
        # Identifică comentariile de bloc și evidențiază întregul bloc în verde
        start_index = "1.0"
        while True:
            start_index = self.text.search("/\\*", start_index, tk.END, regexp=True)
            if not start_index:
                break
            end_index = self.text.search("\\*/", start_index, tk.END, regexp=True)
            if not end_index:
                break
            end_index = self.text.index(f"{end_index}+2c")
            self.text.tag_add("comment_block", start_index, end_index)
            start_index = end_index

    def highlight_strings(self):
        # Identifică textul între ghilimele și evidențiază-l în altă culoare
        start_index = "1.0"
        while True:
            start_index = self.text.search("\"", start_index, tk.END, regexp=True)
            if not start_index:
                break
            end_index = self.text.search("\"", f"{start_index}+1c", tk.END, regexp=True)
            if not end_index:
                break
            end_index = self.text.index(f"{end_index}+1c")
            self.text.tag_add("string", start_index, end_index)
            start_index = end_index

    def highlight_quotes(self):
        # Identifică textul între ghilimele simple și evidențiază-l în altă culoare
        start_index = "1.0"
        while True:
            start_index = self.text.search("'", start_index, tk.END, regexp=True)
            if not start_index:
                break
            end_index = self.text.search("'", f"{start_index}+1c", tk.END, regexp=True)
            if not end_index:
                break
            end_index = self.text.index(f"{end_index}+1c")
            self.text.tag_add("quote", start_index, end_index)
            start_index = end_index


class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs, highlightthickness=0)
        self.textwidget = None
        self.font_size = check.get_config_value("zoom")

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        self.delete("all")
        self.font_size = check.get_config_value("zoom")
        self.font = ("Consolas", self.font_size)
        self.configure(width=4 * int(self.font_size))   # Redefinește lățimea liniei pe baza dimensiunii fontului
        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            # Creează textul pentru numărul de linie și aplică configurația de font
            self.create_text(2, y, anchor="nw", text=linenum, fill="#606366", font=self.font)
            i = self.textwidget.index("%s+1line" % i)