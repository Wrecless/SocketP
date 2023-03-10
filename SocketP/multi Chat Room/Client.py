import socket
import threading

# define consts
DEST_IP = socket.gethostbyname(socket.gethostname())
DEST_PORT = 5050
BYTESIZE = 1024
ENCODER = "utf-8"

# create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((DEST_IP, DEST_PORT))

# receive messages from server
def send_message():
    '''sends messages to server'''
    while True:
            message = input("")
            client_socket.send(message.encode(ENCODER))

def receive_message():
    '''receives messages from server'''
    while True:
        try:
            #receives message from server
            message = client_socket.recv(BYTESIZE).decode(ENCODER)

            #check for name request
            if message == "NAME":
                name = input("Enter name: ")
                client_socket.send(name.encode(ENCODER))
            else:
                print(message)

        except:
            print("An error occurred!")
            client_socket.close()
            break

# create threads to receive messages
print("Client is starting...")
receive_thread = threading.Thread(target=receive_message)
send_thread = threading.Thread(target=send_message)

# start threads
receive_thread.start()
send_thread.start()

