import requests
from bs4 import BeautifulSoup

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