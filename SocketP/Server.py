# Server

import socket

# create a server side socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# see how to get ip dynamically
#print(socket.gethostname())
#print(socket.gethostbyname(socket.gethostname()))

# binds new socket
server_socket.bind((socket.gethostbyname(socket.gethostname()), 12345))

# puts the socket to listening mode
server_socket.listen()  # forever

# listen for connections
while True:
    # accepts connection
    client_socket, address = server_socket.accept()
   #print(type(client_socket))
    print(client_socket)
    print(type(client_socket))
    print(client_socket)

    print(f"Connection from {address} has been established!")

    # sends message to client
    client_socket.send(("Welcome to the server!".encode("utf-8")))

    # close connection
    client_socket.close()
