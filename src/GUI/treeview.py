import tkinter as tk
from tkinter import Menu
from tkinter import ttk
import customtkinter
import sys
import os
import shutil

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from MainMenu import file_menu

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

class TreeviewFrame(customtkinter.CTkFrame):
    def __init__(self, master, text, statusbar, root, root_directory=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.text = text
        self.status = statusbar
        self.root = root
        self.bg_color = self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"])
        self.text_color = self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkLabel"]["text_color"])
        self.selected_color = self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])

        self.treestyle = ttk.Style()
        self.treestyle.theme_use('default')
        self.treestyle.configure(
            "Treeview",
            highlightthickness=0,
            borderwidth=0,
            font=('Consolas', 24),
            rowheight=35
        )
        self.treestyle.map('Treeview', background=[('selected', self.bg_color)], foreground=[('selected', self.selected_color)])
        master.bind("<<TreeviewSelect>>", lambda event: master.focus_set())

        self.treeview = ttk.Treeview(self, show="tree", height=20, style="Treeview")
        self.treeview.pack(fill="both", expand=True)
        self.treeview.column("#0", width=550, stretch=tk.YES)
        self.treeview.bind("<Double-1>", self.on_double_click)

        self.menu = tk.Menu(self, tearoff=0, font=("", 20), bg="white", fg="black", activebackground="#ebebeb", activeforeground="black")
        self.menu.add_command(label="Delete File", command=self.delete_selected_file)

        self.treeview.bind("<Button-3>", self.show_context_menu)
        self.treeview.bind("<ButtonPress-1>", self.on_start_drag)
        self.treeview.bind("<B1-Motion>", self.on_drag)
        self.treeview.bind("<ButtonRelease-1>", self.on_drop)

        self.drag_data = {"item": None, "x": 0, "y": 0}

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

    def show_context_menu(self, event):
        item = self.treeview.identify_row(event.y)
        if item:
            abspath = self.get_absolute_path(item)
            if os.path.isfile(abspath):
                self.treeview.selection_set(item)
                self.menu.post(event.x_root, event.y_root)

    def get_absolute_path(self, node):
        parent_path = self.get_parent_path(node)
        return os.path.join(parent_path, self.treeview.item(node, "text"))

    def delete_selected_file(self):
        selected_item = self.treeview.selection()
        if selected_item:
            node = selected_item[0]
            abspath = self.get_absolute_path(node)
            if os.path.isfile(abspath):
                file_menu.delete_file(abspath, self.status, self.text, self.root)
                self.treeview.delete(node)
                self.text.delete("1.0", tk.END)
                self.root.redraw()

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

    def on_start_drag(self, event):
        '''Begining drag of an object'''
        # record the item and its location
        item = self.treeview.identify_row(event.y)
        if item:
            self.drag_data["item"] = item
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def on_drag(self, event):
        '''Handle dragging of an object'''
        pass  # No need to do anything here

    def on_drop(self, event):
        '''End drag of an object'''
        # get the item being dragged
        item = self.drag_data["item"]
        if item:
            # get the target item
            target = self.treeview.identify_row(event.y)
            if target and target != item:
                abspath_source = self.get_absolute_path(item)
                abspath_target = self.get_absolute_path(target)

                # check if target is a directory
                if os.path.isdir(abspath_target):
                    new_path = os.path.join(abspath_target, os.path.basename(abspath_source))
                    try:
                        shutil.move(abspath_source, new_path)
                        self.treeview.delete(item)
                        
                        # Remove duplicates by clearing and re-populating target directory
                        self.treeview.delete(*self.treeview.get_children(target))
                        self.process_directory(target, abspath_target)

                        # Check if the opened file is inside the moved directory and update its path
                        if file_menu.opened_filename.startswith(abspath_source):
                            new_opened_filename = file_menu.opened_filename.replace(abspath_source, new_path, 1)
                            file_menu.update_file_path(new_opened_filename)

                    except Exception as e:
                        pass

        # reset drag data
        self.drag_data = {"item": None, "x": 0, "y": 0}
