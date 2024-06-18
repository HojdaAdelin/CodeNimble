import socket

class Client:
    def __init__(self, host='127.0.0.1', port=9999):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def send_message(self, message):
        try:
            self.client_socket.send(message.encode())
        except Exception as e:
            print(f"Error sending message: {e}")

    def receive_messages(self, callback):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    callback(message)
            except Exception as e:
                print(f"Error receiving message: {e}")
                self.client_socket.close()
                break