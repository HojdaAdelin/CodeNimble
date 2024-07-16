import customtkinter as ct
import tkinter as tk
from tkinter import messagebox
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from MainMenu import themes
from Config import check

class SnippetsCode(ct.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Snippets Code")
        self.geometry("800x600")
        self.fg, self.text_bg, self.text, self.hover = themes.return_default_win_color(check.get_config_value("theme"))
        themes.title_bar_color_handle(self)
        self.configure(fg_color=self.fg, bg_color=self.fg)
        
        self.entry = ct.CTkEntry(self, width=760, fg_color=self.text_bg, text_color=self.text,font=("", 20))
        self.entry.pack(fill=ct.X, padx=10, pady=10)
        
        bottom_frame = ct.CTkFrame(self, fg_color=self.fg, bg_color=self.fg)
        bottom_frame.pack(fill=ct.BOTH, expand=True, padx=10, pady=10)
        
        self.textbox = ct.CTkTextbox(bottom_frame, fg_color=self.text_bg, bg_color=self.text_bg, text_color=self.text,font=("", 18))
        self.textbox.pack(side=ct.LEFT, fill=ct.BOTH, expand=True, padx=10, pady=10)
        
        self.listbox = ct.CTkFrame(bottom_frame, fg_color=self.fg, bg_color=self.fg)
        self.listbox.pack(side=ct.RIGHT, fill=ct.BOTH, expand=True, padx=10, pady=10)

        self.listbox_list = tk.Listbox(self.listbox, bg=self.text_bg, fg=self.text, font=("", 28))
        self.listbox_list.pack(fill=ct.BOTH, expand=True)
        
        button_frame = ct.CTkFrame(self, fg_color=self.fg, bg_color=self.fg)
        button_frame.pack(fill=ct.X, padx=10, pady=10)
        
        create_button = ct.CTkButton(button_frame, text="Create", command=self.create_snippet)
        create_button.pack(side=ct.LEFT, padx=10)
        
        edit_button = ct.CTkButton(button_frame, text="Edit", command=self.edit_snippet)
        edit_button.pack(side=ct.LEFT, padx=10)
        
        save_button = ct.CTkButton(button_frame, text="Save", command=self.save_snippet)
        save_button.pack(side=ct.LEFT, padx=10)
        
        remove_button = ct.CTkButton(button_frame, text="Remove", command=self.remove_snippet)
        remove_button.pack(side=ct.LEFT, padx=10)

        self.listbox_list.bind("<Double-Button-1>", lambda event:self.edit_snippet())
        self.minsize(width=800, height=600)
        
        self.check_and_create_snippets_folder()
        self.populate_listbox()

    def check_and_create_snippets_folder(self):
        snippets_dir = os.path.join('Snippets')
        if not os.path.exists(snippets_dir):
            os.makedirs(snippets_dir)
        self.snippets_dir = snippets_dir

    def populate_listbox(self):
        self.listbox_list.delete(0, tk.END)  
        for file_name in os.listdir(self.snippets_dir):
            if os.path.isfile(os.path.join(self.snippets_dir, file_name)):
                self.listbox_list.insert(tk.END, os.path.splitext(file_name)[0])
    
    def create_snippet(self):
        snippet_name = self.entry.get().strip()
        if not snippet_name:
            messagebox.showwarning("Warning", "You need to write the name in entry!")
            return
        
        if not snippet_name.endswith(".txt"):
            snippet_name += ".txt"
        
        snippet_path = os.path.join(self.snippets_dir, snippet_name)
        if not os.path.exists(snippet_path):
            with open(snippet_path, 'w') as f:
                f.write("")
            
            self.populate_listbox()  
        else:
            messagebox.showinfo("Info", f"Snippet {snippet_name} already exists.")

    def edit_snippet(self, event=None):
        selected_index = self.listbox_list.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "You need to select a snippet from the listbox!")
            return
        
        selected_file = self.listbox_list.get(selected_index)
        snippet_path = os.path.join(self.snippets_dir, selected_file + ".txt")
        
        with open(snippet_path, 'r') as file:
            content = file.read()
        
        self.textbox.delete("1.0", tk.END)
        self.textbox.insert("1.0", content)

    def save_snippet(self):
        selected_index = self.listbox_list.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "You need to select a snippet from the listbox!")
            return
        
        selected_file = self.listbox_list.get(selected_index)
        snippet_path = os.path.join(self.snippets_dir, selected_file + ".txt")
        
        content = self.textbox.get("1.0", tk.END).strip()
        with open(snippet_path, 'w') as file:
            file.write(content)
        
        messagebox.showinfo("Info", f"Snippet {selected_file} has been saved.")
    
    def remove_snippet(self):
        selected_index = self.listbox_list.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "You need to select a snippet from the listbox!")
            return
        
        selected_file = self.listbox_list.get(selected_index)
        snippet_path = os.path.join(self.snippets_dir, selected_file + ".txt")
        
        if os.path.exists(snippet_path):
            os.remove(snippet_path)
            self.populate_listbox()
            messagebox.showinfo("Info", f"Snippet {selected_file} has been removed.")
        else:
            messagebox.showwarning("Warning", f"Snippet {selected_file} does not exist.")