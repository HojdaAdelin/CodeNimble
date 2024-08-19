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
from Core import view_menu
from Core import file_menu
from GUI import filetab
from Server import server
from Server import client
from Core import run
from Core import themes
from Server import password_handle
from GUI import terminal
from GUI import suggestions

global ante_font
ante_font = check.get_config_value("zoom")

class ScrollText(tk.Frame):
    def __init__(self, master, status, *args, **kwargs):
        global ante_font
        tk.Frame.__init__(self, *args, **kwargs)
        
        self.master = master
        self.statusbar = status
        self.server = None
        self.client = None
        self.password = None
        self.COLORS = {}
        font_size = check.get_config_value("zoom") or 28
        self.specific_patterns()
        self.gui(font_size)
        self.configure_tags()
        self.binding()

    def manipulate_gui(self, type):
        if type == "hide":
            self.terminal.pack_forget()
            self.tab_bar.pack_forget()
            self.tab_bar.pack_forget()
            self.scrollbar.pack_forget()
            self.scrollhor.pack_forget()
            self.numberLines.pack_forget()
            self.text.pack_forget()
        elif type == "show":
            self.terminal.pack(side=tk.BOTTOM, fill=tk.X)
            self.tab_bar.pack(side=tk.TOP, fill="x")
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.scrollhor.pack(side=tk.BOTTOM, fill=tk.X)
            self.numberLines.pack(side=tk.LEFT, fill=tk.Y)
            self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

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

        self.terminal = terminal.Terminal(self)

        self.tab_bar = filetab.TabBar(self, self.text, self)
        self.tab_bar.pack(side=tk.TOP, fill="x")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollhor.pack(side=tk.BOTTOM, fill=tk.X)
        self.numberLines.pack(side=tk.LEFT, fill=tk.Y)
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.suggestions = suggestions.Suggestions(self, self)

    def binding(self):
        self.text.bind('<Up>', self.suggestions.on_up_key)
        self.text.bind('<Down>', self.suggestions.on_down_key)
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
        self.text.bind('<space>', self.suggestions.hide_suggestions)  # Hide suggestions on space
        self.text.bind("<Escape>", self.suggestions.hide_suggestions)
        self.text.bind_all('<KeyRelease>', self.suggestions.on_keyrelease_all)
        self.text.bind('<<Modified>>', self.suggestions.on_text_modified)
        self.text.bind("<Control-Button-4>", view_menu.zoom_in(self))
        self.text.bind("<Control-Button-5>", view_menu.zoom_out(self))
        self.text.bind("<Control-`>", self.handle_terminal)

    def handle_terminal(self, event=None):
        
        if self.terminal.return_height() == 150:
            self.terminal.update_height(0)
            self.terminal.pack_forget()
        else:
            self.terminal.update_height(150)
            self.manipulate_gui("hide")
            self.manipulate_gui("show")

    def add_tab(self, event):
        if self.suggestions.handle_case() == True:
            self.suggestions.handle_tab()
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
        """
        if self.text.tag_ranges(tk.SEL):
            selection_start = self.text.index(tk.SEL_FIRST)
            selection_end = self.text.index(tk.SEL_LAST)
        else:
            selection_start = None
            selection_end = None
        """

        if file_menu.return_file() == ".cpp" or file_menu.return_file() == ".py":
            self.highlight_syntax()
            self.suggestions.update_suggestions()
        self.numberLines.redraw()
        self.statusbar.update_stats(self.text)
        font_size = check.get_config_value("zoom")
        if font_size != ante_font:
            ante_font = font_size
            self.text.configure(font=("Consolas", font_size))
            self.suggestions.suggestions_text.configure(font=("", font_size))
            self.suggestions.tags_text.configure(font=("", font_size))

        #if selection_start and selection_end:
            #self.text.tag_add(tk.SEL, selection_start, selection_end)

        self.on_text_change()

    def specific_patterns(self):
        self.PATTERNS = {
            "for": r"\bfor\b",
            "do": r"\bdo\b",
            "while": r"\bwhile\b",
            "if": r"\bif\b",
            "else": r"\belse\b",
            "int": r"\bint\b",
            "return": r"\breturn\b",
            "long": r"\blong\b",
            "short": r"\bshort\b",
            "unsigned": r"\bunsigned\b",
            "string": r"\bstring\b",
            "float": r"\bfloat\b",
            "double": r"\bdouble\b",
            "static": r"\bstatic\b",
            "bool": r"\bbool\b",
            "true": r"\btrue\b",
            "false": r"\bfalse\b",
            "cout": r"\bcout\b",
            "cin": r"\bcin\b",
            "std": r"\bstd\b",
            "paren": r"[\(\)\[\]\{\}]",
            "number": r"\b\d+\b",
            "arrow_right": r"<",
            "arrow_left": r">",
            "colon": r":",
            "semicolon": r";",
            "question": r"\?",
            "excl": r"!",
            "pointer": r"&",
            "equal": r"=",
            "include": r"#include\s+[\"<]\S+[\">]",
            "comment": r"//.*",
            "string_double": r"\".*?\"",
            "string_single": r"'.*?'",
        }
    
    def colors(self, color_pal):
        self.COLORS = color_pal
        self.configure_tags()
        
    def configure_tags(self):
        for tag, color in self.COLORS.items():
            self.text.tag_configure(tag, foreground=color)

    def highlight_syntax(self):
        text_widget = self.text
        line_start = text_widget.index("insert linestart")
        line_end = text_widget.index("insert lineend")

        line_text = text_widget.get(line_start, line_end)
        line_number = int(line_start.split('.')[0])

        # Șterge toate etichetele pentru linia curentă
        for tag in self.COLORS.keys():
            text_widget.tag_remove(tag, line_start, line_end)

        # Aplică noile etichete
        for tag, pattern in self.PATTERNS.items():
            for match in re.finditer(pattern, line_text):
                start_index = f"{line_number}.{match.start()}"
                end_index = f"{line_number}.{match.end()}"
                text_widget.tag_add(tag, start_index, end_index)

    def highlight_all(self):
        if file_menu.return_file() == ".cpp" or file_menu.return_file() == ".py":
            for tag in self.COLORS.keys():
                self.text.tag_remove(tag, "1.0", tk.END)
            
            # Re-evidențiază întregul text
            text_content = self.text.get("1.0", tk.END)
            lines = text_content.splitlines()
            for line_number, line_text in enumerate(lines, start=1):
                for tag, pattern in self.PATTERNS.items():
                    for match in re.finditer(pattern, line_text):
                        start_index = f"{line_number}.{match.start()}"
                        end_index = f"{line_number}.{match.end()}"
                        self.text.tag_add(tag, start_index, end_index)

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

        if self.suggestions.handle_case() == True:
            self.suggestions.handle_enter()
            return "break"
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
            self.terminal.notification("[Info]: You need to complete the profile before to start the server!")
            return
        if self.server:
            self.terminal.notification("[Info]: Server already created!")
            return
        if self.client:
            self.terminal.notification("[Info]: Client already connected to a server!")
            return
        server_handle = password_handle.PasswordHandle(self)
        server_handle.mainloop()
        if self.password:
            self.server = server.Server(password=self.password, app=self)
            server_thread = threading.Thread(target=self.server.start)
            server_thread.daemon = True
            server_thread.start()
            self.start_client()
            self.statusbar.update_server("host")
            self.terminal.notification("[Server]: Started")

    def start_client(self):
        if not self.profile_bool():
            self.terminal.notification("[Info]: You need to complete the profile before join a local server!")
            return
        if self.client:
            self.terminal.notification("[Info]: Client already connected!")
            return
        if self.password is None:
            server_handle = password_handle.PasswordHandle(self)
            server_handle.mainloop()
        if self.password:
            client_name = self.get_profile_name()
            self.client = client.Client(self, client_name=client_name, password=self.password)
            if self.client.is_connected():
                receive_thread = threading.Thread(target=self.client.receive_messages, args=(self.display_message,))
                receive_thread.daemon = True
                receive_thread.start()
                self.statusbar.update_server("client")
            else:
                self.client = None
                self.password = None
                self.statusbar.update_server("none")
    
    def disconnect_client(self):
        if self.client:
            self.client.disconnect()
            self.client = None
            self.terminal.notification("[Info]: Disconnected successfully!")
            self.statusbar.update_server("none")

    def on_text_change(self):
        message = self.text.get(1.0, tk.END)
        if self.client and self.client.is_connected():
            self.client.send_message(message)

    def display_message(self, message):
        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.INSERT, message)
        self.text.config(state=tk.NORMAL)

    def get_client(self):
        return self.client
    def get_server(self):
        return self.server
    def server_password(self, password):
        self.password = password

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