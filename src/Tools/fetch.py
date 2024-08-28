import requests
from bs4 import BeautifulSoup
from PySide6.QtWidgets import QMessageBox

def fetch_pbinfo(id):
    url = f"https://new.pbinfo.ro/json/probleme/{id}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)

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
        print("[Pbinfo - Error]: Intrare & Iesire doesn't exist")
    
def fetch_kilonova(id):
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
        print("[Kilonova - Error]: Insufficient <pre> tags")

def fetch_codeforce(contest_id, problem_id, link=False):
    if link:
        url = link
    else:
        url = f"https://codeforces.com/contest/{contest_id}/problem/{problem_id}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    pretest_input = None
    pretest_output = None
    
    input_div = soup.find('div', class_='input')
    if input_div:
        pre_element = input_div.find('pre')
        if pre_element:
            pretest_input = pre_element.get_text("\n", strip=True)
    
    output_div = soup.find('div', class_='output')
    if output_div:
        pre_element = output_div.find('pre')
        if pre_element:
            pretest_output = pre_element.get_text("\n", strip=True)
    
    return pretest_input, pretest_output

def fetch_atcoder(problem_url):
    response = requests.get(problem_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Găsește toate secțiunile de exemplu (sample) Input și Output
    sample_inputs = soup.find_all('h3', string='Sample Input 1')
    sample_outputs = soup.find_all('h3', string='Sample Output 1')
    
    # Verificăm că există cel puțin un exemplu de input și output
    if sample_inputs and sample_outputs:
        # Extragem primul exemplu de input și output
        pretest_input = sample_inputs[0].find_next('pre').get_text(strip=True)
        pretest_output = sample_outputs[0].find_next('pre').get_text(strip=True)
        
        return pretest_input, pretest_output
    else:
        return "None", "None"