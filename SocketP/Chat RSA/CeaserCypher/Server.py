import socket
import threading

#define consts
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
BYTESIZE = 1024
ENCODER = "utf-8"

#create socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

#stores all the clients
clients_Socket_List = []
clients_Name_List = []

def encrypt_caesar(plaintext, shift):
    """Encrypt the string and return the ciphertext"""
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            shift_char = chr((ord(char) + shift - 97) % 26 + 97)
            ciphertext += shift_char
        else:
            ciphertext += char
    return ciphertext

def decrypt_caesar(ciphertext, shift):
    """Decrypt the string and return the plaintext"""
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            shift_char = chr((ord(char) - shift - 97) % 26 + 97)
            plaintext += shift_char
        else:
            plaintext += char
    return plaintext

shift = 3

#broadcasts messages to all clients
def broadcast(message):
    '''broadcasts messages to all clients'''
    for client in clients_Socket_List:
        client.send(message)

def receive_messages(client_socket):
    '''receives messages from clients'''
    while True:
        try:
            #gets name of client
            index = clients_Socket_List.index(client_socket)
            name = clients_Name_List[index]

            #receives message from client
            message = client_socket.recv(BYTESIZE).decode(ENCODER)
            print(message)
            print(type(message))
            message = decrypt_caesar(message, shift)
            print(message)
            print(type(message))
            message = encrypt_caesar(f"{name} {message}")
            print(message)
            print(type(message))
            broadcast(message.encode(ENCODER))
        except:
            #finds index of client
            index = clients_Socket_List.index(client_socket)
            name = clients_Name_List[index]

            #removes client from list
            clients_Socket_List.remove(client_socket)
            clients_Name_List.remove(name)

            #removes client from chat
            client_socket.close()
            #broadcast to everyone
            left = encrypt_caesar(f"{name} has left the chat", shift)
            broadcast(left.encode(ENCODER))
            break

def connect_clients():
    '''handles clients'''
    while True:
        #accepts connection
        client_socket, client_address = server.accept()
        print(f"Connected with {client_address}...")

        #gets name of client
        NAME = "rqstname"
        NAME = encrypt_caesar(NAME, shift)
        print(NAME)
        client_socket.send(NAME.encode(ENCODER))
        client_Name = client_socket.recv(BYTESIZE).decode(ENCODER)
        client_Name = decrypt_caesar(client_Name, shift)
        print(client_Name)

        #stores name & IP of client
        clients_Name_List.append(client_Name)
        clients_Socket_List.append(client_socket)

        #prints name & IP of client
        print(f"name of client is {client_Name}\n") #server
        #connected = encrypt_caesar(f"{client_Name} has joined the chat", shift)
        #print(connected)
        #client_socket.sendall(connected.encode(ENCODER)) #client
        server_join = encrypt_caesar(f"{client_Name} has joined the chat", shift)
        print(server_join)
        broadcast(server_join.encode(ENCODER)) #server

        #creates thread to handle client
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,)) #NEEDS THE COMMA!!!
        receive_thread.start()

#starts server
print("Server is starting...")
connect_clients()