#client side
import socket


# define consts
DEST_IP = socket.gethostbyname(socket.gethostname())
DEST_PORT = 5000
BUFFER_SIZE = 1024
ENCODER = "ascii"

# create a client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((DEST_IP, DEST_PORT))

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
        print(f"\n{message}")
        message = input("Enter a message: ")
        client_socket.send(message.encode(ENCODER))

#close connection
client_socket.close()

