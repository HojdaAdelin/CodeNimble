import tkinter as tk
import re
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Config import check
from MainMenu import file_menu
from MainMenu import themes

class Suggestions(tk.Text):
    def __init__(self, master, root, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.root = root
        self.configure(height=5, width=30, wrap="none", font=("Courier", check.get_config_value("zoom")))
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
        self.hide_suggestions()
        self.binding()

    def binding(self):
        self.bind('<Button-1>', self.on_suggestion_click)
        self.bind('<FocusOut>', self.hide_suggestions)
        self.bind("<Escape>", self.hide_suggestions)
        self.bind('<Motion>', self.on_mouse_motion)

    def on_suggestion_click(self, event):
        index = self.index("@%d,%d" % (event.x, event.y))
        suggestion = self.get(f"{index} linestart", f"{index} lineend").strip()
        suggestion = self.strip_marker(suggestion)
        if suggestion:
            self.insert_suggestion(suggestion)
        self.hide_suggestions()

    def hide_suggestions(self, event=None):
        self.place_forget()

    def insert_suggestion(self, suggestion):
        current_word = self.get_current_word()
        cursor_index = self.root.index(tk.INSERT)
        start_index = f'{cursor_index} - {len(current_word)}c'
        self.root.text.delete(start_index, cursor_index)
        self.root.text.insert(cursor_index, suggestion)

    def on_mouse_motion(self, event):
        widget = event.widget
        index = widget.index("@%d,%d" % (event.x, event.y))
        self.highlight_line(index)

    def highlight_line(self, index):
        self.tag_remove("highlight", "1.0", tk.END)
        self.tag_add("highlight", f"{index} linestart", f"{index} lineend")
        self.tag_config("highlight", background=self.cget("selectbackground"), foreground=self.cget("selectforeground"))

    def on_up_key(self, event):
        return 'break'  # Handled by text_widget

    def on_down_key(self, event):
        return 'break'  # Handled by text_widget

    def on_keyrelease_all(self, event):
        if file_menu.return_file() == ".cpp":
            if event.widget == self.root.text:
                if event.keysym in ('Up', 'Down', 'Left', 'Right', 'Return', 'Tab', 'space', "enter", "Backspace"):
                    self.hide_suggestions()
                    return

                if event.keysym == "Escape":
                    self.hide_suggestions()
                    return

                self.update_suggestions()

    def update_suggestions(self):
        typed_word = self.get_current_word()
        if typed_word:
            matching_keywords = [
                f"\u25A0 {kw}" if kw in self.local_variables else kw
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
        self.config(state=tk.NORMAL)
        self.delete("1.0", tk.END)
        for suggestion in suggestions:
            self.insert(tk.END, suggestion + "\n")
        cursor_index = self.root.text.index(tk.INSERT)
        cursor_position = self.root.text.bbox(cursor_index)
        if cursor_position:
            x, y, width, height = cursor_position
            self.place(x=x+(4 * int(check.get_config_value('zoom'))), y=y+80+(int(check.get_config_value('zoom'))))
        self.config(state=tk.DISABLED)

    def handle_tab(self):
        if self.handle_case():
            first_suggestion = self.get("1.0", "1.end").strip()
            first_suggestion = self.strip_marker(first_suggestion)
            self.insert_suggestion(first_suggestion)
            self.hide_suggestions()
            self.root.text.focus_set()
            return 'break'
        
    def handle_enter(self):
        if self.handle_case():
            first_suggestion = self.get("1.0", "1.end").strip()
            first_suggestion = self.strip_marker(first_suggestion)
            self.insert_suggestion(first_suggestion)
            self.hide_suggestions()
            self.root.text.focus_set()
            return 'break'
        
    def on_text_modified(self, event=None):
        text = self.root.text.get("1.0", tk.END)
        pattern = re.compile(r'\b\w+\b')
        matches = pattern.findall(text)
        current_word = self.get_current_word()
        self.local_variables = set(matches) - set(self.keywords) - {current_word}
        self.root.text.edit_modified(False)
        if file_menu.return_file() == ".cpp":
            self.update_suggestions()

    def handle_case(self):
        if self.get("1.0", tk.END).strip() and self.winfo_ismapped():
            return True
        else:
            return False

    def strip_marker(self, text):
        return text.replace("\u25A0 ", "")

# Restul codului pentru integrarea cu alte părți ale aplicației rămâne neschimbat.
