import socket

class Client:
    def __init__(self, app, host='127.0.0.1', port=9999, client_name="", password="1234"):
        self.app = app
        self.host = host
        self.port = port
        self.client_name = client_name
        self.password = password
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.connect_to_server()

    def connect_to_server(self):
        try:
            self.client_socket.connect((self.host, self.port))
            self.client_socket.send(self.client_name.encode())  # Send client name
            
            # Wait for password prompt
            password_response = self.client_socket.recv(1024).decode()
            if password_response == "PASSWORD_REQUIRED":
                self.client_socket.send(self.password.encode())
            else:
                print("Server rejected connection: No password required.")
                self.client_socket.close()
                self.app.client = None
                self.app.statusbar.update_server("none")
                return
            
            # Receive password acceptance
            password_acceptance = self.client_socket.recv(1024).decode()
            if password_acceptance != "PASSWORD_ACCEPTED":
                print("Server rejected connection: Wrong password.")
                self.client_socket.close()
                self.app.client = None
                self.app.statusbar.update_server("none")
                return

            self.connected = True
        except Exception as e:
            print(f"Connection failed: {e}")
            self.app.client = None
            self.app.statusbar.update_server("none")

    def send_message(self, message):
        if self.connected:
            self.client_socket.send(message.encode())

    def disconnect(self):
        try:
            self.send_message("DISCONNECT")
            self.client_socket.close()
            self.connected = False
        except:
            pass

    def receive_messages(self, callback):
        while self.connected:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    callback(message)
            except:
                print("An error occurred!")
                self.client_socket.close()
                self.connected = False
                break

    def is_connected(self):
        return self.connected
