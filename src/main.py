from PySide6.QtWidgets import QApplication
from GUI import gui
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = gui.MainView()
    window.show()
    sys.exit(app.exec())