#udp server side
import socket

#create a server side socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#binds new socket
server_socket.bind((socket.gethostbyname(socket.gethostname()), 12345))

#UDP doesn't need to listen
message, address = server_socket.recvfrom(1024)
print(message.decode("utf-8"))
print(address)
