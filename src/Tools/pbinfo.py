from PySide6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QGridLayout, QWidget
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt
import json
import requests
from bs4 import BeautifulSoup
import re
import asyncio
from aiortc import RTCPeerConnection
import time


class PbinfoInterface(QMainWindow):
    BASE_URL = 'https://new.pbinfo.ro'
    LOGIN_PAGE_URL = f"{BASE_URL}/login"
    LOGIN_URL = f'{BASE_URL}/ajx-module/php-login.php'
    PROBLEM_URL = 'https://new.pbinfo.ro/probleme/1/sum'
    SUBMIT_URL = 'https://new.pbinfo.ro/probleme/incarcare-solutie/1'
    SOLUTION_URL_TEMPLATE = 'https://new.pbinfo.ro/json/solutie/'

    def __init__(self, text, theme=None, config=None,parent=None, *args, **kwargs):
        super().__init__(parent,*args, **kwargs)
        
        self.theme = theme or {}
        self.config = config or {}
        self.apply_theme(self.theme)
        
        self.setWindowTitle("Code Nimble - Pbinfo tools")
        self.setGeometry(100, 100, 650, 550)
        self.setWindowIcon(QIcon("images/logo.ico"))
        self.setFixedSize(650, 550)
        
        self.text = text
        
        self.init_ui()
        self.login_payload = {
            'user': '',  # completare
            'parola': ''  # completare
        }
        self.submit_payload = {
            'csrf': '',
            'sursa': '',  # completare
            'limbaj_de_programare': 'cpp',
            'local_ip': '',
            'id': '',  # completare
            'id_runda': '0'
        }

    def apply_theme(self, theme):
        stylesheet = f"""
            QWidget {{
                background-color: {theme.get('background_color', '#333')};
                color: {theme.get('text_color', '#fff')};
            }}
            QPushButton {{
                background-color: {theme.get('button_color', '#555')};
                color: {theme.get('button_text_color', '#fff')};
                padding: 5px;
                border: 1px solid {theme.get('border_color')};
            }}
            QPushButton:hover {{
                background-color: {theme.get('button_hover_color', '#777')};
            }}
            QLineEdit, QTextEdit {{
                background-color: {theme.get('editor_background', '#333')};
                color: {theme.get('text_color', '#fff')};
                border: 1px solid {theme.get("border_color")};
                padding: 5px;
            }}
        """
        self.setStyleSheet(stylesheet)

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)

        # Labels
        username_label = QLabel("Username")
        username_label.setFont(QFont("Arial", 14))
        password_label = QLabel("Password")
        password_label.setFont(QFont("Arial", 14))
        problem_id_label = QLabel("Problem ID")
        problem_id_label.setFont(QFont("Arial", 14))
        layout.addWidget(username_label, 0, 0, Qt.AlignLeft)
        layout.addWidget(password_label, 0, 1, Qt.AlignCenter)
        layout.addWidget(problem_id_label, 0, 2, Qt.AlignRight)

        # Entries
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.problem_id = QLineEdit()

        self.password.setEchoMode(QLineEdit.Password)

        if self.config.get("credits", {}).get("username"):
            self.username.setText(self.config["credits"]["username"])
        if self.config.get("credits", {}).get("password"):
            self.password.setText(self.config["credits"]["password"])

        layout.addWidget(self.username, 1, 0, Qt.AlignLeft)
        layout.addWidget(self.password, 1, 1, Qt.AlignCenter)
        layout.addWidget(self.problem_id, 1, 2, Qt.AlignRight)

        # Buttons
        self.mode1 = QPushButton("Copy from editor")
        self.mode1.clicked.connect(self.get_textbox_code)
        layout.addWidget(self.mode1, 2, 1, Qt.AlignCenter)

        # Textbox
        self.textbox = QTextEdit()
        layout.addWidget(self.textbox, 3, 0, 1, 3)

        # Submit Button
        self.submit = QPushButton("Submit")
        self.submit.clicked.connect(self.unit)
        layout.addWidget(self.submit, 4, 1, Qt.AlignCenter)

        # Solution ID and Score Labels
        self.sol_id = QLabel("Solution ID:")
        self.sol_id.setFont(QFont("Arial", 14))
        self.score_result = QLabel("Score:")
        self.score_result.setFont(QFont("Arial", 14))
        layout.addWidget(self.sol_id, 5, 0, Qt.AlignLeft)
        layout.addWidget(self.score_result, 5, 2, Qt.AlignRight)

    def unit(self):
        if self.username.text().strip() == "":
            QMessageBox.warning(self, "Code Nimble - Warning", "Username is empty!")
            return
        if self.password.text().strip() == "":
            QMessageBox.warning(self, "Code Nimble - Warning", "Password is empty")
            return
        if self.problem_id.text().strip() == "":
            QMessageBox.warning(self, "Code Nimble - Warning", "ID is empty!")
            return
        if self.textbox.toPlainText().strip() == "":
            QMessageBox.warning(self, "Code Nimble - Warning", "Code is empty!")
            return

        self.login_payload['user'] = self.username.text().strip()
        self.login_payload['parola'] = self.password.text().strip()
        self.submit_payload['id'] = self.problem_id.text().strip()
        self.submit_payload['sursa'] = self.textbox.toPlainText()

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
        }
        self.session = requests.Session()
        asyncio.run(self.main())

    def fetch_login_page(self):
        try:
            self.response = self.session.get(self.LOGIN_PAGE_URL, headers=self.headers)
            self.response.raise_for_status()
            return BeautifulSoup(self.response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"[Pbinfo - Error]: Error fetching login page: {e}")
            return

    def extract_form_token(self, soup):
        self.form_token_input = soup.find('input', {'name': 'form_token'})
        if self.form_token_input:
            return self.form_token_input.get('value')
        else:
            QMessageBox.critical(self, "Error", f"[Pbinfo - Error]: Form token not found.")
            return

    def get_csrf(self):
        problem_response = self.session.get(self.PROBLEM_URL, headers=self.headers)
        self.soup = BeautifulSoup(problem_response.text, 'html.parser')

        self.csrf_input = self.soup.find('meta', {'name': 'csrf'})
        if self.csrf_input:
            self.csrf_token = self.csrf_input['content']
            return self.csrf_token
        else:
            QMessageBox.critical(self, "Error", f"[Pbinfo - Error]: CSRF token not found.")
            return

    async def get_local_ip(self):
        local_ip = None

        def on_ice_candidate(candidate):
            nonlocal local_ip
            if candidate:
                candidate_str = candidate.candidate.split(' ')[4]
                if candidate_str:
                    local_ip = candidate_str

        pc = RTCPeerConnection()
        pc.onicecandidate = lambda event: on_ice_candidate(event.candidate)

        # Add a dummy data channel
        pc.createDataChannel('dummyChannel')

        await pc.setLocalDescription(await pc.createOffer())
        await asyncio.sleep(2)

        await pc.close()

        return local_ip

    def save_debug_info(self, filename, content):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)

    def submit_solution(self, local_ip):
        csrf_token = self.get_csrf()

        self.submit_payload['csrf'] = csrf_token
        self.submit_payload['local_ip'] = local_ip

        files = {key: (None, value) for key, value in self.submit_payload.items()}

        try:
            submit_response = self.session.post(self.SUBMIT_URL, files=files, headers=self.headers)
            submit_response_converted = json.loads(submit_response.text)
            if submit_response_converted.get("raspuns") == "Id problema invalid":
                QMessageBox.critical(self, "Error", "Invalid problem ID")
                return
            submit_response.raise_for_status()
            QMessageBox.information(self, "Info", "[Pbinfo]: Solution submitted successfully!")

            match = re.search(r'"id_solutie":(\d+)', submit_response.text)
            if match:
                solution_id = match.group(1)
                return solution_id
            else:
                print("Solution ID not found in response.")
                return
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"[Pbinfo - Error]: Error submitting solution: {e}")
            return

    def fetch_solution_score(self, solution_id):
        SOLUTION_URL = f"{self.SOLUTION_URL_TEMPLATE}{solution_id}?include_problema"
        if solution_id is None:
            return
        try:
            while True:
                response = self.session.get(SOLUTION_URL, headers=self.headers)
                response.raise_for_status()

                response_json = response.json()
                status = response_json['sursa']['status']

                if status == 'complete':
                    score = response_json['sursa']['scor']
                    self.score_result.setText(f"Score: {score}")
                    break
                else:
                    self.score_result.setText("Score: Evaluating...")

                time.sleep(5)  # Așteaptă 5 secunde înainte de a reîncerca

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"[Pbinfo - Error]: Error fetching solution score: {e}")
        except json.JSONDecodeError as je:
            print("Error decoding JSON response:", je)
        except Exception as ex:
            print("An unexpected error occurred:", ex)

    def login(self):
        soup = self.fetch_login_page()
        form_token = self.extract_form_token(soup)
        self.login_payload['form_token'] = form_token

        files = {key: (None, value) for key, value in self.login_payload.items()}

        try:
            login_response = self.session.post(self.LOGIN_URL, files=files, headers=self.headers)
            login_response.raise_for_status()
            return login_response
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"[Pbinfo - Error]: Error during login attempt: {e}")
            return

    async def main(self):
        login_response = self.login()
        login_response_converted = json.loads(login_response.text)
        if login_response_converted.get("raspuns") == "Utilizator/parola incorecte!":
            QMessageBox.critical(self, "Error", "Login failed: incorrect user/password")
            return
        local_ip = await self.get_local_ip()
        solution_id = self.submit_solution(local_ip)
        self.sol_id.setText(f"Solution ID: {solution_id}")
        self.fetch_solution_score(solution_id)
        with open('config.json', 'r') as config_file:
            config_data = json.load(config_file)
        config_data["credits"]["username"] = self.login_payload['user']
        config_data["credits"]["password"] = self.login_payload['parola']
        with open('config.json', 'w') as config_file:
            json.dump(config_data, config_file, indent=4)

    def get_textbox_code(self):
        self.textbox.clear()
        content = self.text.toPlainText()
        self.textbox.setPlainText(content)