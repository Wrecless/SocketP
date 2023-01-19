#client side
import socket, rsa


# define consts
DEST_IP = socket.gethostbyname(socket.gethostname())
DEST_PORT = 5000
BUFFER_SIZE = 1024
ENCODER = "ascii"

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


# create a client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((DEST_IP, DEST_PORT))

#send / receive data
while True:
    #receive data
    message = client_socket.recv(BUFFER_SIZE)
    message = decrypt_message(message, privKey)


    #quit function
    if message == "quit":
        client_socket.send("quit".encode(ENCODER))
        print("Closing connection.")
        break
    else:
        print(f"\n{message}")
        message = input("Enter a message: ")
        message = encrypt_message(message, pubKey)
        client_socket.send(message)

#close connection
client_socket.close()