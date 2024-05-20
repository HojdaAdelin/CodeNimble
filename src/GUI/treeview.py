import tkinter as tk
from tkinter import ttk
import customtkinter
import os

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

class TreeviewFrame(customtkinter.CTkFrame):
    def __init__(self, master, root_directory, *args, **kwargs):
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
            font=('Consolas', 20),  # Set the font and size to 20
            rowheight=30  # Set the row height to avoid text overlap
        )
        self.treestyle.map('Treeview', background=[('selected', self.bg_color)], foreground=[('selected', self.selected_color)])
        master.bind("<<TreeviewSelect>>", lambda event: master.focus_set())

        # Create Treeview with just the tree column
        self.treeview = ttk.Treeview(self, show="tree", height=20, style="Treeview")
        self.treeview.pack(fill="both", expand=True)

        # Configure the column width
        self.treeview.column("#0", width=500, stretch=tk.YES)  # "#0" refers to the tree column

        self.populate_treeview(root_directory)

        # Bind the event for opening a tree node
        self.treeview.bind("<<TreeviewOpen>>", self.on_open)

    def populate_treeview(self, path):
        # Clear all items in the treeview before populating it with new items
        self.treeview.delete(*self.treeview.get_children())

        abspath = os.path.abspath(path)
        root_node = self.treeview.insert('', 'end', text=abspath, open=True)  # No values
        self.process_directory(root_node, abspath)

    def process_directory(self, parent, path):
        try:
            for item in os.listdir(path):
                abspath = os.path.join(path, item)
                isdir = os.path.isdir(abspath)
                node = self.treeview.insert(parent, 'end', text=item, open=False)  # No values
                if isdir:
                    self.treeview.insert(node, 'end')  # Add a dummy child to make the node expandable
        except PermissionError:
            pass

    def on_open(self, event):
        node = self.treeview.focus()
        parent_path = self.get_parent_path(node)
        abspath = os.path.join(parent_path, self.treeview.item(node, "text"))

        # Clear the existing children of the node
        children = self.treeview.get_children(node)
        if children:
            self.treeview.delete(*children)

        # Populate the node with actual content
        self.process_directory(node, abspath)


    def get_parent_path(self, node):
        parent_node = self.treeview.parent(node)
        if parent_node:
            parent_path = self.get_parent_path(parent_node)
            return os.path.join(parent_path, self.treeview.item(parent_node, "text"))
        else:
            return self.treeview.item(node, "text")
