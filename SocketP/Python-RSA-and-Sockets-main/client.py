from RSA import *
import socket

connection = True

target_host = "192.168.0.21"
target_port = 1300

#create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))
print("Conexão Ativa!\n\n")
print("Neste momento as chaves de criptografia estão sendo criadas e trocadas...")
public_key, private_key = generating_keys()
print(f"\nEssa é sua chave pública: {public_key}")
valid_secret_message = private_key_digital_signature(private_key)


#exchanging and validating keys

client.send(str(public_key).encode()) #enviando minha chave pública
server_public_key_received = client.recv(65000)
server_public_key = eval(server_public_key_received.decode("utf-8"))
print(f"Chave Pública Recebida: {server_public_key}") #exibindo chave pública recebida da conexão
client.send(bytes(str(valid_secret_message), "utf-8")) #enviando mensagem para validar chave pública
server_valid_secret_message = client.recv(65000)
valid_secret_message_received = str(server_valid_secret_message,"utf-8")
is_valid = validating_digital_signature(valid_secret_message_received, server_public_key)
print(is_valid)


while connection:

    #connect the client
    data_flow = input("")
    if data_flow == "FIN":
        data_flow = encrypt(data_flow, server_public_key)
        #send some data
        client.send(bytes(data_flow, "utf-8"))
        response = client.recv(65000)
        response = str(response,"utf-8")
        response = decrypt(response, private_key)
        print(response)
        client.close()
        break

    data_flow = encrypt(data_flow, server_public_key)
    #send some data
    client.send(bytes(data_flow, "utf-8"))

    #receive some data
    try:
        response = client.recv(65000)
        response = str(response,"utf-8")
        response = decrypt(response, private_key)
        print(response)
        

    except:
        pass  