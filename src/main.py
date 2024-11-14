from PySide6.QtWidgets import QApplication
from GUI import gui
import sys
import threading
from Server.competitive_companion import run_flask_server

if __name__ == "__main__":

    flask_thread = threading.Thread(target=run_flask_server, daemon=True)
    flask_thread.start()

    app = QApplication(sys.argv)
    window = gui.MainView()
    window.show()
    sys.exit(app.exec())