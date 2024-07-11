import socket
import threading

class Server:
    def __init__(self, host='0.0.0.0', port=9999, password="1234"):
        self.host = host
        self.port = port
        self.password = password
        self.clients = {}

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")

        while True:
            client_socket, addr = server_socket.accept()
            client_name = client_socket.recv(1024).decode()

            # Ask for password
            client_socket.send("PASSWORD_REQUIRED".encode())
            password_attempt = client_socket.recv(1024).decode()
            if password_attempt != self.password:
                client_socket.send("WRONG_PASSWORD".encode())
                client_socket.close()
                continue

            client_socket.send("PASSWORD_ACCEPTED".encode())
            self.clients[client_socket] = client_name
            print(f"Connection established with {client_name} ({addr})")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.daemon = True
            client_thread.start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                if message == "DISCONNECT":
                    print(f"Client {self.clients[client_socket]} disconnected")
                    del self.clients[client_socket]
                    client_socket.close()
                    break
                self.broadcast(message, client_socket)
            except:
                if client_socket in self.clients:
                    del self.clients[client_socket]
                client_socket.close()
                break

    def broadcast(self, message, client_socket):
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(message.encode())
                except:
                    del self.clients[client]
                    client.close()