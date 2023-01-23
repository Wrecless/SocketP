import socket
import threading
import rsa

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

pubKey, privKey = load_keys()



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

#accepts connection
client_socket, client_address = server.accept()
print(f"Connected with {client_address}...")

#receives client info and broadcasts it
clientInfo = client_socket.recv(BYTESIZE).decode(ENCODER)
print (clientInfo)