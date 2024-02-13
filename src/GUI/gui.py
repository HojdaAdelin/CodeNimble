import customtkinter as ct
from ctypes import byref, sizeof, c_int, windll

class MainWindow(ct.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("CodeNimble")
        HWND = windll.user32.GetParent(self.winfo_id())
        tb_color = 0x333333
        windll.dwmapi.DwmSetWindowAttribute(
            HWND,
            35,
            byref(c_int(tb_color)),
            sizeof(c_int))

if __name__ == "__main__":
    window = MainWindow()
    window.geometry("1200x700")
    window.mainloop()
