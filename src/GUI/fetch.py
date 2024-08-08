import tkinter as tk
import customtkinter as ct
from tkinter import messagebox
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from MainMenu import themes
from Config import check
from API import fetch_get

class FetchWindow(ct.CTk):
    def __init__(self,terminal,right_panel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("320x120")
        self.title("Code Nimble - fetch test cases")
        self.terminal = terminal
        self.right_panel = right_panel
        self.iconbitmap("images/logo.ico")
        self.resizable(False, False)
        self.bg_color, self.text_bg, self.text, self.hover_color = themes.return_default_win_color(check.get_config_value("theme"))
        self.gui()
        themes.title_bar_color_handle(self)
        self.columnconfigure(1, weight=0)
        self.configure(fg_color = self.bg_color)
        self.contest_id_for_cf = ct.CTkEntry(self, text_color=self.text, fg_color=self.text_bg, border_width=0)
        self.contest_id_for_cf_label = ct.CTkLabel(self,text="Contest ID", text_color=self.text, font=("", 16))

    def toggle_gui(self, platform):
        if platform == "Pbinfo" or platform == "Kilonova":
            self.contest_id_for_cf.grid_forget()
            self.contest_id_for_cf_label.grid_forget()
            self.geometry()
            self.geometry("320x120")
            self.fetch_button.grid_forget()
            self.fetch_button.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nwe")
            self.id_label.configure(text="Problem ID")
        elif platform == "Codeforces":
            self.contest_id_for_cf_label.grid(row=0, column=2, pady=(10, 5), padx=10, sticky="n")
            self.contest_id_for_cf.grid(row=1, column=2,padx=10, pady=(0, 10), sticky="ne")
            self.fetch_button.grid_forget()
            self.fetch_button.grid(row=2, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="nwe")
            self.geometry("480x120")
            self.id_label.configure(text="Problem ID")
        elif platform == "AtCoder":
            self.contest_id_for_cf.grid_forget()
            self.contest_id_for_cf_label.grid_forget()
            self.geometry()
            self.geometry("320x120")
            self.fetch_button.grid_forget()
            self.fetch_button.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nwe")
            self.id_label.configure(text="URL")
    def gui(self):
        self.site_label = ct.CTkLabel(self,text="Platform", text_color=self.text, font=("", 16))
        self.site_label.grid(row=0, column=0, pady=(10, 5), padx=10, sticky="n")
        self.id_label = ct.CTkLabel(self, text="Problem ID", text_color=self.text, font=("", 16))
        self.id_label.grid(row=0, column=1, pady=(10, 5), padx=10, sticky="n")
        self.site = ct.CTkComboBox(self, values=["Pbinfo", "Kilonova", "Codeforces", "AtCoder"],command=self.toggle_gui, font=("", 16), text_color=self.text, fg_color=self.text_bg, dropdown_fg_color=self.text_bg, dropdown_text_color=self.text, button_color=self.text_bg, button_hover_color=self.hover_color, dropdown_hover_color=self.hover_color, border_width=0)
        self.site.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nw")
        self.id = ct.CTkEntry(self, text_color=self.text, fg_color=self.text_bg, border_width=0)
        self.id.grid(row=1,column=1,padx=10, pady=(0, 10), sticky="ne")
        self.fetch_button = ct.CTkButton(self, text="Fetch test cases", command=self.fetch)
        self.fetch_button.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nwe")

    def fetch(self):
        if self.site.get().strip() == "Pbinfo" or self.site.get().strip() == "Kilonova" or self.site.get().strip() == "Codeforces" or self.site.get().strip() == "AtCoder":
            pass
        else:
            messagebox.showerror("Error", "Invalid platform!")
            return

        if len(self.id.get().strip()) == 0:
            messagebox.showerror("Error", "Please enter a valid problem ID!")
            return
        
        if self.site.get().strip() == "Pbinfo":
            self.intrare, self.iesire = fetch_get.fetch_pbinfo(self.terminal, self.id.get().strip())
            self.right_panel.input_box.delete("1.0", "end")
            self.right_panel.input_box.insert("1.0", self.intrare)
            self.right_panel.expected_box.delete("1.0", "end")
            self.right_panel.expected_box.insert("1.0", self.iesire)
        elif self.site.get().strip() == "Kilonova":
            self.intrare, self.iesire = fetch_get.fetch_kilonova(self.terminal, self.id.get().strip())
            self.right_panel.input_box.delete("1.0", "end")
            self.right_panel.input_box.insert("1.0", self.intrare)
            self.right_panel.expected_box.delete("1.0", "end")
            self.right_panel.expected_box.insert("1.0", self.iesire)
        elif self.site.get().strip() == "Codeforces":
            self.intrare, self.iesire = fetch_get.fetch_codeforce(contest_id=self.contest_id_for_cf.get().strip(), problem_id=self.id.get().strip())
            self.right_panel.input_box.delete("1.0", "end")
            self.right_panel.input_box.insert("1.0", self.intrare)
            self.right_panel.expected_box.delete("1.0", "end")
            self.right_panel.expected_box.insert("1.0", self.iesire)
        elif self.site.get().strip() == "AtCoder":
            self.intrare, self.iesire = fetch_get.fetch_atcoder(self.id.get().strip())
            self.right_panel.input_box.delete("1.0", "end")
            self.right_panel.input_box.insert("1.0", self.intrare)
            self.right_panel.expected_box.delete("1.0", "end")
            self.right_panel.expected_box.insert("1.0", self.iesire)
    
        
