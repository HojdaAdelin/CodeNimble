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
from MainMenu import themes

class ServerPanel(ctk.CTk):
    def __init__(self,main, server_instance=None):
        super().__init__()

        self.server = server_instance
        self.previous_clients = None
        self.main = main

        fg_cl, text_bg, text, hover_color, self.button_color, self.button_hover_color, self.button_text_color = themes.return_default_win_color(check.get_config_value("theme"))
        self.window(fg_cl)
        self.title_color()
        self.gui(text_bg, text,hover_color)

        if self.server:
            self.update_clients()
            self.after(1000, self.update_clients_periodic)

    def gui(self, text_bg, text, hover_color):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.start_server = ctk.CTkButton(self, text="Start Server", font=('Consolas', 24),command=self.start_server, fg_color=self.button_color, hover_color=self.button_hover_color, text_color=self.button_text_color)
        self.start_server.grid(row=0,column=0,padx=(20,0),pady=(20, 0))
        self.join_server = ctk.CTkButton(self, text="Join Server", font=('Consolas', 24),command=self.main.start_client, fg_color=self.button_color, hover_color=self.button_hover_color, text_color=self.button_text_color)
        self.join_server.grid(row=0,column=1,padx=(10,10),pady=(20, 0))
        self.disconnect_server = ctk.CTkButton(self, text="Disconnect", font=('Consolas', 24),command=self.disconnect_client, fg_color=self.button_color, hover_color=self.button_hover_color, text_color=self.button_text_color)
        self.disconnect_server.grid(row=0,column=2,padx=(0,20),pady=(20, 0))
        self.table = CTkTable(master=self, row=0, column=2, values=[["Name", "Address"]],
                              font=('Consolas', 20),
                              width=500,
                              padx=5, pady=5, 
                              text_color=text,
                              colors=[text_bg, text_bg], 
                              color_phase='vertical', 
                              header_color=text_bg,
                              corner_radius=10,
                              hover_color=hover_color)
        #self.table.pack(expand=False, fill="both", padx=20, pady=20)
        self.table.grid(row=1,column=0,columnspan=3,padx=20,pady=20)

    def start_server(self):
        self.main.start_server()
        self.server = self.main.server
        self.update_clients()

    def disconnect_client(self):
        self.main.disconnect_client()
        self.server = self.main.server
        self.update_clients()

    def title_color(self):
        themes.title_bar_color_handle(self)

    def window(self, fg_cl):
        self.configure(fg_color=fg_cl)
        self.title("Server Panel")
        self.geometry("600x600")
        self.iconbitmap("images/logo.ico")
        self.resizable(False, False)

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