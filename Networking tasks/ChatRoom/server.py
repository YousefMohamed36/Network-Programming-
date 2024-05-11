import socket
import threading

# Connection Data
server_host = '127.0.0.1'
server_port = 7000

# Starting Server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_host, server_port))
server_socket.listen()

# Lists For Clients and Their Nicknames
client_sockets = []
client_nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message, current_socket):
    for client_socket in client_sockets:
        if client_socket == current_socket:
            continue
        client_socket.send(message)

# Handling Messages From Clients
def handle(client_socket):
    while True:
        try:
            # Broadcasting Messages
            message = client_socket.recv(1024)
            broadcast(message, client_socket)
        except:
            # Removing And Closing Clients
            index = client_sockets.index(client_socket)
            client_sockets.remove(client_socket)
            client_socket.close()
            nickname = client_nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'), client_socket)
            client_nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client_socket, address = server_socket.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client_socket.send('NICK'.encode('ascii'))
        nickname = client_socket.recv(1024).decode('ascii')
        client_nicknames.append(nickname)
        client_sockets.append(client_socket)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'), client_socket)
        client_socket.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client_socket,))
        thread.start()

receive()
