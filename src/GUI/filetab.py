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

        # Set up the main tab button
        self.tab_button = customtkinter.CTkButton(
            self, text=text, command=self.command, height=30, width=80,
            corner_radius=0, hover_color="#2c3eb8", fg_color="#374ee6"
        )
        self.tab_button.pack(side="left", fill="y")

        # Set up the close button
        self.close_button = customtkinter.CTkButton(
            self, text="x", command=self.close, height=30, width=20,
            corner_radius=0, hover_color="#b82c2c", fg_color="#e63737"
        )
        self.close_button.pack(side="left", fill="y")

    def close(self):
        self.close_command(self)

class TabBar(customtkinter.CTkFrame):
    def __init__(self, master, text_widget, scroll, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.text_widget = text_widget
        self.scroll = scroll
        self.tabs = {}
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

        def close_command(tab):
            self.close_tab(file_path)

        tab = ClosableTab(
            self, text=file_name, command=lambda: self.show_file_content(file_path),
            close_command=close_command
        )
        tab.pack(side="left", padx=(0, 2))

        self.tabs[file_path] = tab
        self.file_contents[file_path] = file_menu.get_content_of_current_file(file_path)

    def show_file_content(self, file_path):
        if file_path == file_menu.current_file():
            return
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
            self.scroll.redraw()
    def check_tab(self, file_path):
        return file_path in self.tabs
