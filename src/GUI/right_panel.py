import sys
import os
import customtkinter as ct
import tkinter as tk

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

class RightPanel(ct.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(corner_radius=0)
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=0)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=0)

        # Label-ul pentru input
        self.input_label = ct.CTkLabel(self, text="Input Label")
        self.input_label.grid(row=0, column=0, padx=10, pady=5, sticky="n")

        # Textbox pentru input
        self.input_box = ct.CTkTextbox(self, height=10)
        self.input_box.grid(row=1, column=0, padx=10, pady=(0,5), sticky="nsew")

        # Label-ul pentru output
        self.output_label = ct.CTkLabel(self, text="Output Label")
        self.output_label.grid(row=2, column=0, padx=10, pady=(0,5), sticky="n")

        # Textbox pentru output
        self.output_box = ct.CTkTextbox(self, height=10)
        self.output_box.grid(row=3, column=0, padx=10, pady=(0,5), sticky="nsew")

        # Label-ul pentru expected output
        self.expected_label = ct.CTkLabel(self, text="Expected Output")
        self.expected_label.grid(row=4, column=0, padx=10, pady=(0,5), sticky="n")

        # Textbox pentru expected output
        self.expected_box = ct.CTkTextbox(self, height=10)
        self.expected_box.grid(row=5, column=0, padx=10, pady=(0,10), sticky="nsew")

        # Partea inferioara
        self.fetch = ct.CTkButton(self,text="Fetch test cases", font=("", 16))
        self.fetch.grid(row=6, column=0, padx=10, pady=(0, 5), sticky="swe")
