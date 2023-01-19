#chat server
import socket, rsa
from datetime import datetime
timestamp = 1625309472.357246
date_time = datetime.fromtimestamp(timestamp)
str_time = date_time.strftime("%I:%M.%S")


#define consts
HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT = 5000
BUFFER_SIZE = 1024

#create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen()

#def generate_keys():
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
    return rsa.sign(message.encode('ascii'), key, 'SHA-512')

def verify_signature(message, signature, key):
    try:
        return rsa.verify(message.encode('ascii'), signature, key) == 'SHA-512'
    except:
        return False

generate_keys()
pubKey, privKey = load_keys()

#listen for connections
print("Server is listening for connections...")
client_socket, client_address = server_socket.accept()
welcome = f"Welcome to the server, {client_address}"
welcome = encrypt_message(welcome, pubKey)
client_socket.send(welcome)

#send / receive data
while True:
    #receive data
    message = client_socket.recv(BUFFER_SIZE)
    message = decrypt_message(message, privKey)

    #quit function
    if message == "quit":
        client_socket.send("quit")
        print("Closing connection.")
        break
    else:
        print(f"\n{client_address} at {str_time} sent: {message}")
        message = input("Enter a message: ")
        message = encrypt_message(message, pubKey)
        client_socket.send(message)

#close connection
client_socket.close()