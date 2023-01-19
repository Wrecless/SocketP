import socket
import threading
import rsa

# define consts
DEST_IP = socket.gethostbyname(socket.gethostname())
DEST_PORT = 5050
BYTESIZE = 1024
ENCODER = 'ascii'

# create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((DEST_IP, DEST_PORT))

#RSA
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

pubKey, privKey = load_keys()

# receive messages from server
def send_message(encrypt_message):
    '''sends messages to server'''
    while True:
        message = input()
        client_socket.send(encrypt_message(message, pubKey))

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

