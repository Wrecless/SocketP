import rsa

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
    return rsa.sign(message.encode('ascii'), key, 'SHA-1')

def verify_signature(message, signature, key):
    try:
        return rsa.verify(message.encode('ascii'), signature, key) == 'SHA-1'
    except:
        return False

generate_keys()
pubKey, privKey = load_keys()

message = input("Enter message: ")
ciphertext = encrypt_message(message, pubKey)

sign_message(message, privKey)

signature = sign_message(message, privKey)

#receive on the other side
plaintext = decrypt_message(ciphertext, privKey)
print(f"Decrypted message: {ciphertext}")
print(f"Signature verified: {signature}")

if plaintext:
    print(f"Message received: {plaintext}")
else:
    print("unable to decrypt message")

if verify_signature(plaintext, signature, pubKey):
    print("Signature verified!")
else:
    print("Invalid signature!")
