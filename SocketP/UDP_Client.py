#UDP client
import socket

#creates a client side socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#send information to server
client_socket.sendto("Hello, sexy boi".encode("utf-8"), (socket.gethostbyname(socket.gethostname()), 12345))