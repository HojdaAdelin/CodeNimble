import requests
from bs4 import BeautifulSoup
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

custom_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
}

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
            win_base.win.status_bar.toggle_inbox_icon("Auth successfully!")
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
        
        if submit_response.status_code == 200:
            win_base.win.status_bar.toggle_inbox_icon("Submitted code successfully!")
        else:
            win_base.win.status_bar.toggle_inbox_icon(f"Error: {submit_response.text}")
        print("Status Submit:", submit_response.status_code)
        print("Response Submit:", submit_response.text)