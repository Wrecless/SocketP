import socket
import threading

HEADER = 64 #how big the message can be
PORT = 5050 #port number

# Server
#SERVER = "172.27.50.248"
SERVER = socket.gethostbyname(socket.gethostname()) # Client
print(SERVER)
print(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) #recevies messages from the server
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE: #if the message is disconnect, then the server will disconnect
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")#prints the server ip
    while True:
        conn, addr = server.accept() #accepts the connection
        thread = threading.Thread(target=handle_client, args=(conn, addr)) #creates a thread for each client
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()
