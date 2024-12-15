import socket
import threading 

class ServerManager:
    def __init__(self,password, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.password = password
        self.server_socket = None
        self.clients = []
        
    def start_server(self):
        """Inițializează și pornește serverul."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Serverul a pornit pe {self.host}:{self.port} cu parola setata.")
        self.run()

    def stop_server(self):
        """Oprește serverul și eliberează resursele."""
        for client in self.clients:
            client['socket'].close()
        if self.server_socket:
            self.server_socket.close()
        print("Serverul a fost oprit.")

    def broadcast(self, message, sender_socket):
        """Trimite un mesaj tuturor clienților conectați, cu excepția celui care a trimis mesajul."""
        for client in self.clients:
            if client['socket'] != sender_socket:
                try:
                    client['socket'].send(message.encode('utf-8'))
                except:
                    client['socket'].close()
                    self.clients.remove(client)

    def handle_client(self, client_socket, client_address):
        """Gestionarea unui client conectat."""
        try:
            # Primirea parolei de la client
            received_password = client_socket.recv(1024).decode('utf-8').strip()
            print(f"Parola primita de la {client_address}: '{received_password}' (ar trebui sa fie '{self.password}')")

            # Verificarea parolei
            if received_password != self.password:
                print(f"Conexiune refuzata de la {client_address}. Parola este incorecta.")
                client_socket.send("Parola incorecta".encode('utf-8'))
                client_socket.close()
                return

            # Trimite confirmarea că parola a fost corectă
            client_socket.send("OK".encode('utf-8'))

            # Parola este corectă, continuăm cu primirea numelui clientului
            client_name = client_socket.recv(1024).decode('utf-8').strip()
            print(f"Numele clientului: '{client_name}'")

            client_info = {'socket': client_socket, 'name': client_name}
            self.clients.append(client_info)
            print(f"{client_name} s-a conectat de la {client_address}")
            
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"Mesaj de la {client_name}: {message}")
                # Transmite mesajul tuturor clienților
                self.broadcast(f"{client_name}: {message}", client_socket)
            
        except ConnectionResetError:
            print(f"Conexiunea cu {client_address} a fost întrerupta.")
        
        print(f"{client_name} s-a deconectat.")
        self.clients.remove(client_info)
        client_socket.close()
    def run(self):
        """Rularea serverului pentru a accepta conexiuni noi."""
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()
        except KeyboardInterrupt:
            self.stop_server()
