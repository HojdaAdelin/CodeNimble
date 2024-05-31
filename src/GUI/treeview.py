import tkinter as tk
from tkinter import Menu
from tkinter import ttk
import customtkinter
import sys
import os
import shutil
from tkinter import messagebox

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
            font=('Consolas', 28),
            rowheight=45
        )
        self.treestyle.map('Treeview', background=[('selected', self.bg_color)], foreground=[('selected', self.selected_color)])
        
        self.treestyle.configure("Treeview.Heading", font=('Consolas', 28), rowheight=45)
        self.treestyle.map("Treeview", background=[('selected', self.bg_color)], foreground=[('selected', self.selected_color)])
        self.treestyle.configure("Treeview.Dragged", background='#ffcccb')
        self.treestyle.configure("Treeview.Hover", background='#add8e6')
        
        master.bind("<<TreeviewSelect>>", lambda event: master.focus_set())

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.treeview = ttk.Treeview(self, show="tree", height=20, style="Treeview")
        #self.treeview.pack(fill="both", expand=True)
        self.treeview.grid(row=0, column=0, sticky="nsew")
        self.treeview.column("#0", width=600, minwidth=600, stretch=False)
        self.treeview.bind("<Double-1>", self.on_double_click)

        self.menu = tk.Menu(self, tearoff=0, font=("", 30), bg="white", fg="black", activebackground="#ebebeb", activeforeground="black")
        self.menu.add_command(label="Delete File", command=self.delete_selected_file)
        self.menu.add_command(label="Rename File", command=self.rename_selected_file)
        self.menu.add_separator()  
        self.menu.add_command(label="Open in Explorer", command=self.open_in_explorer)

        self.folder_menu = tk.Menu(self, tearoff=0, font=("", 30), bg="white", fg="black", activebackground="#ebebeb", activeforeground="black")
        self.folder_menu.add_command(label="Add File", command=self.add_file) 
        self.folder_menu.add_command(label="Add Folder", command=self.add_folder)
        self.folder_menu.add_separator()
        self.folder_menu.add_command(label="Delete Folder", command=self.delete_selected_folder)
        self.folder_menu.add_command(label="Rename Folder", command=self.rename_folder)
        self.folder_menu.add_separator()
        self.folder_menu.add_command(label="Open in Explorer", command=self.open_in_explorer)

        self.treeview.bind("<Button-3>", self.show_context_menu)
        self.treeview.bind("<ButtonPress-1>", self.on_start_drag)
        self.treeview.bind("<B1-Motion>", self.on_drag)
        self.treeview.bind("<ButtonRelease-1>", self.on_drop)

        #self.input = customtkinter.CTkTextbox(self, height=100, width=600)
        #self.output = customtkinter.CTkTextbox(self, height=100, width=600)

        # Ascunde textboxurile inițial
        #self.input.grid_remove()
        #self.output.grid_remove()
        
        self.drag_data = {"item": None, "x": 0, "y": 0}
        self.hovered_item = None  # Track the currently hovered item

        if root_directory:
            self.populate_treeview(root_directory)

        self.treeview.bind("<<TreeviewOpen>>", self.on_open)

    def delete_selected_folder(self):
        selected_item = self.treeview.selection()
        if selected_item:
            node = selected_item[0]
            abspath = self.get_absolute_path(node)

            if abspath == self.treeview.item(self.treeview.get_children()[0], "text"):
                self.status.update_text("Cannot delete root folder")
                return

            if os.path.isdir(abspath):
                if file_menu.opened_filename and file_menu.opened_filename.startswith(abspath):
                    file_menu.opened_filename = None
                    self.text.delete("1.0", tk.END)
                    self.root.redraw()

                try:
                    shutil.rmtree(abspath)
                    self.treeview.delete(node)
                    self.status.update_text("Deleted folder: " + abspath)
                except OSError as e:
                    self.status.update_text("Error deleting folder: " + str(e))

    def populate_treeview(self, path):
        self.treeview.delete(*self.treeview.get_children())
        abspath = os.path.abspath(path)
        root_node = self.treeview.insert('', 'end', text=abspath, open=True)
        self.process_directory(root_node, abspath)
        
        #if root_node:
            #self.input.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
            #self.output.grid(row=2, column=0, sticky="nsew")

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
            else:
                self.treeview.selection_set(item)
                self.folder_menu.post(event.x_root, event.y_root)

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

    def rename_selected_file(self):
        selected_item = self.treeview.selection()
        if selected_item:
            node = selected_item[0]
            abspath = self.get_absolute_path(node)
            if os.path.isfile(abspath):
                file_menu.rename_file(self.status,self,abspath)


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
        self.grid_forget()

    def on_double_click(self, event):
        item = self.treeview.identify('item', event.x, event.y)
        if item:    
            abspath = self.get_full_path(item)
            if os.path.isfile(abspath):  # Verificăm dacă este un fișier
                if file_menu.opened_file_status():
                    opened_filename_text = file_menu.get_content_of_current_file()
                    current_text = self.text.get("1.0", tk.END)
                    if opened_filename_text.strip() != current_text.strip():
                        raspuns = messagebox.askyesno("Warning", "There are unsaved changes. Do you want to save?")
                        if raspuns:
                            # Apelăm funcția save_file din file_menu.py pentru a salva modificările
                            file_menu.save_file(self.text, self.status)
                            self.text.delete("1.0", tk.END)
                else:
                    current_text = self.text.get("1.0", tk.END)
                    if current_text.strip():
                        raspuns = messagebox.askyesno("Warning", "There are unsaved changes. Do you want to save?")
                        if raspuns:
                            file_menu.save_file(self.text, self.status)
                            self.text.delete("1.0", tk.END)
                self.treeview_open_file(abspath)

    def add_folder(self):
        selected_item = self.treeview.selection()
        if selected_item:
            node = selected_item[0]
            abspath = self.get_absolute_path(node)
            file_menu.add_folder(self.status, self, abspath)

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
            # Add "dragged" tag to the item being dragged
            self.treeview.item(item, tags=("dragged",))
            self.treestyle.configure("Treeview.Item", font=('Consolas', 28), background=self.bg_color)

    def on_drag(self, event):
        '''Handle dragging of an object'''
        target = self.treeview.identify_row(event.y)
        
        # Reset hover effect from all items
        if self.hovered_item:
            self.treeview.item(self.hovered_item, tags=())
            self.hovered_item = None

        if target and target != self.drag_data["item"]:
            # Check if the target item is a folder
            if os.path.isdir(self.get_absolute_path(target)):
                # Add "hover" tag to the target item
                self.treeview.item(target, tags=("hover",))
                self.hovered_item = target

                # Apply the hover effect using the Treeview style
                self.treeview.tag_configure("hover", background="#add8e6")  # Light blue for hover effect

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

            # Reset hover effect from all items
            self.reset_hover_effect()

        # reset drag data
        self.drag_data = {"item": None, "x": 0, "y": 0}

    def reset_hover_effect(self):
        '''Reset hover effect from all items'''
        for item in self.treeview.get_children():
            self.treeview.item(item, tags=())
        self.hovered_item = None

    def get_current_treeview_path(self):
        selected_item = self.treeview.selection()
        if selected_item:
            node = selected_item[0]
            return self.get_absolute_path(node)
        return os.getcwd()  # Returnează directorul de lucru curent dacă nu este selectat niciun element

    def add_file(self):
        selected_item = self.treeview.selection()
        if selected_item:
            node = selected_item[0]
            abspath = self.get_absolute_path(node)
            file_menu.custom_file(self.status, self, abspath)
    
    def rename_folder(self):
        selected_item = self.treeview.selection()
        if selected_item:
            node = selected_item[0]
            abspath = self.get_absolute_path(node)
            file_menu.rename_folder(self.status, self, abspath)
    
    def open_in_explorer(self):
        selected_item = self.treeview.selection()
        if selected_item:
            node = selected_item[0]
            abspath = self.get_absolute_path(node)
            if os.path.isdir(abspath):
                os.startfile(abspath)
            else:
                os.startfile(os.path.dirname(abspath))