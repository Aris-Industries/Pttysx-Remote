import curses
import socket
from cryptography.fernet import Fernet
import threading

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('10.43.1.21', 1234))

# Receive the encryption key from the server
key = client_socket.recv(1024)
cipher_suite = Fernet(key)

while True:
    name = input("Enter your name: ")
    client_socket.send(name.encode())
    response = client_socket.recv(1024).decode()
    if response == 'ok':
        print("Name accepted")
        break
    else:
        print("Name already taken, please enter a different name.")

def receive_messages():
    while True:
        # Receive and decrypt messages from the server
        message = client_socket.recv(1024)
        decrypted_message = cipher_suite.decrypt(message).decode()
        # use curses to move the cursor down and print the message
        curses.initscr()
        curses.endwin()
        print(decrypted_message)
        curses.initscr()
        curses.move(1,0)

# start a new thread for receiving messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True:
    # Get user input for the message
    message = input("Enter your message: ")
    if message == "exit" or message == "disconnect":
        client_socket.send(cipher_suite.encrypt("disconnect".encode()))
        client_socket.close()
        receive_thread.join()
        break
    # Encrypt the message and send it to the server
    encrypted_message = cipher_suite.encrypt(message.encode())
    client_socket.send(encrypted_message)

