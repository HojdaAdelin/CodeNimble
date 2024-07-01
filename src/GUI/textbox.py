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
from MainMenu import file_menu
from GUI import filetab
from Server import server
from Server import client
from MainMenu import run

global ante_font
ante_font = check.get_config_value("zoom")


class ScrollText(tk.Frame):
    def __init__(self, master, status, *args, **kwargs):
        global ante_font
        tk.Frame.__init__(self, *args, **kwargs)
        
        self.statusbar = status
        self.server = None
        self.client = None
        font_size = check.get_config_value("zoom") or 28

        self.gui(font_size)
        self.binding()

    def gui(self, font_size):
        self.text = tk.Text(self, bg="#2b2b2b", foreground="#d1dce8", insertbackground='white',
                            selectbackground="#4d4d4d", font=("Consolas", font_size),
                            undo=True, autoseparators=True, borderwidth=0, wrap="none")
        self.configure(bg="#2b2b2b")
        self.scrollbar = ct.CTkScrollbar(self, orientation=tk.VERTICAL, command=self.text.yview)
        self.scrollhor = ct.CTkScrollbar(self.text, orientation=tk.HORIZONTAL, command=self.text.xview)
        self.text.configure(yscrollcommand=self.scrollbar.set, xscrollcommand=self.scrollhor.set)

        self.numberLines = TextLineNumbers(self, width=4 * font_size, bg='#313335')
        self.numberLines.attach(self.text)

        self.tab_bar = filetab.TabBar(self, self.text, self)
        self.tab_bar.pack(side=tk.TOP, fill="x")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollhor.pack(side=tk.BOTTOM, fill=tk.X)
        self.numberLines.pack(side=tk.LEFT, fill=tk.Y)
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Autocompletare
        
        self.suggestions = tk.Listbox(self, width=25, height=5, font=("", check.get_config_value("zoom")))
        self.suggestions.bind('<Button-1>', self.on_suggestion_click)
        self.suggestions.bind('<FocusOut>', self.hide_suggestions)
        #self.text.bind('<Tab>', self.on_tab)
        self.suggestions.bind("<Escape>", self.hide_suggestions)
        #self.text.bind('<FocusOut>', self.hide_suggestions)  # Hide suggestions when focus is lost
        self.suggestions.bind('<<ListboxSelect>>', self.on_suggestion_select)
        self.suggestions.bind('<Motion>', self.on_mouse_motion)
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

    def binding(self):
        self.text.bind('<Up>', self.on_up_key)
        self.text.bind('<Down>', self.on_down_key)
        self.text.bind("<Key>", self.onPressDelay)
        self.text.bind("<Button-1>", self.numberLines.redraw)
        self.scrollbar.bind("<Button-1>", self.onScrollPress)
        self.text.bind("<MouseWheel>", self.onPressDelay)
        self.text.bind("<KeyRelease>", lambda event: self.redraw())
        self.text.bind("<Tab>", self.add_tab)
        self.text.bind("(", self.insert_parentheses)
        self.text.bind("[", self.insert_brackets)
        self.text.bind("{", self.insert_braces)
        self.text.bind("\"", self.insert_quotation_mark)
        self.text.bind("\'", self.insert_quotation_mark_sp)
        self.text.bind("\*", self.comment_block)
        self.text.bind("<BackSpace>", self.handle_backspace)
        self.text.bind("<Return>", self.handle_return)
        self.text.bind("<Control-BackSpace>", self.handle_ctrl_backspace)
        self.text.bind('<space>', self.hide_suggestions)  # Hide suggestions on space
        self.text.bind("<Escape>", self.hide_suggestions)
        self.text.bind_all('<KeyRelease>', self.on_keyrelease_all)

    def on_up_key(self, event):
        if self.suggestions.winfo_ismapped():
            if self.suggestions.curselection():
                index = self.suggestions.curselection()[0]
                if index > 0:
                    self.suggestions.select_clear(0, tk.END)
                    self.suggestions.select_set(index - 1)
                    self.suggestions.see(index - 1)
                    self.suggestions.focus_set()  # Setează focusul înapoi pe lista de sugestii
            return 'break'
        else:
            return None

    def on_down_key(self, event):
        if self.suggestions.winfo_ismapped():
    
            if self.suggestions.curselection():
                index = self.suggestions.curselection()[0]
                if index < self.suggestions.size() - 1:
                    self.suggestions.select_clear(0, tk.END)
                    self.suggestions.select_set(index + 1)
                    self.suggestions.see(index + 1)
                    self.suggestions.focus_set()  # Setează focusul înapoi pe lista de sugestii
            return 'break'
        else:
            return None

    def on_suggestion_select(self, event):
        selected_index = self.suggestions.curselection()
        if selected_index:
            selected_text = self.suggestions.get(selected_index)
            self.insert_suggestion(selected_text)

    def on_mouse_motion(self, event):
        widget = event.widget
        widget.focus()
        widget.select_clear(0, tk.END)
        widget.select_set(widget.nearest(event.y))

    def on_keyrelease_all(self, event):
        if file_menu.return_file() == ".cpp":
            if event.widget == self.text:
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
            matching_keywords = [kw for kw in self.keywords if kw.startswith(typed_word)]
            if matching_keywords:
                self.show_suggestions(matching_keywords)
            else:
                self.hide_suggestions()
        else:
            self.hide_suggestions()

    def get_current_word(self):
        try:
            cursor_index = self.index(tk.INSERT)
            line_start = self.index(f'{cursor_index} linestart')
            current_line_text = self.get(line_start, cursor_index)
            return current_line_text.split()[-1] if current_line_text else ''
        except IndexError:
            return ''

    def show_suggestions(self, suggestions):
        self.suggestions.delete(0, tk.END)
        for suggestion in suggestions:
            self.suggestions.insert(tk.END, suggestion)
        cursor_index = self.text.index(tk.INSERT)
        cursor_position = self.text.bbox(cursor_index)
        if cursor_position:
            x, y, width, height = cursor_position
            self.suggestions.place(x=x+(4 * int(check.get_config_value("zoom"))), y=y+80+(int(check.get_config_value("zoom"))))
            self.suggestions.select_set(0)

    def hide_suggestions(self, event=None):
        self.suggestions.place_forget()

    def on_suggestion_click(self, event):
        selected_suggestion = self.suggestions.get(tk.ACTIVE)
        if selected_suggestion:
            self.insert_suggestion(selected_suggestion)
        self.hide_suggestions()

    def on_tab(self, event):
        if self.suggestions.size() > 0:
            first_suggestion = self.suggestions.get(0)
            self.insert_suggestion(first_suggestion)
            self.hide_suggestions()
            return 'break'  # This prevents the default behavior of the Tab key
        return None

    def insert_suggestion(self, suggestion):
        current_word = self.get_current_word()
        cursor_index = self.index(tk.INSERT)
        # Calculate the start index of the current word
        start_index = f'{cursor_index} - {len(current_word)}c'
        # Delete the current word
        self.text.delete(start_index, cursor_index)
        # Insert the suggestion
        self.text.insert(cursor_index, suggestion)

    def add_tab(self, event):
        if self.suggestions.size() > 0 and self.suggestions.winfo_ismapped():
            first_suggestion = self.suggestions.get(0)
            self.insert_suggestion(first_suggestion)
            self.hide_suggestions()
            self.text.focus_set()
            return 'break'
        else:
            self.text.insert(tk.INSERT, "    ")
            return 'break'

    def onScrollPress(self, *args):
        self.scrollbar.bind("<B1-Motion>", self.numberLines.redraw)

    def onScrollRelease(self, *args):
        self.scrollbar.unbind("<B1-Motion>", self.numberLines.redraw)

    def onPressDelay(self, *args):
        self.after(2, self.numberLines.redraw)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.text.index(*args, **kwargs)

    def redraw(self):
        global ante_font
        if self.text.tag_ranges(tk.SEL):
            selection_start = self.text.index(tk.SEL_FIRST)
            selection_end = self.text.index(tk.SEL_LAST)
        else:
            selection_start = None
            selection_end = None

        if file_menu.return_file() == ".cpp" or file_menu.return_file() == ".py":
            self.highlight_syntax()
            if file_menu.return_file() == ".cpp":
                self.update_suggestions()
        self.numberLines.redraw()
        self.statusbar.update_stats(self.text)
        font_size = check.get_config_value("zoom")
        if font_size != ante_font:
            ante_font = font_size
            self.text.configure(font=("Consolas", font_size))
            self.suggestions.configure(font=("", font_size))

        if selection_start and selection_end:
            self.text.tag_add(tk.SEL, selection_start, selection_end)

        self.on_text_change()

    def highlight_syntax(self):
        theme = check.get_config_value("theme")
        keyword_colors = self.get_keyword_colors(theme)

        for tag in self.text.tag_names():
            self.text.tag_remove(tag, "1.0", tk.END)

        for keyword_group, color in keyword_colors.items():
            self.text.tag_configure(keyword_group, foreground=color)

        keywords = self.get_keywords()

        # Highlight keywords
        for keyword_group, keyword_list in keywords.items():
            for keyword in keyword_list:
                start_index = "1.0"
                while True:
                    start_index = self.text.search(r'\m{}\M'.format(re.escape(keyword)), start_index, tk.END, regexp=True)
                    if not start_index:
                        break
                    end_index = self.text.index(f"{start_index}+{len(keyword)}c wordend")
                    self.text.tag_add(keyword_group, start_index, end_index)
                    start_index = end_index


        # Highlight special characters individually
        special_characters = self.get_special_characters()
        for char, tag in special_characters.items():
            self.highlight_character(char, tag)

        self.highlight_line_comments()
        self.highlight_block_comments()
        self.highlight_strings()
        self.highlight_quotes()
        self.highlight_include()

    def get_keyword_colors(self, theme):
        dark_theme = {
            "keyword1": "#94193e",  # Cuvinte cheie (ex: int, float, etc.)
            "keyword2": "#1b8ca8",  # Acces specifiers (ex: public, private, etc.)
            "keyword3": "#00b7ff",
            "special_char": "#7eade0",    # Numere și alte cuvinte cheie
            "comment_line": "#008000",  # Comentarii
            "comment_block": "#008000", # Comentarii bloc
            "string": "#008000",    # Șiruri de caractere
            "quote": "#008000",     # Caractere între ghilimele simple
            "include": "#008000",   # Directive include 
        }

        light_theme = {
            "keyword1": "#94193e",
            "keyword2": "#1b8ca8",
            "keyword3": "#00b7ff",
            "special_char": "#7eade0",
            "comment_line": "#008000",
            "comment_block": "#008000",
            "string": "#008000",
            "quote": "#008000",
            "include": "#008000"
        }

        return dark_theme if theme == 0 else light_theme

    def get_keywords(self):
        if file_menu.return_file() == ".cpp":
            return {
                "keyword1": [
                "int", "float", "double", "char", "if", "else", "for", "while", 
                "return", "do", "string", "const", "using", "short", "long", 
                "signed", "unsigned", "bool", "true", "false", "auto", 
                "static", "volatile", "register", "extern", "enum", "typedef",
                "inline", "switch", "case", "default", "goto", "break", "continue",
                "sizeof", "namespace", "new", "delete", "try", "catch", "throw", 
                "nullptr"
                ],

                "keyword2": ["void", "main", "printf", "scanf", "cin", "cout", "endl", "std", 
                "size_t", "ptrdiff_t", "int8_t", "int16_t", "int32_t", "int64_t", 
                "uint8_t", "uint16_t", "uint32_t", "uint64_t", "int_least8_t", 
                "int_least16_t", "int_least32_t", "int_least64_t", "uint_least8_t", 
                "uint_least16_t", "uint_least32_t", "uint_least64_t", "int_fast8_t", 
                "int_fast16_t", "int_fast32_t", "int_fast64_t", "uint_fast8_t", 
                "uint_fast16_t", "uint_fast32_t", "uint_fast64_t", "intptr_t", 
                "uintptr_t", "intmax_t", "uintmax_t"],
                "keyword3": [
                    "class", "public", "private", "protected"
                ]

            }
        elif file_menu.return_file() == ".py":
            return {
                "keyword1": ["False", "None", "True", "and", "as", "assert", "async", "await", "break", "class",
        "continue", "def", "del", "elif", "else", "except", "finally", "for", "from",
        "global", "if", "import", "in", "is", "lambda", "nonlocal", "not", "or", "pass",
        "raise", "return", "try", "while", "with", "yield"],
                "keyword2": ['abs', 'delattr', 'hash', 'memoryview', 'set', 'all', 'dict', 'help', 'min', 'setattr', 'any', 'dir', 'hex',
        'next', 'slice', 'ascii', 'divmod', 'id', 'object', 'sorted', 'bin', 'enumerate', 'input', 'oct', 'staticmethod',
        'bool', 'eval', 'int', 'open', 'str', 'breakpoint', 'exec', 'isinstance', 'ord', 'sum', 'bytearray', 'filter',
        'issubclass', 'pow', 'super', 'bytes', 'float', 'iter', 'print', 'tuple', 'callable', 'format', 'len', 'property',
        'type', 'chr', 'frozenset', 'list', 'range', 'vars', 'classmethod', 'getattr', 'locals', 'repr', 'zip', 'compile',
        'globals', 'map', 'reversed', '__import__', 'complex', 'hasattr', 'max', 'round'],
                "keyword3": ['append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort',
        'capitalize', 'casefold', 'center', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'format_map', 'isalnum',
        'isalpha', 'isascii', 'isdecimal', 'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace',
        'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans', 'partition', 'replace', 'rfind', 'rindex',
        'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title',
        'translate', 'upper', 'zfill']
            }

    def get_special_characters(self):
        return {
            "{": "special_char",
            "}": "special_char",
            "[": "special_char",
            "]": "special_char",
            "(": "special_char",
            ")": "special_char",
            "<": "special_char",
            ">": "special_char",
            "=": "special_char",
            "%": "special_char",
            "+": "special_char",
            "-": "special_char",
            "*": "special_char",
            "!": "special_char",
            ";": "special_char",
            ":": "special_char",
            "0": "keyword3",
            "1": "keyword3", "2": "keyword3", "3": "keyword3", "4": "keyword3", "5": "keyword3", 
            "6": "keyword3", "7": "keyword3", "8": "keyword3", "9": "keyword3"
        }

    def highlight_character(self, character, tag):
        start_index = "1.0"
        while True:
            start_index = self.text.search(re.escape(character), start_index, tk.END, regexp=True)
            if not start_index:
                break
            end_index = self.text.index(f"{start_index}+1c")
            self.text.tag_add(tag, start_index, end_index)
            start_index = end_index

    def highlight_include(self):
        start_index = "1.0"
        while True:
            start_index = self.text.search("#", start_index, tk.END, regexp=True)
            if not start_index:
                break
            end_index = self.text.index(f"{start_index} lineend")
            self.text.tag_add("include", start_index, end_index)
            start_index = end_index

    def highlight_line_comments(self):
        start_index = "1.0"
        while True:
            start_index = self.text.search("//", start_index, tk.END, regexp=True)
            if not start_index:
                break
            end_index = self.text.search("\n", start_index, tk.END, regexp=True)
            if not end_index:
                end_index = self.text.index(tk.END)
            self.text.tag_add("comment_line", start_index, end_index)
            start_index = end_index

    def highlight_block_comments(self):
        start_index = "1.0"
        while True:
            start_index = self.text.search("/\\*", start_index, tk.END, regexp=True)
            if not start_index:
                break
            end_index = self.text.search("\\*/", start_index, tk.END, regexp=True)
            if not end_index:
                end_index = self.text.index(tk.END)
            end_index = self.text.index(f"{end_index}+2c")  # Adjust the end index to include the "*/"
            self.text.tag_add("comment_block", start_index, end_index)
            start_index = end_index + "+1c"


    def highlight_strings(self):
        self.highlight_pattern("\"", "string", "\"", offset=1)

    def highlight_quotes(self):
        self.highlight_pattern("'", "quote", "'", offset=1)

    def highlight_pattern(self, start_pattern, tag, end_pattern, offset=0):
        start_index = "1.0"
        while True:
            start_index = self.text.search(start_pattern, start_index, tk.END, regexp=True)
            if not start_index:
                break
            end_index = self.text.search(end_pattern, f"{start_index}+{offset}c", tk.END, regexp=True)
            if not end_index:
                break
            end_index = self.text.index(f"{end_index}+1c")
            self.text.tag_add(tag, start_index, end_index)
            start_index = end_index

    def insert_quotation_mark(self, event):
        self.text.insert(tk.INSERT, "\"\"")
        self.text.mark_set(tk.INSERT, f"{self.text.index(tk.INSERT)}-1c")
        return "break"
    
    def insert_quotation_mark_sp(self, event):
        self.text.insert(tk.INSERT, "\'\'")
        self.text.mark_set(tk.INSERT, f"{self.text.index(tk.INSERT)}-1c")
        return "break"
    
    def comment_block(self, event):
        self.text.insert(tk.INSERT, "**/")
        self.text.mark_set(tk.INSERT, f"{self.text.index(tk.INSERT)}-2c")
        return "break"
    
    def insert_parentheses(self, event):
        self.text.insert(tk.INSERT, "()")
        self.text.mark_set(tk.INSERT, f"{self.text.index(tk.INSERT)}-1c")
        return "break"

    def insert_brackets(self, event):
        self.text.insert(tk.INSERT, "[]")
        self.text.mark_set(tk.INSERT, f"{self.text.index(tk.INSERT)}-1c")
        return "break"

    def insert_braces(self, event):
        self.text.insert(tk.INSERT, "{}")
        self.text.mark_set(tk.INSERT, f"{self.text.index(tk.INSERT)}-1c")
        return "break"

    def handle_backspace(self, event):
        cursor_index = self.text.index(tk.INSERT)
        previous_char = self.text.get(f"{cursor_index} -1c", cursor_index)
        next_char = self.text.get(cursor_index, f"{cursor_index} +1c")

        if previous_char in "({[\"\'" and next_char in ")}]\"\'":
            if self.text.get(f"{cursor_index} -1c", f"{cursor_index} +1c") in ["()", "{}", "[]", "\"\"", "\'\'"]:
                self.text.delete(f"{cursor_index} -1c", f"{cursor_index} +1c")
                return "break"
        return

    def handle_return(self, event):

        if self.suggestions.size() > 0 and self.suggestions.winfo_ismapped():
            first_suggestion = self.suggestions.get(0)
            self.insert_suggestion(first_suggestion)
            self.hide_suggestions()
            self.text.focus_set()
            return 'break'
        if file_menu.return_file() != ".cpp":
            cursor_index = self.text.index(tk.INSERT)
            current_line = self.text.get(f"{cursor_index} linestart", cursor_index)
            leading_spaces = len(current_line) - len(current_line.lstrip())
            indent = " " * leading_spaces
            self.text.insert(cursor_index, "\n" + indent)
            return "break"
        
        cursor_index = self.text.index(tk.INSERT)
        current_line = self.text.get(f"{cursor_index} linestart", cursor_index)
        
        leading_spaces = len(current_line) - len(current_line.lstrip())
        indent = " " * leading_spaces

        keyword_map = {
            "DO": f"do {{\n{indent}\n{indent}}} while();",
            "FOR": f"for (int i = ; i <= ; i++) {{\n{indent}\n{indent}}}",
            "WHILE": f"while () {{\n{indent}\n{indent}}}",
            "IF": f"if () {{\n{indent}\n{indent}}}",
            "INT": f"int () {{\n{indent}\n{indent}}}",
            "VOID": f"void () {{\n{indent}\n{indent}}}",
            "LONG": f"long long () {{\n{indent}\n{indent}}}",
            "CPP": """#include <iostream>

int main()
{
    std::cout << "Hello World";
    return 0;
}""" 
        }

        stripped_line = current_line.strip()
        if stripped_line in keyword_map:
            self.text.delete(f"{cursor_index} linestart", cursor_index)
            self.text.insert(f"{cursor_index} linestart", indent + keyword_map[stripped_line])
            new_cursor_index = self.get_new_cursor_index(stripped_line, cursor_index, indent)
            self.text.mark_set(tk.INSERT, new_cursor_index)
            return "break"

        previous_char = self.text.get(cursor_index + "-1c")
        next_char = self.text.get(cursor_index)

        if previous_char == "{" and next_char == "}":
            self.text.insert(cursor_index, "\n" + indent + "    \n" + indent)
            self.text.mark_set(tk.INSERT, f"{cursor_index} + {len(indent) + 5}c")
            return "break"

        self.text.insert(cursor_index, "\n" + indent)
        
        return "break"

    def get_new_cursor_index(self, keyword, cursor_index, indent):
        line_index = self.text.index(cursor_index + "linestart")
        if keyword == "DO":
            while_pos = self.text.search("while();", line_index, tk.END)
            if while_pos:
                return f"{while_pos} - 1c"
        elif keyword == "FOR":
            for_pos = self.text.search("for (int i = ", line_index, tk.END)
            if for_pos:
                return f"{for_pos} + 13c"
        elif keyword == "WHILE":
            while_pos = self.text.search("while ()", line_index, tk.END)
            if while_pos:
                return f"{while_pos} + 7c"
        elif keyword == "IF":
            if_pos = self.text.search("if ()", line_index, tk.END)
            if if_pos:
                return f"{if_pos} + 4c"
        elif keyword in ["INT", "VOID", "LONG"]:
            func_pos = self.text.search(f"{keyword.lower()} ()", line_index, tk.END)
            if func_pos:
                return f"{func_pos} + {len(keyword) + 1}c"
        return cursor_index

    def handle_ctrl_backspace(self, event):
        cursor_index = self.text.index(tk.INSERT)
        line_start = self.text.index(f"{cursor_index} linestart")
        text_before_cursor = self.text.get(line_start, cursor_index)
        
        if not text_before_cursor:
            return "break"
        
        # Împărțim textul în cuvinte și spații
        segments = re.findall(r'\S+|\s+', text_before_cursor)
        
        if segments[-1].isspace():
            # Dacă ultimul segment este spațiu, îl ștergem
            spaces_to_delete = len(segments[-1])
            self.text.delete(f"{cursor_index} - {spaces_to_delete}c", cursor_index)
        else:
            # Dacă ultimul segment este un cuvânt, îl ștergem
            word_to_delete = len(segments[-1])
            self.text.delete(f"{cursor_index} - {word_to_delete}c", cursor_index)
        
        return "break"

    def profile_bool(self):
        if os.path.exists("profile.txt"):
            with open("profile.txt", "r") as file:
                content = file.read().strip()
                if content.startswith('name: "'):
                    profile_name = content[7:-1]
                    if profile_name:
                        return True
        return False

    def get_profile_name(self):
        if os.path.exists("profile.txt"):
            with open("profile.txt", "r") as file:
                content = file.read().strip()
                if content.startswith('name: "'):
                    profile_name = content[7:-1]
                    return profile_name

    def start_server(self):
        if not self.profile_bool():
            messagebox.showinfo("Info", "You need to complete the profile first!")
            return
        if self.server:
            messagebox.showinfo("Info", "Server already created!")
            return
        if self.client:
            messagebox.showinfo("Info", "Client already connected to a server!")
            return
        self.server = server.Server()
        server_thread = threading.Thread(target=self.server.start)
        server_thread.daemon = True
        server_thread.start()
        self.start_client()

    def start_client(self):
        if not self.profile_bool():
            messagebox.showinfo("Info", "You need to complete the profile first!")
            return
        if self.client:
            messagebox.showinfo("Info", "Client already connected!")
            return
        client_name = self.get_profile_name()
        self.client = client.Client(client_name=client_name)
        receive_thread = threading.Thread(target=self.client.receive_messages, args=(self.display_message,))
        receive_thread.daemon = True
        receive_thread.start()

    def disconnect_client(self):
        if self.client:
            self.client.disconnect()
            self.client = None
            messagebox.showinfo("Info", "Disconnected successfully!")

    def on_text_change(self):
        message = self.text.get(1.0, tk.END)
        if self.client:
            self.client.send_message(message)

    def display_message(self, message):
        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.INSERT, message)
        self.text.config(state=tk.NORMAL)

class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs, highlightthickness=0)
        self.textwidget = None
        self.font_size = check.get_config_value("zoom")
        self.text_color = "#606366"

    def attach(self, text_widget):
        self.textwidget = text_widget
    
    def redraw(self, *args):
        self.delete("all")
        self.font_size = check.get_config_value("zoom")
        self.font = ("Consolas", self.font_size)
        self.configure(width=4 * int(self.font_size))
        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, fill=self.text_color, font=self.font)
            i = self.textwidget.index(f"{i}+1line")