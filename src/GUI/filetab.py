import customtkinter
import tkinter as tk
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from MainMenu import file_menu

class TabBar(customtkinter.CTkFrame):
    def __init__(self, master, text_widget, scroll, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.text_widget = text_widget
        self.scroll = scroll
        self.tabs = {}
        self.buttons = []
        self.file_contents = {}

        # Setați lățimea fixă a frame-ului
        self.configure(height=30, corner_radius=0)
        self.pack_propagate(False)  # Previne modificarea automată a dimensiunilor frame-ului

    def add_tab(self, file_path):
        # Verificați dacă fișierul este deja deschis într-un tab
        if file_path in self.tabs:
            return

        # Obțineți doar numele fișierului
        file_name = os.path.basename(file_path)

        tab_button = customtkinter.CTkButton(
            self, text=file_name, command=lambda: self.show_file_content(file_path), height=30, width=100,
            corner_radius=0, hover_color="#2c3eb8", fg_color="#374ee6"
        )
        tab_button.pack(side="left", padx=(0, 2))

        self.tabs[file_path] = tab_button
        self.buttons.append(tab_button)

    def show_file_content(self, file_path):
        if file_path == file_menu.current_file():
            return
        # Verificăm dacă avem deja conținutul fișierului în dicționarul file_contents
        if file_path in self.file_contents:
            content = self.file_contents[file_path]
            #content = content.rsplit('\n', 1)[0]
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

    def check_tab(self, file_path):
        return file_path in self.tabs
