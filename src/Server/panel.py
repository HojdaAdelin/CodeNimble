from typing import Counter
import customtkinter as ctk
from CTkTable import CTkTable
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
        self.previous_clients = None

        fg_cl, text_bg, text, hover_color = self.theme()
        self.window(fg_cl)
        self.title_color()
        self.gui(text_bg, text,hover_color)

        if self.server:
            self.update_clients()
            self.after(1000, self.update_clients_periodic)

    def gui(self, text_bg, text, hover_color):
        self.table = CTkTable(master=self, row=0, column=2, values=[["Name", "Address"]],
                              font=('Consolas', 20),
                              padx=5, pady=5, 
                              text_color=text,
                              colors=[text_bg, text_bg], 
                              color_phase='vertical', 
                              header_color=text_bg,
                              corner_radius=10,
                              hover_color=hover_color)
        self.table.pack(expand=False, fill="both", padx=20, pady=20)

    def title_color(self):
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

    def window(self, fg_cl):
        self.configure(fg_color=fg_cl)
        self.title("Server Panel")
        self.geometry("1000x600")
        self.iconbitmap("images/logo.ico")
        self.resizable(False, False)

    def theme(self):
        fg_cl = "#2b2b2b"
        text_bg = "#4a4a4a"
        text = "white"
        hover_color="#4d4d4d"
        if int(check.get_config_value("theme")) == 0:
            fg_cl = "#2b2b2b"
            text_bg = "#4a4a4a"
            text = "white"
            hover_color="#4d4d4d"
        elif int(check.get_config_value("theme")) == 1:
            fg_cl = "white"
            text_bg = "#f0f0f0"
            text = "black"
            hover_color="#ebebeb"
        return fg_cl,text_bg,text,hover_color

    def update_clients(self):
        current_clients = list(self.server.clients.values())

        # Verificăm dacă lista curentă de clienți este identică cu cea anterioară
        if self.previous_clients is None or Counter(current_clients) != Counter(self.previous_clients):
            self.previous_clients = current_clients

            # Ștergem toate rândurile, cu excepția antetului
            self.table.delete_rows(range(1, len(self.table.get())))

            # Adăugăm clienții conectați în CTkTable
            for client_socket, client_name in self.server.clients.items():
                self.table.add_row(values=[client_name, "127.0.0.1"])

    def update_clients_periodic(self):
        self.update_clients()
        self.after(1000, self.update_clients_periodic)