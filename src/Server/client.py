import socket

class Client:
    def __init__(self, host='127.0.0.1', port=9999, client_name="", password="1234"):
        self.host = host
        self.port = port
        self.client_name = client_name
        self.password = password
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

    def connect_to_server(self):
        self.client_socket.connect((self.host, self.port))
        self.client_socket.send(self.client_name.encode())  # Send client name
        
        # Wait for password prompt
        password_response = self.client_socket.recv(1024).decode()
        if password_response == "PASSWORD_REQUIRED":
            self.client_socket.send(self.password.encode())
        else:
            print("Server rejected connection: Wrong password.")
            self.client_socket.close()
            return
        
        # Receive password acceptance
        password_acceptance = self.client_socket.recv(1024).decode()
        if password_acceptance != "PASSWORD_ACCEPTED":
            print("Server rejected connection: Wrong password.")
            self.client_socket.close()
            return

    def send_message(self, message):
        self.client_socket.send(message.encode())

    def disconnect(self):
        try:
            self.send_message("DISCONNECT")
            self.client_socket.close()
        except:
            pass

    def receive_messages(self, callback):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    callback(message)
            except:
                print("An error occurred!")
                self.client_socket.close()
                break