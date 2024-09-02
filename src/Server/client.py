import socket
import threading

class ClientManager:
    def __init__(self, name, password,gui, host='localhost', port=8080):
        self.name = name
        self.password = password
        self.host = host
        self.port = port
        self.client_socket = None
        self.gui = gui  # Referință către interfața grafică pentru actualizarea QPlainTextEdit
    
    def connect_to_server(self):
        """Conectarea la server."""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Încearcă să te conectezi la server
            self.client_socket.connect((self.host, self.port))
        except ConnectionRefusedError:
            print("Conexiune esuata: Serverul nu este pornit sau nu este disponibil.")
            self.client_socket.close()
            return
        except socket.error as e:
            print(f"Eroare la conectare: {e}")
            self.client_socket.close()
            return

        # Trimiterea parolei
        print(f"Trimit parola: '{self.password}'")
        self.client_socket.send(self.password.encode('utf-8'))

        # Așteptarea confirmării de la server pentru parolă
        response = self.client_socket.recv(1024).decode('utf-8').strip()
        if response != "OK":
            print(f"Conectare esuată: {response}")
            self.client_socket.close()
            return
        
        # Trimiterea numelui clientului după confirmarea parolei
        print(f"Trimit numele: '{self.name}'")
        self.client_socket.send(self.name.encode('utf-8'))

        print(f"{self.name} s-a conectat la server.")
        
        # Pornește un thread pentru a asculta mesajele de la server
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self, message):
        """Trimiterea unui mesaj către server."""
        if self.client_socket:
            self.client_socket.send(message.encode('utf-8'))

    def receive_messages(self):
        """Ascultă și afișează mesajele de la server."""
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message and self.gui:
                    self.gui.append_to_textbox(message)  # Actualizează QPlainTextEdit
            except:
                print("Conexiunea a fost intrerupta.")
                break
    
    def disconnect(self):
        """Deconectarea de la server."""
        if self.client_socket:
            self.client_socket.close()
            print(f"{self.name} s-a deconectat de la server.")
            self.client_socket = None
