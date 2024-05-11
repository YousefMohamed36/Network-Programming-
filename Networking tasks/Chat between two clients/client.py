# import essential libraries
import socket
import threading

# function to receive messages through socket
def receive_messages(sock):
    while True:
        try:
            size_bytes = sock.recv(8)
            size = int.from_bytes(size_bytes, 'big')
            data = sock.recv(size).decode('utf-8')
            print(data)
        except socket.error:
            break

# function to send messages through socket 
def send_messages(sock):
    while True:
        message = input()
        recipient = input("Enter recipient address (host:port): ")
        data = f"{recipient}:{message}"
        sock.send(len(data).to_bytes(8,'big'))
        sock.send(data.encode('utf-8'))

# function to start chat between 2 clients
def start_chatting():
    server_host = 'localhost'
    server_port = 8000
    
    # make a TCP socket 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port)) # connected to server

    # START receive_thread
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()
    # START send_thread
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()

if __name__ == '__main__':
    # begin chat session 
    start_chatting()
