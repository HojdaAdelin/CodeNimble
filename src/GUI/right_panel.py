from PySide6.QtWidgets import (
    QWidget, QLabel, QTextEdit, QPushButton, QGridLayout, QSizePolicy, QStackedWidget, QPlainTextEdit, QVBoxLayout, QLineEdit, QFrame, QHBoxLayout, QMessageBox, QComboBox, QSpacerItem, QCheckBox
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
from Tools import kilonova

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
        self.functions.addItems(["Testing","Submit code", "Documentation", "Server", "Settings"])
        self.functions.setItemText
        self.functions.currentIndexChanged.connect(self.toggle_tabs)
        self.main_layout.addWidget(self.functions)
        
        # Crearea QStackedWidget pentru a comuta între tab-uri
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)
        



        # Testing tab
        self.testing_widget = QWidget()
        self.testing_layout = QGridLayout(self.testing_widget)
        self.testing_widget.setLayout(self.testing_layout)

        self.layout = self.testing_layout
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        self.layout.setColumnStretch(0, 1)
        self.layout.setRowStretch(0, 0)  # Pentru combo box
        self.layout.setRowStretch(1, 0)  # Pentru label input
        self.layout.setRowStretch(2, 1)  # Pentru input box
        self.layout.setRowStretch(3, 0)  # Pentru label output
        self.layout.setRowStretch(4, 1)  # Pentru output box
        self.layout.setRowStretch(5, 0)  # Pentru label expected
        self.layout.setRowStretch(6, 1)  # Pentru expected box
        self.layout.setRowStretch(7, 0)  # Pentru butonul diff
        self.layout.setRowStretch(8, 0)  # Pentru butonul fetch

        # Dicționar pentru stocarea test case-urilor
        self.test_cases = {
            "Test Case 1": {"input": "", "output": "", "expected": ""},
            "Test Case 2": {"input": "", "output": "", "expected": ""},
            "Test Case 3": {"input": "", "output": "", "expected": ""},
            "Test Case 4": {"input": "", "output": "", "expected": ""},
            "Test Case 5": {"input": "", "output": "", "expected": ""}
        }

        # Combo box pentru selectarea test case-ului
        self.test_selector = QComboBox(self)
        self.test_selector.addItems(list(self.test_cases.keys()))
        self.test_selector.currentTextChanged.connect(self.change_test_case)
        self.layout.addWidget(self.test_selector, 0, 0)

        # Label-ul pentru input
        self.input_label = QLabel("Input", self)
        self.layout.addWidget(self.input_label, 1, 0, Qt.AlignHCenter)

        # Textbox pentru input
        self.input_box = QTextEdit(self)
        self.input_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.input_box.textChanged.connect(lambda: self.save_current_state("input"))
        self.layout.addWidget(self.input_box, 2, 0)

        # Label-ul pentru output
        self.output_label = QLabel("Output", self)
        self.layout.addWidget(self.output_label, 3, 0, Qt.AlignHCenter)

        # Textbox pentru output
        self.output_box = QTextEdit(self)
        self.output_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.output_box.textChanged.connect(lambda: self.save_current_state("output"))
        self.layout.addWidget(self.output_box, 4, 0)

        # Label-ul pentru expected output
        self.expected_label = QLabel("Expected Output", self)
        self.layout.addWidget(self.expected_label, 5, 0, Qt.AlignHCenter)

        # Textbox pentru expected output
        self.expected_box = QTextEdit(self)
        self.expected_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.expected_box.textChanged.connect(lambda: self.save_current_state("expected"))
        self.layout.addWidget(self.expected_box, 6, 0)

        # Butonul pentru comparare
        self.diff = QPushButton("Output comparator", self, clicked=self.diff_core)
        self.diff.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.addWidget(self.diff, 7, 0)

        # Butonul pentru fetch
        self.fetch = QPushButton("Fetch test cases", self, clicked=self.fetch_core)
        self.fetch.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.addWidget(self.fetch, 8, 0)

        # Adăugăm widget-ul „Testing" în stacked_widget
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

        # Text box pentru documentatie
        self.documentation_textbox = QTextEdit(self)
        self.documentation_textbox.setReadOnly(True)  # Setăm să fie doar pentru citire
        self.documentation_textbox.setFont(QFont("Consolas", 12))
        self.documentation_textbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.documentation_textbox.setMinimumHeight(200)  # Poți ajusta valoarea dacă este necesar

        # Setăm textul complet al documentației
        self.documentation_textbox.setHtml("""
            <h1 style="font-size:16pt; font-weight:bold; text-align:center;">Documentation</h1>
            <p><span style="font-size:14pt; font-weight:bold;">Autocomplete keywords:</span></p>
            <p>Type one of the following keywords with CAPS then hit ENTER: CPP, FOR, INT, IF, WHILE.</p>
            <p><span style="font-size:14pt; font-weight:bold;">Tip:</span> You can change the default counter of the FOR loop using FOR-your new counter.</p>
        """)

        self.documenation_layout.addWidget(self.documentation_textbox)

        self.stacked_widget.addWidget(self.documentation_widget)
        
        # Submit code

        self.submit_code = QWidget()
        self.submit_code_layout = QVBoxLayout(self.submit_code)
        self.submit_code.setLayout(self.submit_code_layout)
        
        self.submit_platform = QComboBox(self)
        self.submit_platform.addItems(["Kilonova", "Pbinfo"])
        self.submit_platform.setCurrentText("Kilonova")
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

        # Settings tab
        with open('config.json', 'r') as file:
            self.config = json.load(file)
        

        self.settings = QWidget()
        self.settings_layout = QVBoxLayout(self.settings)
        self.settings.setLayout(self.settings_layout)
        val = self.config['startup']['pre_template']
        self.pre_template = QCheckBox("Startup template", self)
        if val == "0":
            self.pre_template.setChecked(True)
        self.settings_layout.addWidget(self.pre_template, alignment=Qt.AlignTop)
        self.pre_template_items = QComboBox(self)
        self.pre_template_items.addItems(["C++", "C++ Competitive", "C", "Java", "Html"])
        self.settings_layout.addWidget(self.pre_template_items, alignment=Qt.AlignTop)

        self.editor_font_label = QLabel("Editor font", self)
        self.editor_font_label.setFont(QFont("Consolas", 12))
        self.settings_layout.addWidget(self.editor_font_label, alignment=Qt.AlignTop)
        self.editor_font = QLineEdit(self)
        self.editor_font.setText(self.config["editor_font_size"])
        self.settings_layout.addWidget(self.editor_font, alignment=Qt.AlignTop)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.settings_layout.addItem(spacer)

        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_settings)
        self.settings_layout.addWidget(self.save_button, alignment=Qt.AlignBottom)
        
        self.stacked_widget.addWidget(self.settings)

        # Aplicarea temei
        self.apply_theme(self.theme)
        self.user_name = self.config.get('profile_name')

    def save_current_state(self, field):
        current_test = self.test_selector.currentText()
        if field == "input":
            self.test_cases[current_test]["input"] = self.input_box.toPlainText()
        elif field == "output":
            self.test_cases[current_test]["output"] = self.output_box.toPlainText()
        elif field == "expected":
            self.test_cases[current_test]["expected"] = self.expected_box.toPlainText()

    def change_test_case(self, test_case):
        # Încărcăm datele salvate pentru test case-ul selectat
        self.input_box.setText(self.test_cases[test_case]["input"])
        self.output_box.setText(self.test_cases[test_case]["output"])
        self.expected_box.setText(self.test_cases[test_case]["expected"])

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
        elif curr_funct == 4:
            self.show_settings_tab()

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
            self.win.status_bar.toggle_inbox_icon("Submit tools - Username is empty!", "orange")
            return
        if self.password.text().strip() == "":
            self.win.status_bar.toggle_inbox_icon("Submit tools - Password is empty!", "orange")
            return
        if self.problem_id.text().strip() == "":
            self.win.status_bar.toggle_inbox_icon("Submit tools - ID is empty!", "orange")
            return
        if self.win.editor.toPlainText().strip() == "":
            self.win.status_bar.toggle_inbox_icon("Submit tools - Source is empty!", "orange")
            return
        
        if self.submit_platform.currentIndex() == 0:
            kilonova.login_and_submit(self.username.text().strip(), self.password.text().strip(), self.win.file_manager.get_opened_filename(),self.problem_id.text().strip())
        elif self.submit_platform.currentIndex() == 0:
            self.submit_interface = pbinfo.PbinfoInterface(self.source_id_label, self.result_label)
            self.submit_interface.unit(self.username.text().strip(), self.password.text().strip(), self.problem_id.text().strip(), self.win.editor.toPlainText().strip())

    def save_settings(self):
        self.config['editor_font_size'] = self.editor_font.text().strip()
        if self.pre_template.isChecked():
            self.config['startup']['pre_template'] = "0"
            self.config['startup']['template'] = self.pre_template_items.currentText().strip()
        else:
            self.config['startup']['pre_template'] = "1"
            self.config['startup']['template'] = ""
        with open('config.json', 'w') as file:
            json.dump(self.config, file,indent=4)
        self.win.re_zoom(self.editor_font.text().strip())
        self.win.status_bar.toggle_inbox_icon("Settings saved!")

    def append_to_textbox(self, message):
        self.server_textbox.appendPlainText(message)

    def show_settings_tab(self):
        self.stacked_widget.setCurrentWidget(self.settings)

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
        self.pre_template_items.setStyleSheet(f"""
            background-color: {theme.get("editor_background")};
            color: {theme.get("editor_foreground")};
            border: 1px solid {theme.get("border_color")};
            padding: 5px;
        """)
        self.pre_template.setStyleSheet(f"""
            QCheckBox {{
                color: {theme.get("text_color")};  /* Culoarea textului */
                font-size: 16px;  /* Dimensiunea fontului */
            }}
            QCheckBox::indicator {{
                border: 2px solid {theme.get("border_color")};  /* Bordura casetei de bifare */
                width: 16px;  /* Lățimea casetei */
                height: 16px;  /* Înălțimea casetei */
                
            }}
            QCheckBox::indicator:checked {{
                background-color: {theme.get("button_hover_color")};  /* Culoarea de fundal când este bifată */
                border: 2px solid {theme.get("border_color")};  /* Bordura când este bifată */
            }}
            
        """)
        
        self.password_entry.setStyleSheet(f"""
            background-color: {theme.get("editor_background")};
            color: {theme.get("editor_foreground")};
            border: 1px solid {theme.get("border_color")};
            padding: 5px;
        """)
        self.editor_font.setStyleSheet(f"""
            background-color: {theme.get("editor_background")};
            color: {theme.get("editor_foreground")};
            border: 1px solid {theme.get("border_color")};
            padding: 5px;
        """)
        self.test_selector.setStyleSheet(f"""
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
        self.save_button.setStyleSheet(button_style)
