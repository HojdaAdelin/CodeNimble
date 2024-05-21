import tkinter as tk
from tkinter import ttk
import customtkinter
import os

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

class TreeviewFrame(customtkinter.CTkFrame):
    def __init__(self, master, root_directory=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
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
