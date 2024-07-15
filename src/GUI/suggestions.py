import threading
import tkinter as tk
from tkinter import messagebox
import customtkinter as ct
import re
import sys
import os
import keyword

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Config import check
from MainMenu import view_menu
from MainMenu import file_menu
from GUI import filetab
from Server import server
from Server import client
from MainMenu import run
from MainMenu import themes
from Server import password_handle
from GUI import terminal

class Suggestions(tk.Listbox):
    def __init__(self, master, root, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.root = root
        self.height = 5
        self.width = 25
        self.font = ("", check.get_config_value("zoom"))
        self.configure(width=self.width, height=self.height, font=self.font)
        self.keywords = [
                'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else',
                'enum', 'extern', 'float', 'for', 'goto', 'if', 'inline', 'int', 'long', 'register', 'restrict',
                'return', 'short', 'signed', 'sizeof', 'static', 'struct', 'switch', 'typedef', 'union', 'unsigned',
                'void', 'volatile', 'while', 'using', 'namespace', 'std', 'vector', 'set', 'map', 'unordered_map',
                'queue', 'priority_queue', 'stack', 'list', 'deque', 'algorithm', 'iterator', 'utility', 'functional',
                'numeric', 'limits', 'memory', 'shared_ptr', 'unique_ptr', 'make_shared', 'make_unique', 'move',
                'swap', 'typeid', 'type_traits', 'function', 'bind', 'placeholders', 'tuple', 'array', 'bitset',
                'complex', 'valarray', 'future', 'promise', 'thread', 'mutex', 'condition_variable', 'chrono',
                'ratio', 'random', 'atomic', 'filesystem', 'ratio', 'complex', 'valarray', 'new', 'delete',
                'template', 'typename', 'bool', 'catch', 'class', 'const_cast', 'dynamic_cast', 'explicit', 'export',
                'friend', 'mutable', 'operator', 'private', 'protected', 'public', 'reinterpret_cast',
                'static_assert', 'static_cast', 'throw', 'try', 'typeid', 'typename', 'virtual', 'wchar_t',
                'and', 'and_eq', 'asm', 'bitand', 'bitor', 'compl', 'not', 'not_eq', 'or', 'or_eq', 'xor', 'xor_eq',
                'true', 'false'
            ]
        self.local_variables = set()
        self.current_file = None
        self.binding()

    def binding(self):
        self.bind('<Button-1>', self.on_suggestion_click)
        self.bind('<FocusOut>', self.hide_suggestions)
        self.bind("<Escape>", self.hide_suggestions)
        self.bind('<<ListboxSelect>>', self.on_suggestion_select)
        self.bind('<Motion>', self.on_mouse_motion)

    def on_suggestion_click(self, event):
        selected_suggestion = self.get(tk.ACTIVE)
        if selected_suggestion:
            self.insert_suggestion(selected_suggestion)
        self.hide_suggestions()
        
    def hide_suggestions(self, event=None):
        self.place_forget()

    def on_suggestion_select(self, event):
        selected_index = self.curselection()
        if selected_index:
            selected_text = self.get(selected_index)
            self.insert_suggestion(selected_text)

    def insert_suggestion(self, suggestion):
        current_word = self.root.get_current_word()
        cursor_index = self.root.index(tk.INSERT)
        # Calculate the start index of the current word
        start_index = f'{cursor_index} - {len(current_word)}c'
        # Delete the current word
        self.root.text.delete(start_index, cursor_index)
        if suggestion.endswith(" (local)"):
            suggestion = suggestion[:-8] 
        # Insert the suggestion
        self.root.text.insert(cursor_index, suggestion)

    def on_mouse_motion(self, event):
        widget = event.widget
        widget.focus()
        widget.select_clear(0, tk.END)
        widget.select_set(widget.nearest(event.y))

    def on_up_key(self, event):
        if self.winfo_ismapped():
            if self.curselection():
                index = self.curselection()[0]
                if index > 0:
                    self.select_clear(0, tk.END)
                    self.select_set(index - 1)
                    self.see(index - 1)
                    self.focus_set() 
            return 'break'
        else:
            return None
    
    def on_down_key(self, event):
        if self.winfo_ismapped():
    
            if self.curselection():
                index = self.curselection()[0]
                if index < self.size() - 1:
                    self.select_clear(0, tk.END)
                    self.select_set(index + 1)
                    self.see(index + 1)
                    self.focus_set() 
            return 'break'
        else:
            return None
        
    def on_keyrelease_all(self, event):
        if file_menu.return_file() == ".cpp":
            if event.widget == self.root.text:
                if event.keysym in ('Up', 'Down', 'Left', 'Right', 'Return', 'Tab', 'space', "enter", "Backspace"):
                    self.hide_suggestions()  # Ascunde sugestiile la apăsarea acestor taste
                    return  # Sari peste tastele săgeți, Enter, Tab și spațiu

                # Verifică dacă a fost apăsată tasta "Escape" și oprește afișarea sugestiilor
                if event.keysym == "Escape":
                    self.hide_suggestions()
                    return

                # Actualizează sugestiile doar dacă nu a fost apăsată tasta "Escape"
                self.update_suggestions()

    def update_suggestions(self):
        typed_word = self.get_current_word()
        if typed_word:
            matching_keywords = [
                f"{kw} (local)" if kw in self.local_variables else kw
                for kw in (list(self.local_variables) + self.keywords)
                if kw.startswith(typed_word)
            ]
            if matching_keywords:
                self.show_suggestions(matching_keywords)
            else:
                self.hide_suggestions()
        else:
            self.hide_suggestions()

    def get_current_word(self):
        try:
            cursor_index = self.root.index(tk.INSERT)
            line_start = self.root.index(f'{cursor_index} linestart')
            current_line_text = self.root.get(line_start, cursor_index)
            return current_line_text.split()[-1] if current_line_text else ''
        except IndexError:
            return ''
        
    def show_suggestions(self, suggestions):
        self.delete(0, tk.END)
        for suggestion in suggestions:
            self.insert(tk.END, suggestion)
        cursor_index = self.root.text.index(tk.INSERT)
        cursor_position = self.root.text.bbox(cursor_index)
        if cursor_position:
            x, y, width, height = cursor_position
            self.place(x=x+(4 * int(check.get_config_value("zoom"))), y=y+80+(int(check.get_config_value("zoom"))))
            self.select_set(0)

    def handle_tab(self):
        if self.handle_case() == True:
            first_suggestion = self.get(0)
            self.insert_suggestion(first_suggestion)
            self.hide_suggestions()
            self.root.text.focus_set()
            return 'break'
        
    def handle_enter(self):
        if self.handle_case() == True:
            first_suggestion = self.get(0)
            self.insert_suggestion(first_suggestion)
            self.hide_suggestions()
            self.root.text.focus_set()
            return 'break'
        
    def on_text_modified(self, event=None):
        # Obține textul curent din widget
        text = self.root.text.get("1.0", tk.END)
        
        # Folosim regex pentru a găsi variabile locale
        pattern = re.compile(r'\b\w+\b')
        matches = pattern.findall(text)
        current_word = self.get_current_word()
        # Actualizăm setul de variabile locale
        self.local_variables = set(matches) - set(self.keywords) - {current_word}
        self.root.text.edit_modified(False)
        # Actualizăm sugestiile
        if file_menu.return_file() == ".cpp":
            self.update_suggestions()

    def handle_case(self):
        if self.size() > 0 and self.winfo_ismapped():
            return True
        else:
            return False