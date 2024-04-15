import tkinter as tk
import customtkinter as ctk

find_window_opened = False

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
    text.tag_add(tk.SEL, "1.0", tk.END)
    text.mark_set(tk.INSERT, "1.0")
    text.see(tk.INSERT)

def find_text(scroll_text):
    global find_window_opened

    if not find_window_opened:
        find_window_opened = True
        find_window = ctk.CTk()
        find_window.title("CodeNimble - Find Text")

        w = 300 
        h = 100 

        ws = find_window.winfo_screenwidth()
        hs = find_window.winfo_screenheight()

        x = (ws/2+500) - (w/2)
        y = (hs/2+200) - (h/2)

        find_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        find_window.resizable(False, False)
        find_window.iconbitmap("images/logo.ico")
        find_window.configure(fg_color = "#2b2b2b")

        # Adaugă un Entry în fereastra find_window
        text_box = tk.Entry(find_window, width=25, font=("Arial", 30), bg='#4a4a4a', foreground="#d1dce8", 
                            insertbackground='white',
                            selectbackground="#616161", borderwidth=0)
        text_box.pack(pady=40)

        def find():
            search_text = text_box.get().strip()
            if search_text:
                start_index = "1.0"
                while True:
                    start_index = scroll_text.search(search_text, start_index, tk.END)
                    if not start_index:
                        break
                    end_index = f"{start_index}+{len(search_text)}c"
                    scroll_text.tag_add("found", start_index, end_index)
                    scroll_text.tag_configure("found", background="gray")
                    start_index = end_index
        
        # Adaugă un buton "Find" pentru a găsi textul
        find_button = ctk.CTkButton(find_window, text="Find", command=find)
        find_button.pack()

        # Funcție pentru a reseta find_window_opened la False după ce închidem fereastra
        def on_closing():
            global find_window_opened
            find_window_opened = False
            find_window.destroy()

        find_window.protocol("WM_DELETE_WINDOW", on_closing)
        find_window.mainloop()



def replace_text(text):
    pass