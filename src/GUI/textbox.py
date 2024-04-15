import tkinter as tk
import customtkinter as ct

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
                            selectbackground="#4d4d4d", font=("Arial", font_size),
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
        self.numberLines.redraw()
        self.font_size = check.get_config_value("zoom")
        self.text.configure(font=("Arial", self.font_size))

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
        self.font = ("Arial", self.font_size)
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
