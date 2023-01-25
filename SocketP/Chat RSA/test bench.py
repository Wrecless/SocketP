import socket, threading, time, rsa

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

# example usage
plaintext = "name"
shift = 3
ciphertext = encrypt_caesar(plaintext, shift)
print("Ciphertext: ", ciphertext)
print(type(ciphertext))
decrypted_text = decrypt_caesar(ciphertext, shift)
print("Decrypted text: ", decrypted_text)
print(type(decrypted_text))

"""
import socket

def send_message(message, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(message.encode())

def receive_message(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(data.decode())

# encrypt the message
plaintext = "hello world"
shift = 3
ciphertext = encrypt_caesar(plaintext, shift)

# send the message
send_message(ciphertext, "127.0.0.1", 1234)

# receive the message
receive_message("127.0.0.1", 1234)
"""
27052009