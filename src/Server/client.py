import socket

class Client:
    def __init__(self, host='127.0.0.1', port=9999, client_name=""):
        self.host = host
        self.port = port
        self.client_name = client_name
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

    def connect_to_server(self):
        self.client_socket.connect((self.host, self.port))
        self.client_socket.send(self.client_name.encode())  # Trimite numele clientului la server

    def send_message(self, message):
        self.client_socket.send(message.encode())

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
