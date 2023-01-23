import socket
import threading
import rsa

# define consts
DEST_IP = socket.gethostbyname(socket.gethostname())
DEST_PORT = 5050
BYTESIZE = 1024
ENCODER = "utf-8"

# create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((DEST_IP, DEST_PORT))

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

# receive messages from server
def send_message():
    '''sends messages to server'''
    while True:
        message = input("")

        if message == "QUIT":
            #print ("You have been disconnected from the server!")
            client_socket.close()
            break

        message = encrypt_message(message, pubKey)
        client_socket.send(message)

def receive_message():
    '''receives messages from server'''
    while True:
        try:
            #receives message from server
            message = client_socket.recv(BYTESIZE)
            message = decrypt_message(message, privKey)

            if message == "NICK":
                nick = input("Choose a nickname: ")
                nick = encrypt_message(nick, pubKey)
                client_socket.send(nick)

            #elif message == "NICK_TAKEN":
                #nick = input("Nickname is taken! Choose another one: ")
                #nick = encrypt_message(nick, pubKey)
                #client_socket.send(nick)

            else:
                print(message)

        except:
            print("You are being Disconnect from the server!")
            client_socket.close()
            break

# create threads to receive messages
print("Client is starting...")
receive_thread = threading.Thread(target=receive_message)
send_thread = threading.Thread(target=send_message)

# start threads
receive_thread.start()
send_thread.start()