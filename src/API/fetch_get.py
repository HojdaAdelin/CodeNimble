import requests
from bs4 import BeautifulSoup
import re
import sys

def fetch_pbinfo(terminal,id):
    url = f"https://new.pbinfo.ro/json/probleme/{id}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)
    sys.stdout.reconfigure(encoding='utf-8')

    if response.status_code == 200:
        try:
            
            data = response.json()
            
            enunt = data['problema']['enunt_html']
            
            soup = BeautifulSoup(enunt, 'html.parser')
        
            pre_sections = soup.find_all('pre')
            
            if len(pre_sections) >= 2:
                # Considerăm că primele două secțiuni <pre> sunt pentru Intrare și Ieșire
                intrare_text = pre_sections[0].get_text(strip=True)
                iesire_text = pre_sections[1].get_text(strip=True)
                
                return intrare_text, iesire_text
            else:
                terminal.notification("[Pbinfo - Error]: Intrare & Iesire doesn't exist")
        except ValueError as e:
            terminal.notification(f"[Pbinfo - Error]: {e}")
    else:
        terminal.notification(f"[Pbinfo - Error]: {response.status_code}")

def fetch_kilonova(terminal, id):
    url = f'https://kilonova.ro/problems/{id}'

    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    pre_tags = soup.find_all('pre')

    if len(pre_tags) >= 2:
        stdin_content = pre_tags[0].get_text()
        stdout_content = pre_tags[1].get_text()
        return stdin_content, stdout_content
    else:
        terminal.notification("[Kilonova - Error]: Insufficient <pre> tags")