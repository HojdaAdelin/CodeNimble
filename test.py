import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class CodeEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Code Editor with Tabs")
        self.geometry("800x600")

        # Creare Notebook (tab control)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=1, fill='both')

        # Creare bara de meniu
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # Creare meniu File
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New File", command=self.new_file)
        file_menu.add_command(label="Open File", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

    def new_file(self):
        new_tab = ttk.Frame(self.notebook)
        text_widget = tk.Text(new_tab)
        text_widget.pack(expand=1, fill='both')
        self.notebook.add(new_tab, text="Untitled")
    
    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()

            new_tab = ttk.Frame(self.notebook)
            text_widget = tk.Text(new_tab)
            text_widget.insert(tk.END, content)
            text_widget.pack(expand=1, fill='both')
            self.notebook.add(new_tab, text=file_path.split("/")[-1])

if __name__ == "__main__":
    app = CodeEditor()
    app.mainloop()
