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
    statusbar.update_text("Used C++ template")
    root.redraw()
