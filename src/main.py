from GUI.gui import *
from Config.check import *

if __name__ == "__main__":
    config = check_config_file()
    if (config == False):
        create_config_file()
        pre_write_config()

    window = MainWindow()
    window.mainloop()
