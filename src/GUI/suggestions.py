import tkinter as tk
import customtkinter as ct
import re
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Config import check
from MainMenu import file_menu
from MainMenu import themes

class Suggestions(tk.Frame):
    def __init__(self, master, root, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.root = root

        self.suggestions_text = tk.Text(self, height=6, width=20, wrap="none", font=("Courier", check.get_config_value("zoom")))
        self.suggestions_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar = ct.CTkScrollbar(self,orientation="vertical", command=self.sync_scroll)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tags_text = tk.Text(self, height=6, width=7, wrap="none", font=("Courier", check.get_config_value("zoom")))
        self.tags_text.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.suggestions_text.config(yscrollcommand=self.on_scrollbar)
        self.tags_text.config(yscrollcommand=self.on_scrollbar)

        self.keywords_selector()
        self.snippets_code = []
        self.snippet_code()
        self.local_variables = set()
        self.current_file = None
        self.current_selection = 0
        self.hide_suggestions()
        self.binding()

    def sync_scroll(self, *args):
        self.suggestions_text.yview(*args)
        self.tags_text.yview(*args)

    def on_scrollbar(self, *args):
        self.scrollbar.set(*args)
        self.sync_scroll('moveto', args[0])

    def keywords_selector(self):
        self.cpp_keywords = [
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else',
            'enum', 'float', 'for', 'goto', 'if', 'inline', 'int', 'long',
            'return', 'short', 'signed', 'sizeof', 'static', 'struct', 'switch', 'typedef', 'unsigned',
            'void', 'while', 'using', 'namespace', 'std', 'vector', 'set', 'map', 'unordered_map', 'cout', 'cin',
            'queue', 'priority_queue', 'stack', 'list', 'deque', 'algorithm', 'iterator', 'utility', 'functional',
            'numeric', 'limits', 'shared_ptr', 'unique_ptr', 'make_shared', 'make_unique', 'move',
            'swap', 'typeid', 'type_traits', 'function', 'bind', 'placeholders', 'tuple', 'array', 'bitset',
            'complex', 'valarray', 'future', 'promise', 'thread', 'mutex', 'condition_variable', 'chrono',
            'ratio', 'random', 'atomic', 'filesystem', 'ratio', 'complex', 'valarray', 'new', 'delete',
            'template', 'typename', 'bool', 'catch', 'class', 'const_cast', 'dynamic_cast', 'explicit', 'export',
            'friend', 'mutable', 'operator', 'private', 'protected', 'public', 'reinterpret_cast',
            'static_assert', 'static_cast', 'throw', 'try', 'typeid', 'typename', 'virtual', 'wchar_t',
            'and', 'and_eq', 'asm', 'bitand', 'bitor', 'compl', 'not', 'not_eq', 'or', 'or_eq', 'xor', 'xor_eq',
            'true', 'false'
        ]
        self.py_keywords = ["False", "None", "True", "and", "as", "assert", "async", "await", "break", "class",
        "continue", "def", "del", "elif", "else", "except", "finally", "for", "from",
        "global", "if", "import", "in", "is", "lambda", "nonlocal", "not", "or", "pass",
        "raise", "return", "try", "while", "with", "yield",
        'abs', 'delattr', 'hash', 'memoryview', 'set', 'all', 'dict', 'help', 'min', 'setattr', 'any', 'dir', 'hex',
        'next', 'slice', 'ascii', 'divmod', 'id', 'object', 'sorted', 'bin', 'enumerate', 'input', 'oct', 'staticmethod',
        'bool', 'eval', 'int', 'open', 'str', 'breakpoint', 'exec', 'isinstance', 'ord', 'sum', 'bytearray', 'filter',
        'issubclass', 'pow', 'super', 'bytes', 'float', 'iter', 'print', 'tuple', 'callable', 'format', 'len', 'property',
        'type', 'chr', 'frozenset', 'list', 'range', 'vars', 'classmethod', 'getattr', 'locals', 'repr', 'zip', 'compile',
        'globals', 'map', 'reversed', '__import__', 'complex', 'hasattr', 'max', 'round',
        'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort',
        'capitalize', 'casefold', 'center', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'format_map', 'isalnum',
        'isalpha', 'isascii', 'isdecimal', 'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace',
        'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans', 'partition', 'replace', 'rfind', 'rindex',
        'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title',
        'translate', 'upper', 'zfill']

    def binding(self):
        self.suggestions_text.bind('<Button-1>', self.on_suggestion_click)
        self.suggestions_text.bind('<FocusOut>', self.hide_suggestions)
        self.suggestions_text.bind("<Escape>", self.hide_suggestions)
        self.suggestions_text.bind('<Motion>', self.on_mouse_motion)

    def on_suggestion_click(self, event):
        index = self.suggestions_text.index("@%d,%d" % (event.x, event.y))
        suggestion = self.suggestions_text.get(f"{index} linestart", f"{index} lineend").strip()
        tag = self.tags_text.get(f"{index} linestart", f"{index} lineend").strip()
        if suggestion and tag == "snippet":
            self.insert_suggestion(suggestion, snippet=tag)
        elif suggestion:
            self.insert_suggestion(suggestion)
        self.hide_suggestions()

    def hide_suggestions(self, event=None):
        self.place_forget()

    def insert_suggestion(self, suggestion, snippet=None):
        current_word = self.get_current_word().strip()
        if not current_word:
            return
        if snippet == "snippet":
            src = "Snippets/" + suggestion + ".txt"
            with open(src, "r") as file:
                suggestion = file.read()

        cursor_index = self.root.index(tk.INSERT)
        start_index = f'{cursor_index} - {len(current_word)}c'
        self.root.text.delete(start_index, cursor_index)
        self.root.text.insert(cursor_index, suggestion)

    def on_mouse_motion(self, event):
        widget = event.widget
        index = widget.index("@%d,%d" % (event.x, event.y))
        self.highlight_line(index)

    def highlight_line(self, index):
        try:
            line_start = self.suggestions_text.index(f"{index} linestart")
            line_end = self.suggestions_text.index(f"{index} lineend")
            self.suggestions_text.tag_remove("highlight", "1.0", tk.END)
            self.suggestions_text.tag_add("highlight", line_start, line_end)
            self.suggestions_text.tag_config("highlight", background=self.suggestions_text.cget("selectbackground"), foreground=self.suggestions_text.cget("selectforeground"))
        except tk.TclError:
            pass

    def on_up_key(self, event):
        pass

    def on_down_key(self, event):
        pass

    def on_keyrelease_all(self, event):
        if file_menu.return_file() == ".cpp" or file_menu.return_file() == ".py":
            if event.widget == self.root.text:
                if event.keysym in ('Up', 'Down', 'Left', 'Right', 'Return', 'Tab', 'space', "enter", "Backspace"):
                    self.hide_suggestions()
                    return

                if event.keysym == "Escape":
                    self.hide_suggestions()
                    return

                self.update_suggestions()

    def update_suggestions(self):
        if file_menu.return_file() == ".cpp":
            self.keywords = self.cpp_keywords
        elif file_menu.return_file() == ".py":
            self.keywords = self.py_keywords
        typed_word = self.get_current_word().strip()
        if typed_word and not typed_word.isspace():
            matching_keywords = [
                f"{kw}" if kw in self.local_variables else kw
                for kw in (list(self.local_variables) + self.keywords + self.snippets_code)
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
            words = current_line_text.split()
            if words and current_line_text.endswith(words[-1]):
                return words[-1]
            else:
                return ''
        except IndexError:
            return ''

    def show_suggestions(self, suggestions):
        if file_menu.return_file() == ".cpp":
            self.keywords = self.cpp_keywords
        elif file_menu.return_file() == ".py":
            self.keywords = self.py_keywords
        self.suggestions_text.config(state=tk.NORMAL)
        self.tags_text.config(state=tk.NORMAL)
        self.suggestions_text.delete("1.0", tk.END)
        self.tags_text.delete("1.0", tk.END)
        for suggestion in suggestions:
            self.suggestions_text.insert(tk.END, suggestion + "\n")
            if suggestion in self.keywords:
                self.tags_text.insert(tk.END, "keyword\n")
            elif suggestion in self.local_variables:
                self.tags_text.insert(tk.END, "local\n")
            elif suggestion in self.snippets_code:
                self.tags_text.insert(tk.END, "snippet\n")
            else:
                self.tags_text.insert(tk.END, "\n")
        cursor_index = self.root.text.index(tk.INSERT)
        cursor_position = self.root.text.bbox(cursor_index)
        if cursor_position:
            x, y, width, height = cursor_position
            self.place(x=x+(4 * int(check.get_config_value('zoom'))), y=y+80+(int(check.get_config_value('zoom'))))
        self.suggestions_text.config(state=tk.DISABLED)
        self.tags_text.config(state=tk.DISABLED)

    def handle_tab(self):
        if self.handle_case():
            first_suggestion = self.suggestions_text.get("1.0", "1.end").strip()
            tag = self.tags_text.get("1.0", "1.end").strip()
            if tag == "snippet":
                self.insert_suggestion(first_suggestion, snippet=tag)
            else:
                self.insert_suggestion(first_suggestion)
            self.hide_suggestions()
            self.root.text.focus_set()
            return 'break'
        
    def handle_enter(self):
        if self.handle_case():
            first_suggestion = self.suggestions_text.get("1.0", "1.end").strip()
            tag = self.tags_text.get("1.0", "1.end").strip()
            if tag == "snippet":
                self.insert_suggestion(first_suggestion, snippet=tag)
            else:
                self.insert_suggestion(first_suggestion)
            self.hide_suggestions()
            self.root.text.focus_set()
            return 'break'
        
    def on_text_modified(self, event=None):

        if file_menu.return_file() == ".cpp":
            self.keywords = self.cpp_keywords
        elif file_menu.return_file() == ".py":
            self.keywords = self.py_keywords
        else:
            self.keywords = []
        text = self.root.text.get("1.0", tk.END)
        pattern = re.compile(r'\b\w+\b')
        matches = pattern.findall(text)
        current_word = self.get_current_word().strip()
        self.local_variables = set(matches) - set(self.keywords) - set(self.snippets_code) - {current_word}
        self.root.text.edit_modified(False)
        if file_menu.return_file() == ".cpp" or file_menu.return_file() == ".py":
            self.update_suggestions()

    def handle_case(self):
        if self.suggestions_text.get("1.0", tk.END).strip() and self.winfo_ismapped():
            return True
        else:
            return False
        
    def snippet_code(self):
        snippets_folder = os.path.join(os.getcwd(), 'Snippets')

        # Check if the folder exists
        if not os.path.exists(snippets_folder):
            print(f"Folder '{snippets_folder}' does not exist.")
            return

        # Loop through all files in the folder
        for filename in os.listdir(snippets_folder):
            # Check if the file has a .txt extension
            if filename.endswith('.txt'):
                # Add the file name without extension to the list
                self.snippets_code.append(os.path.splitext(filename)[0])