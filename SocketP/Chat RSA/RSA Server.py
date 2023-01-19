import socket
import threading
import rsa

#define consts
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
BYTESIZE = 1024
ENCODER = 'ascii'


#create socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

#stores all the clients
clients_Socket_List = []
clients_Name_List = []

def generate_keys():
    (pubKey, privKey) = rsa.newkeys(1024)
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


#broadcasts messages to all clients
def broadcast(message):
    '''broadcasts messages to all clients'''
    for client in clients_Socket_List:
        client.send(message)

def receive_messages(client_socket, decrypt_message):
    '''receives messages from clients'''
    while True:
        try:
            #gets name of client
            index = clients_Socket_List.index(client_socket)
            name = clients_Name_List[index]

            #receives message from client
            message = client_socket.recv(BYTESIZE).decode(ENCODER)
            print(message)
            message = f"{name}: {message}".encode(ENCODER)
            print(message)
            broadcast(message)
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
            broadcast(f"{name} has left the chat".encode(ENCODER)) #red / blinking
            break

def connect_clients():
    '''handles clients'''
    while True:
        #accepts connection
        client_socket, client_address = server.accept()
        print(f"Connected with {client_address}...")

        #gets name of client
        client_socket.send("NAME".encode(ENCODER))
        client_Name = client_socket.recv(BYTESIZE).decode(ENCODER)

        #stores name & IP of client
        clients_Name_List.append(client_Name)
        clients_Socket_List.append(client_socket)

        #prints name & IP of client
        print(f"Name of client is {client_Name}\n") #server
        client_socket.send(f"{client_Name}, Connected to server".encode(ENCODER)) #client
        broadcast(f"{client_Name} has joined the chat\n".encode(ENCODER)) #server

        #creates thread to handle client
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,)) #NEEDS THE COMMA!!!
        receive_thread.start()

#starts server
print("Server is starting...")
connect_clients()
generate_keys()
pubKey, privKey = load_keys()