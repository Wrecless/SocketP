#chat server
import socket

#define consts
HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT = 5000
BUFFER_SIZE = 1024
ENCODER = "utf-8"

#create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen()

#listen for connections
print("Server is listening for connections...")
client_socket, client_address = server_socket.accept()
client_socket.send("Welcome to the chat server!\n".encode(ENCODER))

#send / receive data
while True:
    #receive data
    message = client_socket.recv(BUFFER_SIZE).decode(ENCODER)

    #quit function
    if message == "quit":
        client_socket.send("quit".encode(ENCODER))
        print("Closing connection.")
        break
    else:
        print(f"\n{client_address} sent: {message}")
        message = input("Enter a message: ")
        client_socket.send(message.encode(ENCODER))

#close connection
client_socket.close()
