import tkinter as tk

import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from MainMenu import file_menu
from MainMenu import edit_menu

def cpp_template(textbox, root, statusbar):
    # Textul șablonului
    template_text = """#include <iostream>

int main()
{
    std::cout << "Hello World";
    return 0;
}"""

    # Inserarea textului în textbox
    edit_menu.clear_text(textbox, root, statusbar)
    textbox.insert("1.0", template_text)
    file_menu.create_file(template_text)
    root.redraw()