import socket
import threading
import pickle
import os

IP = 'localhost'
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

def receive_data():
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response = pickle.loads(data)
        if response['type'] == 'list':
            for file in response['files']:
                print(file)
        elif response['type'] == 'download':
            with open(response['filename'], 'wb') as f:
                f.write(response['data'])
            print(f'Downloaded {response["filename"]}')
        elif response['type'] == 'error':
            print(f'Error: {response["message"]}')

receive_thread = threading.Thread(target=receive_data)
receive_thread.start()

while True:
    command = input('Enter command: ')
    parts = command.split()
    if not command or parts[0] == 'quit':
        break