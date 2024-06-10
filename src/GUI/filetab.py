import customtkinter
import tkinter as tk
from tkinter import messagebox
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from MainMenu import file_menu

class ClosableTab(customtkinter.CTkFrame):
    def __init__(self, master, text, command, close_command, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.command = command
        self.close_command = close_command

        self.inactive_bg_color = "#374ee6"
        self.active_bg_color = "#2c3eb8"

        # Set up the main tab button
        self.tab_button = customtkinter.CTkButton(
            self, text=text, command=self.command, height=35, width=80,
            corner_radius=0, hover_color=self.active_bg_color, fg_color=self.inactive_bg_color,
            font=("", 16)
        )
        self.tab_button.pack(side="left", fill="y")

        # Set up the close button
        self.close_button = customtkinter.CTkButton(
            self, text="✕", command=self.close, height=35, width=20,
            corner_radius=0, hover_color=self.active_bg_color, fg_color=self.inactive_bg_color,
            font=("", 18)
        )
        self.close_button.pack(side="left", fill="y")

        # Add mouse events for dragging
        self.tab_button.bind("<ButtonPress-1>", self.on_start_drag)
        self.tab_button.bind("<B1-Motion>", self.on_drag)
        self.tab_button.bind("<ButtonRelease-1>", self.on_drop)

        self._drag_data = {"x": 0, "item": None}

    def close(self):
        self.close_command(self)

    def activate(self):
        self.tab_button.configure(fg_color=self.active_bg_color)
        self.close_button.configure(fg_color=self.active_bg_color)

    def deactivate(self):
        self.tab_button.configure(fg_color=self.inactive_bg_color)
        self.close_button.configure(fg_color=self.inactive_bg_color)

    def on_start_drag(self, event):
        self._drag_data["item"] = self
        self._drag_data["x"] = event.x_root - self.winfo_x()

    def on_drag(self, event):
        delta_x = (event.x_root - self._drag_data["x"]) / 2
        self.place(x=delta_x, y=0)

    def on_drop(self, event):
        self._drag_data["item"] = None
        self.master.reorder_tabs()


class TabBar(customtkinter.CTkFrame):
    def __init__(self, master, text_widget, scroll, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.text_widget = text_widget
        self.scroll = scroll
        self.tabs = {}
        self.file_contents = {}
        self.current_tab = None

        self.text_widget.bind("<Control-Tab>", self.next_tab)
        self.text_widget.bind("<Control-Shift-Tab>", self.previous_tab)
        self.text_widget.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        # Setați lățimea fixă a frame-ului
        self.configure(height=35, corner_radius=0)
        self.pack_propagate(False)  # Previne modificarea automată a dimensiunilor frame-ului

    def add_tab(self, file_path):
        # Verificați dacă fișierul este deja deschis într-un tab
        if file_path in self.tabs:
            self.show_file_content(file_path)
            return

        # Obțineți doar numele fișierului
        file_name = os.path.basename(file_path)

        def close_command(tab):
            self.close_tab(file_path)

        tab = ClosableTab(
            self, text=file_name, command=lambda: self.show_file_content(file_path),
            close_command=close_command
        )
        tab.pack(side="left", padx=(0, 2))

        self.tabs[file_path] = tab
        self.file_contents[file_path] = file_menu.get_content_of_current_file(file_path)

        # Setează tab-ul nou ca tab activ
        self.show_file_content(file_path)

    def show_file_content(self, file_path):
        if file_path == file_menu.current_file():
            return

        # Deactivate the current tab if there is one
        if self.current_tab and self.current_tab in self.tabs.values():
            self.current_tab.deactivate()

        # Activate the new tab
        self.current_tab = self.tabs[file_path]
        self.current_tab.activate()

        # Verificăm dacă avem deja conținutul fișierului în dicționarul file_contents
        if file_path in self.file_contents:
            content = self.file_contents[file_path]
        else:
            # Dacă nu, citim conținutul fișierului și îl salvăm în dicționar
            with open(file_path, 'r') as file:
                content = file.read()
            self.file_contents[file_path] = content

        ante_path = file_menu.current_file()
        if ante_path:
            self.file_contents[ante_path] = self.text_widget.get("1.0", "end-1c")

        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("1.0", content)
        file_menu.update_file_path(file_path)
        self.scroll.redraw()
        self.text_widget.focus_set()

    def close_tab(self, file_path):
        if file_path in self.tabs:
            # Verifică dacă tabul închis este cel deschis în prezent
            is_current_tab = (file_path == file_menu.current_file())
            # Verifică dacă conținutul din text_widget este diferit de cel salvat
            if file_path in self.file_contents and not is_current_tab:
                current_content = self.file_contents[file_path]
            else:
                current_content = self.text_widget.get("1.0", "end-1c")
            
            file_content = file_menu.get_content_of_current_file(file_path)

            if current_content != file_content:
                response = messagebox.askyesnocancel("Save Changes?", "Do you want to save changes to the file?")
                if response:  # Yes
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(current_content)
                    self.file_contents[file_path] = current_content
                elif response is None:  # Cancel
                    return  # Nu se închide tab-ul

            # Șterge tabul
            self.tabs[file_path].destroy()
            del self.tabs[file_path]
            del self.file_contents[file_path]

            # Actualizează conținutul text_widget doar dacă tabul închis era cel deschis
            if is_current_tab:
                if self.tabs:
                    # Dacă mai sunt alte taburi, deschide primul tab
                    first_file_path = next(iter(self.tabs))
                    self.show_file_content(first_file_path)
                else:
                    # Dacă nu mai sunt alte taburi, golește text_widget
                    self.text_widget.delete("1.0", "end")
                    file_menu.update_file_path("")  # Resetează calea fișierului curent
                    self.current_tab = None
            self.scroll.redraw()

    def delete_tab(self, file_path):
        if file_path in self.tabs:
            # Șterge tabul fără a cere confirmare pentru salvare
            self.tabs[file_path].destroy()
            del self.tabs[file_path]
            del self.file_contents[file_path]

            # Actualizează conținutul text_widget doar dacă tabul închis era cel deschis
            if self.current_tab and self.current_tab == self.tabs.get(file_path):
                if self.tabs:
                    # Dacă mai sunt alte taburi, deschide primul tab
                    first_file_path = next(iter(self.tabs))
                    self.show_file_content(first_file_path)
                else:
                    # Dacă nu mai sunt alte taburi, golește text_widget
                    self.text_widget.delete("1.0", "end")
                    file_menu.update_file_path("")  # Resetează calea fișierului curent
                    self.current_tab = None
            self.scroll.redraw()

    def check_tab(self, file_path):
        return file_path in self.tabs
    
    def next_tab(self, event=None):
        if not self.tabs:
            return
        
        current_index = list(self.tabs.values()).index(self.current_tab)
        next_index = (current_index + 1) % len(self.tabs)
        next_file_path = list(self.tabs.keys())[next_index]
        self.show_file_content(next_file_path)
        self.text_widget.focus_set()

    def previous_tab(self, event=None):
        if not self.tabs:
            return
        
        current_index = list(self.tabs.values()).index(self.current_tab)
        previous_index = (current_index - 1) % len(self.tabs)
        previous_file_path = list(self.tabs.keys())[previous_index]
        self.show_file_content(previous_file_path)
        self.text_widget.focus_set()

    def on_tab_changed(self, event):
        self.text_widget.focus_set()

    def reorder_tabs(self):
        tab_positions = []
        for tab in self.tabs.values():
            tab_positions.append((tab.winfo_x(), tab))

        tab_positions.sort()

        for pos, tab in tab_positions:
            tab.pack_forget()
            tab.pack(side="left", padx=(0, 2))