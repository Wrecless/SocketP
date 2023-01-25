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

def encrypt_caesar(plaintext, shift):
    """Encrypt the string and return the ciphertext"""
    ciphertext = ""
    for char in plaintext:
        if char.isalpha(): #checks if char is a letter
            shift_char = chr((ord(char) + shift - 97) % 26 + 97) # shifts char
            ciphertext += shift_char # adds shifted char to ciphertext
        else:
            ciphertext += char #
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

# receive messages from server
def send_message():
    '''sends messages to server'''
    while True:
        message = input("")
        message = encrypt_caesar(message.lower(), shift)
        client_socket.send(message.encode(ENCODER))

def receive_message():
    '''receives messages from server'''
    while True:
        try:
            #receives message from server
            message = client_socket.recv(BYTESIZE).decode(ENCODER)
            #print(message)
            message = decrypt_caesar(message, shift)
            #print(message)

            #check for name request
            if message == "rqstname":
                name = input("Enter name: ")
                name = encrypt_caesar(name.lower(), shift) #force lowercase
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