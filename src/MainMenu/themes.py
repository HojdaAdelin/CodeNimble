import tkinter as tk
import customtkinter as ct
from ctypes import byref, sizeof, c_int, windll
import json
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from Config import check

def find_theme_color(init, widget):
    path = f"Themes/{init}"
    
    try:
        with open(path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise ValueError(f"File {path} not found")
    
    if widget in data:
        return data[widget]
    else:
        raise ValueError(f"Widget {widget} not found in {path}")

def use_theme(init, menu_bar, cascade1, cascade2, cascade3, cascade4, cascade5, cascade6, cascade7, drop1, drop2, drop3, drop4, drop5, drop6, drop7, status, text, win, tree, tree_menu, tree_foldermenu, tab_bar):
    widgets = {
        'menu_bar': menu_bar,
        'cascade1': cascade1,
        'cascade2': cascade2,
        'cascade3': cascade3,
        'cascade4': cascade4,
        'cascade5': cascade5,
        'cascade6': cascade6,
        'cascade7': cascade7,
        'drop1': drop1,
        'drop2': drop2,
        'drop3': drop3,
        'drop4': drop4,
        'drop5': drop5,
        'drop6': drop6,
        'drop7': drop7,
        'status': status,
        'text': text,
        'win': win,
        'tree': tree,
        'tree_menu': tree_menu,
        'tree_foldermenu': tree_foldermenu,
        'tab_bar': tab_bar
    }
    misc = init
    init += ".json"
    with open(f"Themes/{init}", 'r') as file:
        config = json.load(file)
        
    # Convert title_bar_color from string to integer
    title_bar_color = int(config['title_bar_color'], 16)
        
        # Apply the title bar color
    HWND = windll.user32.GetParent(win.winfo_id())
    windll.dwmapi.DwmSetWindowAttribute(
        HWND,
        35,
        byref(c_int(title_bar_color)),
        sizeof(c_int))

    for widget_name, widget in widgets.items():
        try:
            config = find_theme_color(init, widget_name)
            if widget_name == 'status':
                widget.configure(bg=config['bg'])
                widget.status_label.configure(bg=config['status_label']['bg'], fg=config['status_label']['fg'])
                widget.num_stats_label.configure(bg=config['num_stats_label']['bg'], fg=config['num_stats_label']['fg'])
                widget.run_img.configure(bg=config['run_img']['bg'])
                widget.server_status.configure(bg=config['server_status']['bg'], fg=config['server_status']['fg'])
                widget.set_color(config['set_color'])
                widget.set_based_color(config['set_based_color'])
                widget.timer.configure(bg=config['timer']['bg'], fg=config['timer']['fg'])
                widget.timer_frame.configure(bg=config['timer_frame']['bg'])
            elif widget_name == 'text':
                widget.text.configure(bg=config['text']['bg'], foreground=config['text']['foreground'],
                                      insertbackground=config['text']['insertbackground'],
                                      selectbackground=config['text']['selectbackground'])
                widget.scrollbar.configure(fg_color=config['scrollbar']['fg_color'], button_color=config['scrollbar']['button_color'],
                                           button_hover_color=config['scrollbar']['button_hover_color'])
                widget.scrollhor.configure(fg_color=config['scrollhor']['fg_color'], button_color=config['scrollhor']['button_color'],
                                           button_hover_color=config['scrollhor']['button_hover_color'])
                widget.numberLines.configure(bg=config['numberLines']['bg'])
                widget.suggestions.configure(bg=config['suggestions']['bg'], fg=config['suggestions']['fg'],
                                             selectbackground=config['suggestions']['selectbackground'],
                                             selectforeground=config['suggestions']['selectforeground'])
                widget.terminal.configure(fg_color=config['terminal']['fg_color'], bg_color=config['terminal']['bg_color'])
                widget.terminal.textbox.configure(fg_color=config['terminal']['textbox_color'], text_color=config['terminal']['text_color'])
            elif widget_name == 'tree':
                widget.configure(fg_color=config['fg_color'])
                widget.treestyle.configure("Treeview",
                                           background=config['treestyle']['Treeview']['background'],
                                           fieldbackground=config['treestyle']['Treeview']['fieldbackground'],
                                           foreground=config['treestyle']['Treeview']['foreground'],
                                           bordercolor=config['treestyle']['Treeview']['bordercolor'])
                widget.treestyle.map('Treeview',
                                     background=[('selected', config['treestyle']['Treeview_map']['background'][0][1])],
                                     foreground=[('selected', config['treestyle']['Treeview_map']['foreground'][0][1])])
                widget.input_label.configure(text_color=config['input_label']['text_color'])
                widget.output_label.configure(text_color=config['output_label']['text_color'])
                widget.input.configure(fg_color=config['input']['fg_color'], text_color=config['input']['text_color'])
                widget.output.configure(fg_color=config['output']['fg_color'], text_color=config['output']['text_color'])
            else:
                widget.configure(**config)
        except ValueError as e:
            print(f"Warning: {e}")
        except Exception as e:
            print(f"Error configuring {widget_name}: {e}")
    check.update_config_file("theme", misc)
def title_bar_color_handle(win):
        current_theme = check.get_config_value("theme") + ".json"
        with open(f"Themes/{current_theme}", 'r') as file:
                config = json.load(file)
        
        # Convert title_bar_color from string to integer
        title_bar_color = int(config['title_bar_color'], 16)
                
                # Apply the title bar color
        HWND = windll.user32.GetParent(win.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(
                HWND,
                35,
                byref(c_int(title_bar_color)),
                sizeof(c_int))
        
def return_default_win_color(init):
    theme = "Themes/" + init + ".json"
    
    with open(theme, 'r') as file:
        data = json.load(file)
        
    default_window = data.get("default_window", {})
    fg_color = default_window.get("fg_color")
    text_bg = default_window.get("text_bg")
    text = default_window.get("text")
    hover_color = default_window.get("hover_color")
    
    return fg_color, text_bg, text, hover_color
