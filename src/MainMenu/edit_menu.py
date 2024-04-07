import tkinter as tk

def undo_text(widget, root):
    try:
        widget.edit_undo()
        root.redraw()
    except tk.TclError:
        pass

def redo_text(widget, root):
    try:
        widget.edit_redo()
        root.redraw()
    except tk.TclError:
        pass

def copy_text(text, root):
    selected_text = text.get(tk.SEL_FIRST, tk.SEL_LAST)
    text.clipboard_clear()
    text.clipboard_append(selected_text)
    root.redraw()

def paste_text(text, root):
    clipboard_text = text.clipboard_get()
    text.insert(tk.INSERT, clipboard_text)
    root.redraw()

def cut_text(text, root):
    copy_text(text, root)
    text.delete(tk.SEL_FIRST, tk.SEL_LAST)
    root.redraw()

def delete_text(text, root):
    try:
        start_index = text.index(tk.SEL_FIRST)
        end_index = text.index(tk.SEL_LAST)
        text.delete(start_index, end_index)
        root.redraw()
    except tk.TclError:
        pass

def select_all(text):
    pass