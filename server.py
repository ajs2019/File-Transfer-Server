import socket
import threading
import pickle

IP = 'localhost'
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen(5)

print(f'Server listening on {IP}:{PORT}')

clients = []

def handle_client(client_socket, client_address):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        request = pickle.loads(data)
        if request['type'] == 'list':
            response = {'type': 'list', 'files': [f.name for f in request['folder'].iterdir()]}
        elif request['type'] == 'download':
            try:
                file = request['folder'].joinpath(request['filename'])
                with file.open('rb') as f:
                    response = {'type': 'download', 'data': f.read()}
            except FileNotFoundError:
                response = {'type': 'error', 'message': 'File not found'}
        else:
            response = {'type': 'error', 'message': 'Invalid request type'}
        client_socket.send(pickle.dumps(response))
    client_socket.close()
    clients.remove(client_socket)

while True:
    client_socket, client_address = server_socket.accept()
    print(f'Accepted connection from {client_address[0]}:{client_address[1]}')
    clients.append(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()

server_socket.close()