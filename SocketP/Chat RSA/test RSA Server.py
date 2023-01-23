import socket
import threading
import rsa
import time


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

def generate_keys():
    (pubKey, privKey) = rsa.newkeys(2048)
    with open ("keys/pubkey.pem", "wb") as f:
        f.write(pubKey.save_pkcs1("PEM"))

    with open ("keys/privkey.pem", "wb") as f:
        f.write(privKey.save_pkcs1("PEM"))

def load_keys():
    with open("keys/pubkey.pem", "rb") as f:
        pubKey = rsa.PublicKey.load_pkcs1(f.read())

    with open("keys/privkey.pem", "rb") as f:
        privKey = rsa.PrivateKey.load_pkcs1(f.read())

    return (pubKey, privKey)

def encrypt_message(message, key):
    return rsa.encrypt(message.encode('ascii'), key)

def decrypt_message(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key).decode('ascii')
    except:
        return False


def sign_message(message, key):
    return rsa.sign(message.encode('ascii'), key, 'SHA-1')

def verify_signature(message, signature, key):
    try:
        return rsa.verify(message.encode('ascii'), signature, key) == 'SHA-1'
    except:
        return False

generate_keys()
pubKey, privKey = load_keys()

#broadcasts messages to all clients
def broadcast(message):
    '''broadcasts messages to all clients'''
    for client in clients_Socket_List:
        client.send(message)

def receive_messages(client_socket):
    '''receives messages from clients'''
    while True:
        try:
            current_time = time.strftime("%H:%M:%S", time.localtime())
            #gets name of client
            index = clients_Socket_List.index(client_socket)
            name = clients_Name_List[index]

            #receives message from client
            message = client_socket.recv(BYTESIZE)
            message = decrypt_message(message, privKey)

            """
                if message == "QUIT":
                QUIT = "QUIT"
                QUIT = encrypt_message(QUIT, pubKey)
                client_socket.send(QUIT)
                break
            """
            message = f"{current_time} - {name}: {message}"
            message = encrypt_message(message, pubKey)
            broadcast(message)

        except:
            #finds index of client
            index = clients_Socket_List.index(client_socket)
            name = clients_Name_List[index]

            #broadcast to everyone
            left = f"{name} has left the chat"
            left = encrypt_message(left, pubKey)
            broadcast(left)

            #removes client from list
            clients_Socket_List.remove(client_socket)
            clients_Name_List.remove(name)
            client_socket.close()

            #removes client from chat
            break


def connect_clients():
    '''handles clients'''
    while True:
        #accepts connection
        client_socket, client_address = server.accept()
        print(f"Connected with {client_address}...")

        #gets name of client
        nick = "NICK"
        nick = encrypt_message(nick, pubKey)
        client_socket.send(nick)
        client_Name = client_socket.recv(BYTESIZE)
        client_Name = decrypt_message(client_Name, privKey)

        #stores name & IP of client
        clients_Name_List.append(client_Name)
        clients_Socket_List.append(client_socket)

        #prints name & IP of client
        print(f"Name of client is {client_Name}") #server
        #connected = f"{client_Name}, Connected to server"
        #connected = encrypt_message(connected, pubKey)
        #client_socket.send(connected) #client
        broadcast_join = f"{client_Name} has joined the chat"
        broadcast_join = encrypt_message(broadcast_join, pubKey)
        broadcast(broadcast_join) #server

        #creates thread to handle client
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,)) #NEEDS THE COMMA!!!
        receive_thread.start()

#starts server
print("Server is starting...")
connect_clients()