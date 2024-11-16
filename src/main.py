from PySide6.QtWidgets import QApplication
from GUI import gui
import sys
import threading
from Server.competitive_companion import run_flask_server

def start_flask_server():
    try:
        flask_thread = threading.Thread(target=run_flask_server, daemon=True)
        flask_thread.start()
        print("Serverul Flask on!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":

    start_flask_server()

    app = QApplication(sys.argv)
    window = gui.MainView()
    window.show()
    sys.exit(app.exec())