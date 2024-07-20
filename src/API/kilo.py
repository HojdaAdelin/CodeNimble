import requests
from bs4 import BeautifulSoup
import customtkinter as ct
import sys
import os
from tkinter import *

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Config import check
from MainMenu import themes

class Kilotools(ct.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Code Nimble - Kilonova tools")
        self.geometry("600x200")
        self.iconbitmap("images/logo.ico")
        self.resizable(False, False)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
        }
        self.contest_info()
        self.fg_cl, self.text_bg, self.text, self.hover_color = themes.return_default_win_color(check.get_config_value("theme"))
        self.configure(fg_color = self.fg_cl, bg_color = self.fg_cl)
        themes.title_bar_color_handle(self)
        self.gui()

    def gui(self):
        self.contest_label = ct.CTkLabel(self,text="Latest contest: "+self.contest_name, font=("",20), text_color=self.text)
        self.contest_label.pack(side=TOP, anchor="center",padx=5,pady=5)
        self.contest_status_label = ct.CTkLabel(self,text="Status: "+self.contest_status, font=("",20), text_color=self.text)
        self.contest_status_label.pack(side=TOP, anchor="center",padx=5)

    def contest_info(self):
        BASE_URL = 'https://kilonova.ro/contests?page=official'
        response = requests.get(BASE_URL, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        first_container = soup.find(class_='c-container mb-2')
        self.contest_name = first_container.find(class_='segment-panel my-1').find('h2').text.strip()
        status_paragraph = first_container.find('p', string=lambda t: t and t.startswith('Status:'))
        self.contest_status = ' '.join(status_paragraph.text.split()).replace('Status: ', '')

    def get_contest_name(self):
        return self.contest_name
    def get_contest_status(self):
        return self.contest_status