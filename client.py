import socket
import threading

class ChatroomClient:
    def __init__(self):
        self.host = "127.0.0.1"  # Localhost
        self.port = 5555
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None

    def connect(self):
        self.client.connect((self.host, self.port))

    def send_message(self, message):
        self.client.send(message.encode())

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode()
                print(message)
            except ConnectionResetError:
                print("Server connection closed.")
                break

    def run(self):
        self.connect()
        print("Welcome to the chatroom!")
        print("Available Chatrooms: room1, room2")

        while True:
            self.username = input("Enter your username: ")
            chatroom = input("Enter the chatroom you want to join: ")

            if chatroom not in ["room1", "room2"]:
                print("Invalid chatroom. Try again.")
                continue

            self.send_message(chatroom)
            response = self.client.recv(1024).decode()
            if response == "JOIN":
                print("Joined the chatroom!")
                break

        threading.Thread(target=self.receive_messages).start()

        while True:
            message = input()
            if message.lower() == "exit":
                self.send_message("EXIT")
                break
            self.send_message(f"{self.username}: {message}")

        self.client.close()

client = ChatroomClient()
client.run()
