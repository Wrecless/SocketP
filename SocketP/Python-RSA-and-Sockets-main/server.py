from RSA import *
from socket import *
serverPort = 1300
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("127.0.0.1",serverPort))
serverSocket.listen(5)
print ("TCP Server Ativo!\n")

connectionSocket, addr = serverSocket.accept()
print("A Conexão do Source Address: " + str(addr) + " Foi Aceita!\n\n")
print("Neste momento as chaves de criptografia estão sendo criadas e trocadas...")
public_key, private_key = generating_keys()
print(f"\nEssa é sua chave pública: {public_key}")
valid_secret_message = private_key_digital_signature(private_key)


#exchanging and validating keys

client_public_key = connectionSocket.recv(65000)
client_public_key_received = eval(client_public_key.decode("utf-8"))
print(f"Chave Pública Recebida: {client_public_key_received}")
connectionSocket.send(str(public_key).encode())
client_valid_secret_message = connectionSocket.recv(65000)
valid_secret_message_received = str(client_valid_secret_message,"utf-8")
is_valid = validating_digital_signature(valid_secret_message_received, client_public_key_received)
print(is_valid)
connectionSocket.send(bytes(str(valid_secret_message), "utf-8"))

connection = True
msg_number = 1
while connection:

    sentence = connectionSocket.recv(65000)
    received = str(sentence,"utf-8")
    received = decrypt(received, private_key)

    if received == "FIN":
        fin = encrypt("Pedido para finalizar a conexão recebido\n\nFinalizando a conexão :D", client_public_key_received)
        connectionSocket.send(bytes(str(fin), "utf-8"))
        print("\nO cliente solicitou o fim da conexão :D")
        connection = False
        break

    print ("Mensagem do Cliente:", received)

    confirm_msg = encrypt(f"Mensagem numero {msg_number} recebida com sucesso!", client_public_key_received)

    connectionSocket.send(bytes(str(confirm_msg), "utf-8"))

    msg_number += 1

connectionSocket.close() 