from PySide6.QtWidgets import (
    QWidget, QLabel, QTextEdit, QPushButton, QGridLayout, QSizePolicy, QStackedWidget, QPlainTextEdit, QVBoxLayout, QLineEdit, QFrame, QHBoxLayout, QMessageBox, QComboBox, QSpacerItem
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import threading 
import json
from GUI import fetch_window
from GUI import diff
from Server import server
from Server import client
from Tools import pbinfo

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

        self.functions = QComboBox(self)
        self.functions.addItems(["Testing","Submit code", "Documentation", "Server"])
        self.functions.setItemText
        self.functions.currentIndexChanged.connect(self.toggle_tabs)
        self.main_layout.addWidget(self.functions)
        
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

        # Documentation
        self.documentation_widget = QWidget()
        self.documenation_layout = QVBoxLayout(self.documentation_widget)
        self.documentation_widget.setLayout(self.documenation_layout)

        self.documentation_title = QLabel("Documentation", self)
        self.documentation_title.setFont(QFont("Consolas", 16, QFont.Bold))
        self.documenation_layout.addWidget(self.documentation_title, alignment=Qt.AlignHCenter | Qt.AlignTop)

        self.autocomplete_label_bold = QLabel("Autocomplete keywords:", self)
        self.autocomplete_label_bold.setFont(QFont("Consolas", 14, QFont.Bold))
        self.documenation_layout.addWidget(self.autocomplete_label_bold, alignment=Qt.AlignLeft | Qt.AlignTop)

        self.autocomplete_label_normal = QLabel("Type one of the following keywords with CAPS then hit ENTER: CPP, FOR, INT, IF, WHILE.", self)
        self.autocomplete_label_normal.setFont(QFont("Consolas", 12))
        self.autocomplete_label_normal.setWordWrap(True)  
        self.documenation_layout.addWidget(self.autocomplete_label_normal, alignment=Qt.AlignLeft | Qt.AlignTop)

        self.autocomplete_label_tip = QLabel("Tip: You can change the default counter of the FOR loop using FOR-your new counter.", self)
        self.autocomplete_label_tip.setFont(QFont("Consolas", 14, QFont.Bold))
        self.autocomplete_label_tip.setWordWrap(True)  
        self.documenation_layout.addWidget(self.autocomplete_label_tip, alignment=Qt.AlignLeft | Qt.AlignTop)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.documenation_layout.addItem(spacer)

        self.stacked_widget.addWidget(self.documentation_widget)
        
        # Submit code

        self.submit_code = QWidget()
        self.submit_code_layout = QVBoxLayout(self.submit_code)
        self.submit_code.setLayout(self.submit_code_layout)
        
        self.submit_platform = QComboBox(self)
        self.submit_platform.addItems(["Pbinfo"])
        self.submit_platform.setCurrentText("Pbinfo")
        self.submit_code_layout.addWidget(self.submit_platform, alignment=Qt.AlignTop)
        self.username = QLineEdit(self)
        self.username.setPlaceholderText("Username")
        self.submit_code_layout.addWidget(self.username, alignment=Qt.AlignTop)
        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.submit_code_layout.addWidget(self.password, alignment=Qt.AlignTop)
        self.problem_id = QLineEdit(self)
        self.problem_id.setPlaceholderText("Problem ID")
        self.submit_code_layout.addWidget(self.problem_id, alignment=Qt.AlignTop)
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.submit_core)
        self.submit_code_layout.addWidget(self.submit_button, alignment=Qt.AlignTop)

        # From config
        with open('app_data_/data.json', 'r') as file:
                self.credits = json.load(file)
        if self.credits.get("pbinfo", {}).get("username"):
            self.username.setText(self.credits["pbinfo"]["username"])
        if self.credits.get("pbinfo", {}).get("password"):
            self.password.setText(self.credits["pbinfo"]["password"])

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.submit_code_layout.addItem(spacer)

        self.result_label = QLabel("Score: ", self)
        self.result_label.setFont(QFont("Consolas", 14, QFont.Bold))
        self.submit_code_layout.addWidget(self.result_label, alignment=Qt.AlignBottom | Qt.AlignLeft)
        self.source_id_label = QLabel("Source ID: ", self)
        self.source_id_label.setFont(QFont("Consolas", 14, QFont.Bold))
        self.submit_code_layout.addWidget(self.source_id_label, alignment=Qt.AlignBottom | Qt.AlignLeft)

        self.stacked_widget.addWidget(self.submit_code)

        # Aplicarea temei
        self.apply_theme(self.theme)
        with open('config.json', 'r') as file:
            self.config = json.load(file)
        self.user_name = self.config.get('profile_name')

    def toggle_tabs(self):
        curr_funct = self.functions.currentIndex()
        if curr_funct == 0:
            self.show_testing_tab()
        elif curr_funct == 1:
            self.show_submit_pbinfo_tab()
        elif curr_funct == 2:
            self.show_documentation_tab()
        elif curr_funct == 3:
            self.show_server_tab()

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

    def submit_core(self):
        if self.username.text().strip() == "":
            QMessageBox.warning(self, "Code Nimble - Warning", "Username is empty!")
            return
        if self.password.text().strip() == "":
            QMessageBox.warning(self, "Code Nimble - Warning", "Password is empty")
            return
        if self.problem_id.text().strip() == "":
            QMessageBox.warning(self, "Code Nimble - Warning", "ID is empty!")
            return
        if self.win.editor.toPlainText().strip() == "":
            QMessageBox.warning(self, "Code Nimble - Warning", "Source is empty!")
            return
        
        self.submit_interface = pbinfo.PbinfoInterface(self.source_id_label, self.result_label)
        self.submit_interface.unit(self.username.text().strip(), self.password.text().strip(), self.problem_id.text().strip(), self.win.editor.toPlainText().strip())

    def append_to_textbox(self, message):
        self.server_textbox.appendPlainText(message)

    def show_submit_pbinfo_tab(self):
        self.stacked_widget.setCurrentWidget(self.submit_code)

    def show_testing_tab(self):
        self.stacked_widget.setCurrentWidget(self.testing_widget)

    def show_server_tab(self):
        self.stacked_widget.setCurrentWidget(self.server_widget)

    def show_documentation_tab(self):
        self.stacked_widget.setCurrentWidget(self.documentation_widget)

    def diff_core(self):
        self.diff_win = diff.OutputComparator(self, self.theme)
        self.diff_win.show()

    def fetch_core(self):
        self.fetch_win = fetch_window.FetchWindow(self, self.theme)
        self.fetch_win.show()

    def apply_theme(self, theme):
        self.theme = theme
        self.setStyleSheet(f"""
            background-color: {theme.get("background_color")};
            color: {theme.get("text_color")};
        """)
        self.functions.setStyleSheet(f"""
                                     color: {theme.get('text_color')};
                                     background-color: {theme.get('editor_background')};
                                     border: 1px solid {theme.get('border_color')};
                                     font-size: 14px;
                                     padding: 4px;
                                     """)
        self.submit_platform.setStyleSheet(f"""
                                     color: {theme.get('text_color')};
                                     background-color: {theme.get('editor_background')};
                                     border: 1px solid {theme.get('border_color')};
                                     font-size: 14px;
                                     padding: 4px;
                                     """)
        self.input_label.setStyleSheet(f"color: {theme.get('text_color')};")
        self.output_label.setStyleSheet(f"color: {theme.get('text_color')};")
        self.expected_label.setStyleSheet(f"color: {theme.get('text_color')};")
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

        self.username.setStyleSheet(f"""
            background-color: {theme.get("editor_background")};
            color: {theme.get("editor_foreground")};
            border: 1px solid {theme.get("border_color")};
            padding: 5px;
        """)

        self.password.setStyleSheet(f"""
            background-color: {theme.get("editor_background")};
            color: {theme.get("editor_foreground")};
            border: 1px solid {theme.get("border_color")};
            padding: 5px;
        """)

        self.problem_id.setStyleSheet(f"""
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
                border: 1px solid {theme.get('border_color')};
            }}
            QPushButton:hover {{
                background-color: {theme.get("button_hover_color")};
            }}
        """
        self.diff.setStyleSheet(button_style)
        self.fetch.setStyleSheet(button_style)
        self.send_button.setStyleSheet(button_style)
        self.connect_button.setStyleSheet(button_style)
        self.disconnect_button.setStyleSheet(button_style)
        self.start_server.setStyleSheet(button_style)
        self.submit_button.setStyleSheet(button_style)
