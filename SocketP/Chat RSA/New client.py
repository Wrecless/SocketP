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


# define consts
DEST_IP = socket.gethostbyname(socket.gethostname())
DEST_PORT = 5050
BYTESIZE = 1024
ENCODER = "utf-8"

# create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((DEST_IP, DEST_PORT))

#message = client_socket.recv(BYTESIZE).decode(ENCODER)
MESSAGE = "Hello World"
MESSAGE_ENCRYPTED = encrypt_message(MESSAGE, pubKey)
STATE = 2

msg_packet = [MESSAGE, MESSAGE_ENCRYPTED, STATE]
print (type(msg_packet))
msg_send = client_socket.send(msg_packet.encode(ENCODER))