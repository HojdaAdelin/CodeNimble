import tkinter as tk

import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from MainMenu import file_menu
from MainMenu import edit_menu

cpp_text = """#include <iostream>

int main()
{
    std::cout << "Hello World";
    return 0;
}"""

c_text = """#include <stdio.h>

int main()
{
    printf("Hello World");

    return 0;
}"""

java_text = """public class Main
{
	public static void main(String[] args) {
		System.out.println("Hello World");
	}
}"""

html_text = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    
</body>
</html>"""

competitive_text = """#include <bits/stdc++.h>

using namespace std;

#define ll long long

void solution() {
    
}

int main()
{
    solution();

    return 0;
}"""

def create_template(textbox, root, statusbar, op):
    template_text = """"""
    ext = ""
    ext_misc = ""
    if (op == "cpp"):
        template_text = cpp_text
        ext_misc = "C++"
        ext = ".cpp"
    elif (op == "c"):
        template_text = c_text
        ext_misc = "C"
        ext = ".c"
    elif (op == "java"):
        template_text = java_text
        ext_misc = "Java"
        ext = ".java"
    elif (op == "html"):
        template_text = html_text
        ext_misc = "HTML"
        ext = ".html"
    elif (op == "com"):
        template_text = competitive_text
        ext_misc = "C++ Competitive"
        ext = ".cpp"
    # Inserarea textului în textbox
    edit_menu.clear_text(textbox, root, statusbar)
    textbox.insert("1.0", template_text)
    file_menu.create_file(template_text, ext)
    statusbar.update_text("Used " + ext_misc + " template")
    root.redraw()
    root.tab_bar.add_tab(file_menu.current_file())