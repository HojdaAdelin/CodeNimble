from PySide6.QtWidgets import (
    QWidget, QLabel, QTextEdit, QPushButton, QGridLayout, QSizePolicy, QStackedWidget, QPlainTextEdit, QVBoxLayout, QLineEdit, QFrame, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt
import threading 
import json
from GUI import fetch_window
from GUI import diff
from Server import server
from Server import client

class RightPanel(QWidget):
    def __init__(self, theme,win, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.win = win
        self.theme = theme
        self.server = None
        self.client = None
        # Crearea layout-ului principal
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        
        # Crearea butoanelor de taburi
        self.tab_buttons = QWidget()
        self.tab_buttons_layout = QGridLayout(self.tab_buttons)
        self.main_layout.addWidget(self.tab_buttons)
        
        self.testing_button = QPushButton("Testing", self, clicked=self.show_testing_tab)
        self.server_button = QPushButton("Server", self, clicked=self.show_server_tab)
        
        self.tab_buttons_layout.addWidget(self.testing_button, 0, 0)
        self.tab_buttons_layout.addWidget(self.server_button, 0, 1)
        
        # Crearea QStackedWidget pentru a comuta între tab-uri
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)
        
        # Crearea tab-ului „Testing”
        self.testing_widget = QWidget()
        self.testing_layout = QGridLayout(self.testing_widget)
        self.testing_widget.setLayout(self.testing_layout)
        
        self.layout = self.testing_layout
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        
        self.layout.setColumnStretch(0, 1)
        self.layout.setRowStretch(0, 0)
        self.layout.setRowStretch(1, 1)
        self.layout.setRowStretch(2, 0)
        self.layout.setRowStretch(3, 1)
        self.layout.setRowStretch(4, 0)
        self.layout.setRowStretch(5, 1)
        self.layout.setRowStretch(6, 0)
        self.layout.setRowStretch(7, 0)

        # Label-ul pentru input
        self.input_label = QLabel("Input", self)
        self.layout.addWidget(self.input_label, 0, 0, Qt.AlignHCenter)

        # Textbox pentru input
        self.input_box = QTextEdit(self)
        self.input_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.layout.addWidget(self.input_box, 1, 0)

        # Label-ul pentru output
        self.output_label = QLabel("Output", self)
        self.layout.addWidget(self.output_label, 2, 0, Qt.AlignHCenter)

        # Textbox pentru output
        self.output_box = QTextEdit(self)
        self.output_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.output_box, 3, 0)

        # Label-ul pentru expected output
        self.expected_label = QLabel("Expected Output", self)
        self.layout.addWidget(self.expected_label, 4, 0, Qt.AlignHCenter)

        # Textbox pentru expected output
        self.expected_box = QTextEdit(self)
        self.expected_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.layout.addWidget(self.expected_box, 5, 0)

        # Butonul pentru comparare
        self.diff = QPushButton("Output comparator", self, clicked=self.diff_core)
        self.diff.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.addWidget(self.diff, 6, 0)

        # Butonul pentru fetch
        self.fetch = QPushButton("Fetch test cases", self, clicked=self.fetch_core)
        self.fetch.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.addWidget(self.fetch, 7, 0)

        # Adăugăm widget-ul „Testing” în stacked_widget
        self.stacked_widget.addWidget(self.testing_widget)
        
        # Crearea tab-ului „Server”
        self.server_widget = QWidget()
        self.server_layout = QVBoxLayout(self.server_widget)
        self.server_widget.setLayout(self.server_layout)
        # Separator pentru grupul de butonae
        self.separator = QFrame(self)
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.server_layout.addWidget(self.separator)
        # Password
        self.password_entry = QLineEdit(self)
        self.password_entry.setPlaceholderText("Password")
        self.server_layout.addWidget(self.password_entry)
        # Start server
        self.start_server = QPushButton("Start server", self)
        self.server_layout.addWidget(self.start_server)
        self.start_server.clicked.connect(self.start_server_option)
        # Crearea unui layout pentru butoanele „Connect” și „Disconnect”
        self.connect_buttons = QWidget()
        self.connect_buttons_layout = QHBoxLayout(self.connect_buttons)
        self.connect_button = QPushButton("Connect", self)
        self.connect_button.clicked.connect(self.connect_to_server)
        self.disconnect_button = QPushButton("Disconnect", self)
        self.disconnect_button.clicked.connect(self.disconnect_from_server)
        
        self.connect_buttons_layout.addWidget(self.connect_button)
        self.connect_buttons_layout.addWidget(self.disconnect_button)
        
        self.server_layout.addWidget(self.connect_buttons)

        # QPlainTextEdit pentru Server
        self.server_textbox = QPlainTextEdit(self)
        self.server_textbox.setReadOnly(True)
        self.server_textbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.server_layout.addWidget(self.server_textbox)
        
        # Entry între butonul „Send” și „QPlainTextEdit”
        self.entry = QLineEdit(self)
        self.server_layout.addWidget(self.entry)

        # Butonul „Send”
        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.server_layout.addWidget(self.send_button)
        
        # Adăugăm widget-ul „Server” în stacked_widget
        self.stacked_widget.addWidget(self.server_widget)
        
        # Aplicarea temei
        self.apply_theme(self.theme)
        with open('config.json', 'r') as file:
            self.config = json.load(file)
        self.user_name = self.config.get('profile_name')

    def start_server_option(self):
        if self.password_entry.text() == "":
            QMessageBox.information(self, "Info", "You need to enter the password!")
            return
        self.server = server.ServerManager(password=self.password_entry.text())
        
        def start_server_thread():
            try:
                self.server.start_server()
            except Exception as e:
                print(f"Eroare la pornirea serverului: {e}")
                return
        
        # Pornim serverul pe un thread separat
        server_thread = threading.Thread(target=start_server_thread)
        server_thread.daemon = True  # Asigură-te că thread-ul se închide odată cu aplicația
        server_thread.start()

        if not self.client:
            self.client = client.ClientManager(name=self.user_name, password=self.password_entry.text(), gui=self)
            self.client.connect_to_server()
            self.win.status_bar.update_server("connected")


    def connect_to_server(self):
        if self.password_entry.text() == "":
            QMessageBox.information(self, "Info", "You need to enter the password!")
            return
        if self.client:
            QMessageBox.information(self,"Info", "Already connected to the server.")
        else:
            self.client = client.ClientManager(name=self.user_name, password=self.password_entry.text(), gui=self)
            self.win.status_bar.update_server("connected")
            if not self.client.connect_to_server():  
                QMessageBox.critical(self, "Error", "Server error or wrong password!")
                self.client = None
                self.win.status_bar.update_server("none")

            
    def disconnect_from_server(self):
        if self.client:
            self.client.disconnect()
            self.client = None
            self.win.status_bar.update_server("none")

    def send_message(self):
        message = self.entry.text()
        if message and self.client:
            self.client.send_message(message)
            self.entry.clear()
            self.append_to_textbox(f"You: {message}")

    def append_to_textbox(self, message):
        self.server_textbox.appendPlainText(message)

    def show_testing_tab(self):
        self.stacked_widget.setCurrentWidget(self.testing_widget)

    def show_server_tab(self):
        self.stacked_widget.setCurrentWidget(self.server_widget)

    def diff_core(self):
        self.diff_win = diff.OutputComparator(self, self.theme)
        self.diff_win.show()

    def fetch_core(self):
        self.fetch_win = fetch_window.FetchWindow(self, self.theme)
        self.fetch_win.show()

    def apply_theme(self, theme):
        self.setStyleSheet(f"""
            background-color: {theme.get("background_color")};
            color: {theme.get("text_color")};
        """)

        self.input_label.setStyleSheet(f"color: {theme.get('text_color')};")
        self.output_label.setStyleSheet(f"color: {theme.get('text_color')};")
        self.expected_label.setStyleSheet(f"color: {theme.get('text_color')};")
        self.separator.setStyleSheet(f"background-color: {theme.get('separator_color')};")
        self.input_box.setStyleSheet(f"""
            background-color: {theme.get("editor_background")};
            color: {theme.get("editor_foreground")};
            border: 1px solid {theme.get("border_color")};
            padding: 5px;
        """)
        self.output_box.setStyleSheet(f"""
            background-color: {theme.get("editor_background")};
            color: {theme.get("editor_foreground")};
            border: 1px solid {theme.get("border_color")};
            padding: 5px;
        """)
        self.server_textbox.setStyleSheet(f"""
            background-color: {theme.get("editor_background")};
        """)
        self.expected_box.setStyleSheet(f"""
            background-color: {theme.get("editor_background")};
            color: {theme.get("editor_foreground")};
            border: 1px solid {theme.get("border_color")};
            padding: 5px;
        """)
        self.entry.setStyleSheet(f"""
            background-color: {theme.get("editor_background")};
            color: {theme.get("editor_foreground")};
            border: 1px solid {theme.get("border_color")};
            padding: 5px;
        """)
        self.password_entry.setStyleSheet(f"""
            background-color: {theme.get("editor_background")};
            color: {theme.get("editor_foreground")};
            border: 1px solid {theme.get("border_color")};
            padding: 5px;
        """)

        button_style = f"""
            QPushButton {{
                background-color: {theme.get("button_color")};
                color: {theme.get("text_color")};
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: {theme.get("button_hover_color")};
            }}
        """
        self.diff.setStyleSheet(button_style)
        self.fetch.setStyleSheet(button_style)
        self.send_button.setStyleSheet(button_style)
        self.testing_button.setStyleSheet(button_style)
        self.server_button.setStyleSheet(button_style)
        self.connect_button.setStyleSheet(button_style)
        self.disconnect_button.setStyleSheet(button_style)
        self.start_server.setStyleSheet(button_style)
