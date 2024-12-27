from time import sleep
import requests
from bs4 import BeautifulSoup
import requests
import sys
import json
import os
from cryptography.fernet import Fernet
import base64

custom_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
}

def safe_key(key: bytes, filename: str) -> bytes:
        with open(filename, 'wb') as file:
            file.write(key)

def  load_key(filename: str) -> bytes:
        with open(filename, 'rb') as file:
            return file.read()

def contest_info():
    BASE_URL = 'https://kilonova.ro/contests?page=official'
    response = requests.get(BASE_URL, headers=custom_header)
    soup = BeautifulSoup(response.content, 'html.parser')
    first_container = soup.find(class_='c-container mb-2')
    contest_name = first_container.find(class_='segment-panel my-1').find('h2').text.strip()
    status_paragraph = first_container.find('p', string=lambda t: t and t.startswith('Status:'))
    contest_status = ' '.join(status_paragraph.text.split()).replace('Status: ', '')
    return contest_name, contest_status

BASE_URL = 'https://kilonova.ro'
LOGIN_URL = f"{BASE_URL}/api/auth/login"
SUBMIT_URL = f"{BASE_URL}/api/submissions/submit"

def login_and_submit(win_base, username, password, filepath, problem_id, language="cpp17"):
    
    with requests.Session() as session:
        
        login_payload = {
            'username': username,
            'password': password
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
            'Authorization': ''
        }

        # Trimite cererea de login
        response = session.post(LOGIN_URL, data=login_payload, headers=headers)

        # Verifică dacă autentificarea a fost cu succes și extrage token-ul
        if response.status_code == 200:
            headers["Authorization"] = response.json()["data"]
        else:
            win_base.win.status_bar.toggle_inbox_icon(f"Auth error: {response.status_code}, {response.text}")
            return  

        # Deschide fișierul și construiește payload-ul pentru trimitere
        with open(filepath, 'rb') as file:
            files = {
                'code': (filepath, file),  # Nume și fișierul propriu-zis
            }
            submit_payload = {
                'problem_id': problem_id,
                'language': language,
            }

            submit_response = session.post(SUBMIT_URL, data=submit_payload, files=files, headers=headers)
        
        try:
            key = load_key("app_data_/secret.key")
        except FileNotFoundError:
            key = Fernet.generate_key()
            safe_key(key, "app_data_/secret.key")
        fernet = Fernet(key)
        if submit_response.status_code == 200:
            with open('app_data_/data.json', 'r') as file:
                user_login = json.load(file)
            username_encrypted = base64.urlsafe_b64encode(fernet.encrypt(username.encode('utf-8'))).decode('utf-8')
            password_encrypted = base64.urlsafe_b64encode(fernet.encrypt(password.encode('utf-8'))).decode('utf-8')
            user_login['kilonova']['username'] = username_encrypted
            user_login['kilonova']['password'] = password_encrypted
            with open('app_data_/data.json', 'w') as file:
                json.dump(user_login, file, indent=4)

            response_json = submit_response.json()
            solution_id = response_json.get("data")
            win_base.source_id_label.setText(f"Solution ID: {solution_id}")
            sleep(1)
            SOLUTION_URL = f"{BASE_URL}/api/submissions/getByID?id={solution_id}"
            solution_response = session.get(SOLUTION_URL, headers=headers)
            solution_response.raise_for_status()
            solution_json = solution_response.json()
            score = solution_json.get("data", {}).get("score")
            win_base.result_label.setText(f"Score: {score}")

            win_base.win.status_bar.toggle_inbox_icon("Submitted code successfully!")
        else:
            win_base.win.status_bar.toggle_inbox_icon(f"Error: {submit_response.text}")
        print("Status Submit:", submit_response.status_code)
        print("Response Submit:", submit_response.text)