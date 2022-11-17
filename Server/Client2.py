import socket

HEADER = 64 #how big the message can be
PORT = 5050 #port number
FORMAT = "utf-8" #format of the message
DISCONNECT_MESSAGE = "!DISCONNECT" #message to disconnect
SERVER = "172.27.50.248" #server ip
ADDR = (SERVER, PORT) #address of the server

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT)) #connects to the server

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message) #gets the length of the message
    send_length = str(msg_length).encode(FORMAT) #encodes the length of the message
    send_length += b' ' * (HEADER - len(send_length)) #padding
    client.send(send_length) #sends the length of the message
    client.send(message) #sends the message
    print(client.recv(2048).decode(FORMAT)) #receives the message from the server

send("I'm a client, I'm connected to the server") #sends a message to the server
input("Press Enter to continue: ") #waits for the user to press enter
send("Im the same client, I'm still connected to the server") #sends another message to the server
input("Press Enter to continue: ")
send("Ill disconnect now")
send(DISCONNECT_MESSAGE) #sends a disconnect message to the server

