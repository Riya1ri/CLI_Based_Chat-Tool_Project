import socket
import threading

class ChatroomServer:
    def __init__(self):
        self.host = "127.0.0.1"  # Localhost
        self.port = 5555
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chatrooms = {"room1": [], "room2": []}

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen()

        print("Server started. Listening for connections...")

        while True:
            client_socket, addr = self.server.accept()
            print(f"New connection from {addr[0]}:{addr[1]}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        # Prompt client to join a chatroom
        client_socket.send("JOIN".encode())
        chatroom = client_socket.recv(1024).decode()

        # Add client to the chatroom
        self.chatrooms[chatroom].append(client_socket)

        # Send welcome message to client
        client_socket.send("Welcome to the chatroom!".encode())

        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message == "EXIT":
                    self.chatrooms[chatroom].remove(client_socket)
                    client_socket.send("You left the chatroom.".encode())
                    client_socket.close()
                    break
                self.broadcast_message(chatroom, message)
            except ConnectionResetError:
                self.chatrooms[chatroom].remove(client_socket)
                break

    def broadcast_message(self, chatroom, message):
        for client_socket in self.chatrooms[chatroom]:
            client_socket.send(message.encode())

    def stop(self):
        self.server.close()

server = ChatroomServer()
server.start()
