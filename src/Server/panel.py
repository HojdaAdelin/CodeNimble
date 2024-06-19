import customtkinter as ctk
import tkinter as tk
from CTkTable import CTkTable
from tkinter import ttk
from ctypes import byref, sizeof, c_int, windll
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Config import check

class ServerPanel(ctk.CTk):
    def __init__(self, server_instance=None):
        super().__init__()

        self.server = server_instance

        # Definim culorile bazate pe tema
        fg_cl = "#2b2b2b"
        text_bg = "#4a4a4a"
        text = "white"
        if int(check.get_config_value("theme")) == 0:
            fg_cl = "#2b2b2b"
            text_bg = "#4a4a4a"
            text = "white"
        elif int(check.get_config_value("theme")) == 1:
            fg_cl = "white"
            text_bg = "#f0f0f0"
            text = "black"

        self.configure(fg_color=fg_cl)
        self.title("Server Panel")
        self.geometry("1000x600")
        self.iconbitmap("images/logo.ico")
        self.resizable(False, False)

        tb_color = 0x333333
        if int(check.get_config_value("theme")) == 0:
            tb_color = 0x333333
        elif int(check.get_config_value("theme")) == 1:
            tb_color = 0xFFFFFF
        else:
            tb_color = 0x333333

        HWND = windll.user32.GetParent(self.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(
            HWND,
            35,
            byref(c_int(tb_color)),
            sizeof(c_int))

        # Creăm un CTkTable pentru a afișa clienții conectați
        self.table = CTkTable(master=self, row=0, column=2, padx=10, pady=10,
                              font=('Consolas', 14), wraplength=150, justify=tk.CENTER)
        self.table.grid(row=0, column=0, sticky="nsew")

        self.table.insert(0, 0, "Name")
        self.table.insert(0, 1, "Address")

        if self.server:
            # Încărcăm clienții deja conectați
            self.update_clients()

            # Pornim un thread pentru a actualiza periodic lista de clienți
            self.after(1000, self.update_clients_periodic)

    def update_clients(self):
        # Șterge toate intrările existente
        self.table.delete(rows=range(1, self.table.row_count))

        # Adaugă clienții conectați în CTkTable
        row_index = 1
        for client_socket, client_name in self.server.clients.items():
            self.table.insert(row_index, 0, client_name)
            self.table.insert(row_index, 1, "127.0.0.1")  # Adaugă adresa IP corespunzătoare
            row_index += 1

    def update_clients_periodic(self):
        self.update_clients()
        self.after(1000, self.update_clients_periodic)