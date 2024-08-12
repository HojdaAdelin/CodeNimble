import customtkinter as ct
import json
import tkinter as tk
import requests
from bs4 import BeautifulSoup
import re
import asyncio
from pyee import AsyncIOEventEmitter
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCIceCandidate
import sys
import os
from tkinter import messagebox
import time

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from MainMenu import themes
from Config import check

class PbinfoInterface(ct.CTk):
    BASE_URL = 'https://new.pbinfo.ro'
    LOGIN_PAGE_URL = f"{BASE_URL}/login"
    LOGIN_URL = f'{BASE_URL}/ajx-module/php-login.php'
    PROBLEM_URL = 'https://new.pbinfo.ro/probleme/1/sum'
    SUBMIT_URL = 'https://new.pbinfo.ro/probleme/incarcare-solutie/1'
    SOLUTION_URL_TEMPLATE = 'https://new.pbinfo.ro/json/solutie/'
    def __init__(self,text,terminal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bg_color, self.text_bg, self.text_color, self.hover_color, self.button_color, self.button_hover_color, self.button_text_color = themes.return_default_win_color(check.get_config_value("theme"))
        self.configure(fg_color = self.bg_color)
        self.iconbitmap("images/logo.ico")
        self.geometry("650x550")
        self.resizable(False, False)
        self.title("Code Nimble - Pbinfo tools")
        themes.title_bar_color_handle(self)
        self.gui()
        self.login_payload = {
            'user': '', # completare
            'parola': '' # completare
        }
        self.submit_payload = {
            'csrf': '',
            'sursa': '', # completare
            'limbaj_de_programare': 'cpp',
            'local_ip': '',
            'id': '', # completare
            'id_runda': '0'
        }

        self.text = text
        self.terminal = terminal

    def gui(self):
        # Row 1
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        username_label = ct.CTkLabel(self,text="Username", text_color=self.text_color, font=("", 20))
        password_label = ct.CTkLabel(self,text="Password", text_color=self.text_color, font=("", 20))
        problem_id_label = ct.CTkLabel(self,text="Problem ID", text_color=self.text_color, font=("", 20))
        username_label.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        password_label.grid(row=0, column=1, sticky="n", padx=10, pady=10)
        problem_id_label.grid(row=0, column=2, sticky="ne", padx=10, pady=10)
        # Row 2 
        self.username = ct.CTkEntry(self,text_color=self.text_color, fg_color=self.bg_color)
        self.password = ct.CTkEntry(self,text_color=self.text_color, fg_color=self.bg_color)
        self.problem_id = ct.CTkEntry(self,text_color=self.text_color, fg_color=self.bg_color)
        self.username.grid(row=1, column=0, sticky="nw", padx=10)
        self.password.grid(row=1, column=1, sticky="n", padx=10)
        self.problem_id.grid(row=1, column=2, sticky="ne", padx=10)
        # Row 3 & 4
        self.mode1 = ct.CTkButton(self,text="Copy from editor",command=self.get_textbox_code, fg_color=self.button_color, hover_color=self.button_hover_color, text_color=self.button_text_color)
        self.textbox = ct.CTkTextbox(self, fg_color=self.text_bg, corner_radius=0, text_color=self.text_color)
        self.mode1.grid(row=2, column=1, sticky="n", pady=10)
        self.textbox.grid(row=3, column=0,columnspan=3, sticky="nswe", padx=10)
        # Row 5
        self.submit = ct.CTkButton(self, text="Submit", command=self.unit, fg_color=self.button_color, hover_color=self.button_hover_color, text_color=self.button_text_color)
        self.submit.grid(row=4, column=1, sticky="n", pady=10)
        self.sol_id = ct.CTkLabel(self, text="Solution ID:", text_color=self.text_color, font=("", 20))
        self.score_result = ct.CTkLabel(self, text="Score:", text_color=self.text_color, font=("", 20))
        self.sol_id.grid(row=4, column=0, sticky="nw", padx=10, pady=10)
        self.score_result.grid(row=4, column=2, sticky="ne", padx=25, pady=10)

    def unit(self):
        if self.username.get().strip() == "":
            messagebox.showwarning("Code Nimble - Warning", "Username is empty!")
            return
        if self.password.get().strip() == "":
            messagebox.showwarning("Code Nimble - Warning", "Password is empty")
            return
        if self.problem_id.get().strip() == "":
            messagebox.showwarning("Code Nimble - Warning", "ID is empty!")
            return
        if self.textbox.get("1.0", "end-1c").strip() == "":
            messagebox.showwarning("Code Nimble - Warning", "Code is empty!")
            return 
        self.login_payload['user'] = self.username.get().strip()
        self.login_payload['parola'] = self.password.get().strip()
        self.submit_payload['id'] = self.problem_id.get().strip()
        self.submit_payload['sursa'] = self.textbox.get("1.0", "end-1c")
        # Engine
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
            messagebox.showerror("Error", "Check terminal for more details")
            self.terminal.notification(f"[Pbinfo - Error]: Error fetching login page: {e}")
            return
    def extract_form_token(self,soup):
        self.form_token_input = soup.find('input', {'name': 'form_token'})
        if self.form_token_input:
            return self.form_token_input.get('value')
        else:
            messagebox.showerror("Error", "Check terminal for more details")
            self.terminal.notification(f"[Pbinfo - Error]: Form token not found.")
            return

    def get_csrf(self):
        problem_response = self.session.get(self.PROBLEM_URL, headers=self.headers)
        self.soup = BeautifulSoup(problem_response.text, 'html.parser')
        
        self.csrf_input = self.soup.find('meta', {'name': 'csrf'})
        if self.csrf_input:
            self.csrf_token = self.csrf_input['content']
            return self.csrf_token
        else:
            messagebox.showerror("Error", "Check terminal for more details")
            self.terminal.notification(f"[Pbinfo - Error]: CSRF token not found.")
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
    
    def save_debug_info(self,filename, content):
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
                messagebox.showerror("Error", "Invalid problem ID")
                return 
            submit_response.raise_for_status()
            self.terminal.notification("[Pbinfo]: Solution submitted successfully!")
            
            match = re.search(r'"id_solutie":(\d+)', submit_response.text)
            if match:
                solution_id = match.group(1)
                return solution_id
            else:
                print("Solution ID not found in response.")
                return
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", "Check terminal for more details")
            self.terminal.notification(f"[Pbinfo - Error]: Error submitting solution: {e}")
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
                    self.score_result.configure(text=f"Score: {score}")
                    break
                else:
                    self.score_result.configure(text="Score: Evaluating...")

                time.sleep(5)  # Așteaptă 5 secunde înainte de a reîncerca
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", "Check terminal for more details")
            self.terminal.notification(f"[Pbinfo - Error]: Error fetching solution score: {e}")
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
            #print(f"Login response status code: {login_response.status_code}") 
            login_response.raise_for_status()
            return login_response
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", "Check terminal for more details")
            self.terminal.notification(f"[Pbinfo - Error]: Error during login attempt: {e}")
            return

    async def main(self):
        login_response = self.login()
        login_response_converted = json.loads(login_response.text)
        if login_response_converted.get("raspuns") == "Utilizator/parola incorecte!":
            messagebox.showerror("Error", "Login failed: incorrect user/password")
            return
        local_ip = await self.get_local_ip()
        solution_id = self.submit_solution(local_ip)
        self.sol_id.configure(text=f"Solution ID: {solution_id}")
        self.fetch_solution_score(solution_id)

    def get_textbox_code(self):
        self.textbox.delete("1.0", "end")
        content = self.text.get("1.0", "end-1c")
        self.textbox.insert("1.0",content)