from GUI.gui import *
from GUI.textbox import *
import customtkinter as ct

if __name__ == "__main__":
    window = MainWindow()
    main_frame = ct.CTkFrame(window)
    main_frame.pack(fill="both", expand=True)
    text = TextBox(main_frame)
    text.bind("<KeyRelease>", text.update_line_numbers)
    window.mainloop()
