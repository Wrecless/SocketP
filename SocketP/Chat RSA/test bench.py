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

MESSAGE = "Hello World"
MESSAGE_ENCRYPTED = encrypt_message(MESSAGE, pubKey)
STATE = 2

msg_packet = [MESSAGE, MESSAGE_ENCRYPTED, STATE]

print(msg_packet)

msg_packet.encode('utf-8')
print(msg_packet)
msg_packet.decode('utf-8')
print(msg_packet)
msg_encrypted = msg_packet[1]
print(msg_encrypted)
msg_decrypted = decrypt_message(msg_encrypted, privKey)
print(msg_decrypted)