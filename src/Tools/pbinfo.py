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
    BASE_URL = 'https://www.pbinfo.ro'
    LOGIN_PAGE_URL = f"{BASE_URL}/login"
    LOGIN_URL = f'{BASE_URL}/ajx-module/php-login.php'
    PROBLEM_URL = 'https://new.pbinfo.ro/probleme/1/sum'
    SUBMIT_URL = 'https://new.pbinfo.ro/probleme/incarcare-solutie/1'
    SOLUTION_URL_TEMPLATE = 'https://new.pbinfo.ro/json/solutie/'

    def __init__(self, source_id, result,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.source_id_label = source_id
        self.result = result   
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

    def unit(self, username, password, problem_id, source):
        

        self.login_payload['user'] = username
        self.login_payload['parola'] = password
        self.submit_payload['id'] = problem_id
        self.submit_payload['sursa'] = source

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
                    self.result.setText(f"Score: {score}")
                    break
                else:
                    self.result.setText("Score: Evaluating...")

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
        self.source_id_label.setText(f"Solution ID: {solution_id}")
        self.fetch_solution_score(solution_id)
        with open('app_data_/data.json', 'r') as config_file:
            config_data = json.load(config_file)
        config_data["pbinfo"]["username"] = self.login_payload['user']
        config_data["pbinfo"]["password"] = self.login_payload['parola']
        with open('app_data_/data.json', 'w') as config_file:
            json.dump(config_data, config_file, indent=4)
