import tkinter as tk
from tkinter import ttk
import customtkinter
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from MainMenu import file_menu

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

class TreeviewFrame(customtkinter.CTkFrame):
    def __init__(self, master, text, statusbar,root, root_directory=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.text=text
        self.status = statusbar
        self.root=root
        self.bg_color = self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"])
        self.text_color = self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkLabel"]["text_color"])
        self.selected_color = self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])

        self.treestyle = ttk.Style()
        self.treestyle.theme_use('default')
        self.treestyle.configure(
            "Treeview",
            highlightthickness=0,
            borderwidth=0,
            font=('Consolas', 20),
            rowheight=30
        )
        self.treestyle.map('Treeview', background=[('selected', self.bg_color)], foreground=[('selected', self.selected_color)])
        master.bind("<<TreeviewSelect>>", lambda event: master.focus_set())

        self.treeview = ttk.Treeview(self, show="tree", height=20, style="Treeview")
        self.treeview.pack(fill="both", expand=True)
        self.treeview.column("#0", width=500, stretch=tk.YES)
        self.treeview.bind("<Double-1>", self.on_double_click)

        if root_directory:
            self.populate_treeview(root_directory)

        self.treeview.bind("<<TreeviewOpen>>", self.on_open)

    def populate_treeview(self, path):
        self.treeview.delete(*self.treeview.get_children())
        abspath = os.path.abspath(path)
        root_node = self.treeview.insert('', 'end', text=abspath, open=True)
        self.process_directory(root_node, abspath)

    def process_directory(self, parent, path):
        try:
            for item in os.listdir(path):
                abspath = os.path.join(path, item)
                isdir = os.path.isdir(abspath)
                node = self.treeview.insert(parent, 'end', text=item, open=False)
                if isdir:
                    self.treeview.insert(node, 'end')
        except PermissionError:
            pass

    def on_open(self, event):
        node = self.treeview.focus()
        parent_path = self.get_parent_path(node)
        abspath = os.path.join(parent_path, self.treeview.item(node, "text"))
        children = self.treeview.get_children(node)
        if children:
            self.treeview.delete(*children)
        self.process_directory(node, abspath)

    def get_parent_path(self, node):
        parent_node = self.treeview.parent(node)
        if parent_node:
            parent_path = self.get_parent_path(parent_node)
            return os.path.join(parent_path, self.treeview.item(parent_node, "text"))
        else:
            return self.treeview.item(node, "text")
    
    def reload_treeview(self, path=None):
        if path is None:
            path = os.getcwd()  
        self.populate_treeview(path)

    def hide(self):
        self.pack_forget()

    def on_double_click(self, event):
        item = self.treeview.identify('item', event.x, event.y)
        if item:
            abspath = self.get_full_path(item)
            if os.path.isfile(abspath):  # Verificăm dacă este un fișier
                self.treeview_open_file(abspath)

    def get_full_path(self, node):
        parent_node = self.treeview.parent(node)
        parts = []
        while parent_node:
            parts.append(self.treeview.item(node, "text"))
            node = parent_node
            parent_node = self.treeview.parent(node)
        parts.append(self.treeview.item(node, "text"))
        parts.reverse()
        return os.path.join(*parts)

    def treeview_open_file(self, path):
        file_menu.open_file_by_path(self.text, self.status, path)
        self.root.redraw()