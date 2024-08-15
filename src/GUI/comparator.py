import customtkinter as ct
import tkinter as tk
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Config import check
from Core import themes

class OutputComparator(ct.CTk):
    def __init__(self, panel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Setează dimensiunea ferestrei
        self.geometry("450x300")
        self.title("Output Comparator")
        self.iconbitmap("images/logo.ico")
        fg_cl, text_bg, text, hover_color, button_color, button_hover_color, button_text_color = themes.return_default_win_color(check.get_config_value("theme"))
        
        # Creează un frame pentru a conține TextBox-ul și scrollbars
        frame = ct.CTkFrame(self, fg_color=fg_cl)
        frame.pack(expand=True, fill="both")
        
        # Creează TextBox-ul folosind tkinter.Text
        self.textbox = tk.Text(frame, wrap="word", state="disabled",bg=text_bg,fg=text, font=("Consolas", 30))
        self.textbox.pack(side="left", expand=True, fill="both")
        
        # Creează scrollbars din customtkinter
        scrollbar_y = ct.CTkScrollbar(frame, orientation="vertical", command=self.textbox.yview, button_color=button_color, button_hover_color=button_hover_color)
        scrollbar_y.pack(side="right", fill="y")
        
        scrollbar_x = ct.CTkScrollbar(self, orientation="horizontal", command=self.textbox.xview, button_color=button_color, button_hover_color=button_hover_color)
        scrollbar_x.pack(side="bottom", fill="x")

        # Asociază scrollbars cu TextBox-ul
        self.textbox.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Compară și afișează rezultatele
        self.compare_and_display(panel)
        themes.title_bar_color_handle(self)

    
    def compare_and_display(self, panel):
        # Obține textul din fiecare TextBox și îl transformă în liste
        output_list = panel.output_box.get("1.0", "end-1c").split()
        expected_list = panel.expected_box.get("1.0", "end-1c").split()
        
        # Permite modificarea TextBox-ului
        self.textbox.configure(state="normal")
        
        # Curăță TextBox-ul
        self.textbox.delete("1.0", "end")
        
        # Compară elementele din cele două liste și formatează textul
        for i, (output, expected) in enumerate(zip(output_list, expected_list), start=1):
            result = f"{i}. {expected} ("
            if output == expected:
                result += "correct"
                self.textbox.insert("end", result + ")\n", "correct")
            else:
                result += "incorrect"
                self.textbox.insert("end", result + ")\n", "incorrect")
        
        # Dacă există elemente în `expected_list` care nu au pereche în `output_list`
        if len(expected_list) > len(output_list):
            for i, expected in enumerate(expected_list[len(output_list):], start=len(output_list) + 1):
                result = f"{i}. {expected} (incorrect)\n"
                self.textbox.insert("end", result, "incorrect")
        
        # Configurare stiluri
        self.textbox.tag_configure("correct", foreground="green")
        self.textbox.tag_configure("incorrect", foreground="red")
        
        # Dezactivează modificarea TextBox-ului
        self.textbox.configure(state="disabled")