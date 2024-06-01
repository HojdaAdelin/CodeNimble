import customtkinter
import os

class TabBar(customtkinter.CTkFrame):
    def __init__(self, master, text_widget,linectn, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.text_widget = text_widget
        self.linectn = linectn
        self.tabs = {}
        self.buttons = []

        # Setați lățimea fixă a frame-ului
        self.configure(height=30)
        self.pack_propagate(False)  # Previne modificarea automată a dimensiunilor frame-ului

    def add_tab(self, file_path):
        if file_path in self.tabs:
            return

        # Obțineți doar numele fișierului
        file_name = os.path.basename(file_path)

        tab_button = customtkinter.CTkButton(
            self, text=file_name, command=lambda: self.show_file_content(file_path), height=30, width=100
        )
        tab_button.pack(side="left", padx=(5, 0), pady=(5, 5))

        self.tabs[file_path] = tab_button
        self.buttons.append(tab_button)

    def show_file_content(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read()

        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("1.0", content)
        self.linectn.redraw()