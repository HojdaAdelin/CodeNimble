import socket
import threading

class Server:
    def __init__(self, host='0.0.0.0', port=9999):
        self.host = host
        self.port = port
        self.clients = []

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")

        while True:
            client_socket, addr = server_socket.accept()
            self.clients.append(client_socket)
            print(f"Connection established with {addr}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.daemon = True
            client_thread.start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                self.broadcast(message, client_socket)
            except Exception as e:
                print(f"Error handling client: {e}")
                self.clients.remove(client_socket)
                client_socket.close()
                break

    def broadcast(self, message, client_socket):
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(message.encode())
                except Exception as e:
                    print(f"Error broadcasting message: {e}")
                    self.clients.remove(client)
                    client.close()

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