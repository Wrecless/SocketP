#client

import socket

#creates a client side socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

##connects to server
client_socket.connect((socket.gethostbyname(socket.gethostname()), 12345))

#receives message from server
msg = client_socket.recv(1024)
print(msg.decode("utf-8"))

#close connection
client_socket.close()