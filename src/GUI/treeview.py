import tkinter as tk
from tkinter import Menu
from tkinter import ttk
import customtkinter
import sys
import os
import shutil
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from MainMenu import file_menu

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

class TreeviewFrame(customtkinter.CTkFrame):
    def __init__(self, master, scroll, statusbar, root, root_directory=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.text = scroll.text
        self.scroll = scroll
        self.status = statusbar
        self.root = root
        self.bg_color = self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"])
        self.text_color = self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkLabel"]["text_color"])
        self.selected_color = self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])

        self.gui(master)
        self.drag_data = {"item": None, "x": 0, "y": 0}
        self.hovered_item = None 

        if root_directory:
            self.populate_treeview(root_directory)

        self.treeview.bind("<<TreeviewOpen>>", self.on_open)

    def gui(self, master):
        im_open = Image.new('RGBA', (30, 30), '#00000000')  # Săgeată deschisă mai mare
        im_empty = Image.new('RGBA', (30, 30), '#00000000')  # Imagine goală mai mare
        draw = ImageDraw.Draw(im_open)
        draw.polygon([(0, 10), (28, 10), (14, 28)], fill='#858585', outline='black')
        im_close = im_open.rotate(90)

        self.img_open = ImageTk.PhotoImage(im_open, name='img_open', master=master)
        self.img_close = ImageTk.PhotoImage(im_close, name='img_close', master=master)
        self.img_empty = ImageTk.PhotoImage(im_empty, name='img_empty', master=master)

        self.treestyle = ttk.Style()
        self.treestyle.theme_use('default')

        self.treestyle.element_create('Treeitem.myindicator', 'image', 'img_close', ('user1', '!user2', 'img_open'), ('user2', 'img_empty'), sticky='w', width=30)
        self.treestyle.layout('Treeview.Item', [('Treeitem.padding', {'sticky': 'nswe', 'children': [('Treeitem.myindicator', {'side': 'left', 'sticky': ''}), ('Treeitem.image', {'side': 'left', 'sticky': ''}), ('Treeitem.focus', {'side': 'left', 'sticky': '', 'children': [('Treeitem.text', {'side': 'left', 'sticky': ''})]})]})])

        self.treestyle.configure(
            "Treeview",
            highlightthickness=0,
            borderwidth=0,
            font=('Consolas', 28),
            rowheight=45,
            indent=20
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
        self.treeview.grid(row=0, column=0, sticky="nsew")
        self.treeview.column("#0", width=600, minwidth=600, stretch=False)
        self.treeview.bind("<Double-1>", self.on_double_click)

        self.menu = tk.Menu(self, tearoff=0, font=("", 30), bg="white", fg="black", activebackground="#ebebeb", activeforeground="black")
        self.menu.add_command(label="Delete File", command=self.delete_selected_file)
        self.menu.add_command(label="Rename File", command=self.rename_selected_file)
        self.menu.add_separator()
        self.menu.add_command(label="Open as Input", command=self.open_input)
        self.menu.add_command(label="Open as Output", command=self.open_output)
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

        self.input_label = customtkinter.CTkLabel(self, text="#Input file", font=("", 16))
        self.input = customtkinter.CTkTextbox(self, height=150, width=290)
        self.output_label = customtkinter.CTkLabel(self, text="#Output file", font=("", 16))
        self.output = customtkinter.CTkTextbox(self, height=150, width=290, state="disabled")

    def open_input(self):
        selected_item = self.treeview.selection()
        if selected_item:
            node = selected_item[0]
            abspath = self.get_absolute_path(node)
            if os.path.isfile(abspath):
                file_menu.open_input(self, abspath)

    def open_output(self):
        selected_item = self.treeview.selection()
        if selected_item:
            node = selected_item[0]
            abspath = self.get_absolute_path(node)
            if os.path.isfile(abspath):
                file_menu.open_output(self, abspath)

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
                if self.scroll.tab_bar.check_tab(abspath):
                    self.scroll.tab_bar.delete_tab(abspath)

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
            if os.path.isfile(abspath):
                if self.scroll.tab_bar.check_tab(abspath):
                    return
                self.scroll.tab_bar.add_tab(abspath)
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
        item = self.treeview.identify_row(event.y)
        if item:
            self.drag_data["item"] = item
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
            self.treeview.item(item, tags=("dragged",))
            self.treestyle.configure("Treeview.Item", font=('Consolas', 28), background=self.bg_color)

    def on_drag(self, event):
        target = self.treeview.identify_row(event.y)
        
        if self.hovered_item:
            self.treeview.item(self.hovered_item, tags=())
            self.hovered_item = None

        if target and target != self.drag_data["item"]:
            if os.path.isdir(self.get_absolute_path(target)):
                self.treeview.item(target, tags=("hover",))
                self.hovered_item = target

                self.treeview.tag_configure("hover", background="#add8e6")  # Light blue for hover effect

    def on_drop(self, event):
        item = self.drag_data["item"]
        if item:
            target = self.treeview.identify_row(event.y)
            if target and target != item:
                abspath_source = self.get_absolute_path(item)
                abspath_target = self.get_absolute_path(target)

                if os.path.isdir(abspath_target):
                    new_path = os.path.join(abspath_target, os.path.basename(abspath_source))
                    try:
                        shutil.move(abspath_source, new_path)
                        self.treeview.delete(item)
                        
                        self.treeview.delete(*self.treeview.get_children(target))
                        self.process_directory(target, abspath_target)

                        if file_menu.opened_filename.startswith(abspath_source):
                            new_opened_filename = file_menu.opened_filename.replace(abspath_source, new_path, 1)
                            file_menu.update_file_path(new_opened_filename)

                    except Exception as e:
                        pass

            self.reset_hover_effect()

        self.drag_data = {"item": None, "x": 0, "y": 0}

    def reset_hover_effect(self):
        for item in self.treeview.get_children():
            self.treeview.item(item, tags=())
        self.hovered_item = None

    def get_current_treeview_path(self):
        selected_item = self.treeview.selection()
        if selected_item:
            node = selected_item[0]
            return self.get_absolute_path(node)
        return os.getcwd() 

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

    def clear_treeview(self):
        self.treeview.delete(*self.treeview.get_children())