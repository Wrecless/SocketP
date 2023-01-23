import rsa, json
from datetime import datetime
timestamp = 1625309472.357246
date_time = datetime.fromtimestamp(timestamp)
str_time = date_time.strftime("%I:%M.%S")

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
    return str(rsa.encrypt(message.encode('ascii'), key))

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

generate_keys()
pubKey, privKey = load_keys()

name = "Bruno"
print(type(name))
name_encrypted = encrypt_message(name, pubKey)
print(type(name_encrypted))
name_decrypted = decrypt_message(name_encrypted, privKey)
print(type(name_decrypted))
print(name_decrypted)

print(name_encrypted)
print(type(name_encrypted))
"""
name_encrypted_string = str(name_encrypted)
print(name_encrypted_string)
print(type(name_encrypted_string))
name_encrypted_bytes = bytes(name_encrypted_string, 'utf-8')
print(name_encrypted_bytes)
print(type(name_encrypted_bytes))
name_decrypted_string = decrypt_message(name_encrypted_bytes, privKey)
print(name_decrypted_string)
print(type(name_decrypted_string))
"""

message_packet = {
    "flag": "flag",
    "name": name_encrypted,
    "message": "message",
    "color": "color",
    "timestamp": str_time,
}

encrypted_json_message = json.dumps(message_packet)
print(encrypted_json_message)
decrypted_json_message = json.loads(encrypted_json_message)
print(decrypted_json_message)

























