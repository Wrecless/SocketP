import tkinter, socket, threading, json
from tkinter import DISABLED, NORMAL, END, VERTICAL

# define window
root = tkinter.Tk()
root.title("Chat Room")
root.iconbitmap("Message_Icon.ico")
root.geometry("600x660")
root.resizable(False, False)

# define fonts and colors
my_font = ("Helvetica", 16)
black = "black"
green = "green"
red = "red"
root.config(bg=black)

# define functions
#creates a connection class to hold the server socket
class Connection():
    def __init__(self):
        self.host_ip = socket.gethostbyname(socket.gethostname())
        self.encoder = 'utf-8'
        self.bytesize = 1024
        #stores the client socket and banned status
        self.client_sockets = []
        self.client_ips = []
        self.banned_ips = []

def start_server(connection):
    '''Start the server'''
    #get port number to run
    connection.port = int(port_entry.get())
    #create server socket
    connection.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #bind server socket to port
    connection.server_socket.bind((connection.host_ip, connection.port))
    #listen for connections
    connection.server_socket.listen()

    #update GUI
    history_listbox.delete(0, END)
    history_listbox.insert(0, f"Server started on port {connection.port}")
    #config buttons
    end_button.config(state=NORMAL)
    self_broadcast_button.config(state=NORMAL)
    message_button.config(state=NORMAL)
    kick_button.config(state=NORMAL)
    ban_button.config(state=NORMAL)
    start_button.config(state=DISABLED)

    #start a thread to accept connections
    connect_thread = threading.Thread(target=connect_client, args=(connection,)) #NEEDS COMMA!
    connect_thread.start()

def end_server(connection):
    '''End the server'''
    message_packet = create_message("DISCONNECT", "Admin (broadcast)", "Server is shutting down", red)
    message_json = json.dumps(message_packet)
    broadcast_message(connection, message_json.encode(connection.encoder))
    #update GUI
    history_listbox.insert(0, f"Server stopped on port {connection.port}")
    end_button.config(state=DISABLED)
    self_broadcast_button.config(state=DISABLED)
    message_button.config(state=DISABLED)
    kick_button.config(state=DISABLED)
    ban_button.config(state=DISABLED)
    start_button.config(state=NORMAL)

    #close all connections
    connection.server_socket.close()

def connect_client(connection):
    '''Connect to server'''
    while True:
        try:
            #accept connection
            client_socket, client_address = connection.server_socket.accept()
            #check if its banned
            if client_address[0] in connection.banned_ips:
                #send ban message
                message_packet = create_message("DISCONNECT", "Admin (private)", "You are banned from this server", red)
                message_json = json.dumps(message_packet)
                client_socket.send(message_json.encode(connection.encoder))
                #close connection
                client_socket.close()
            else:
                #Send a message packet to the client
                message_packet = create_message("INFO", "Admin (private)", "Please send your name", red)
                message_json = json.dumps(message_packet)
                client_socket.send(message_json.encode(connection.encoder))

                #wait for confirmation
                message_json = client_socket.recv(connection.bytesize)
                process_message(connection, message_json,client_socket, client_address)

        except:
            break

def create_message(flag, name, message, color):
    '''return message to client'''
    message_packet = {
        "flag": flag,
        "name": name,
        "message": message,
        "color": color,
    }
    return message_packet

def process_message(connection, message_json, client_socket, client_address=(0,0)):
    '''Process message from client'''
    message_packet = json.loads(message_json) #converts json to dictionary
    flag = message_packet["flag"]
    name = message_packet["name"]
    message = message_packet["message"]
    color = message_packet["color"]
    #idtag

    if flag == "INFO":
        #check the flag
        connection.client_sockets.append(client_socket)
        connection.client_ips.append(client_address[0])
        #broadcast message that a user has joined
        message_packet = create_message("MESSAGE", "Admin (broadcast)", f"{name} has joined the chat", green)
        message_json = json.dumps(message_packet)
        broadcast_message(connection, message_json.encode(connection.encoder))

        #UPDATE SERVER UI
        client_listbox.insert(END, f"{name} IP:{client_address[0]} has joined the chat") #display name and ip on the admin side

        #now that a client has been established, send a message to the client
        receive_thread = threading.Thread(target=receive_message, args=(connection, client_socket,)) #NEEDS COMMA!
        receive_thread.start()

    elif flag == "MESSAGE":
        #broadcast message to all clients
        broadcast_message(connection, message_json)
        #update server UI
        history_listbox.insert(0, f"{name}: {message}")
        history_listbox.itemconfig(0, fg=color)

    elif flag == "DISCONNECT":
        #close socket
        index = connection.client_sockets.index(client_socket)
        connection.client_sockets.remove(client_socket)
        connection.client_ips.pop(index)
        client_listbox.delete(index)
        client_socket.close()
        #broadcast message to all clients
        message_packet = create_message("MESSAGE", "Admin (broadcast)", f"{name} has left the chat", red)
        message_json = json.dumps(message_packet)
        broadcast_message(connection, message_json.encode(connection.encoder))
        #update server UI
        history_listbox.insert(END, f"{name} has left the chat")

    else:
        #catch for errors
        history_listbox.insert(0, "Error: Invalid flag")
        pass

def broadcast_message(connection, message_json):
    '''Broadcast message to all clients'''
    #ALL MESSAGES ARE ENCODED IN JSON
    for client_socket in connection.client_sockets:
        client_socket.send(message_json)

def receive_message(connection, client_socket):
    '''Receive message from client'''
    while True:
        try:
            #receive message
            message_json = client_socket.recv(connection.bytesize)
            process_message(connection, message_json, client_socket)
        except:
            break

def self_broadcast_message(connection):
    '''Broadcast message to all clients'''
    message_packet = create_message("MESSAGE", "Admin (broadcast)", input_entry.get(), green)
    message_json = json.dumps(message_packet)
    broadcast_message(connection, message_json.encode(connection.encoder))

    #clear message box
    input_entry.delete(0, END)

def private_message(connection):
    '''Send message to specific client'''
    #select from listbox
    index = client_listbox.curselection()[0]
    client_socket = connection.client_sockets[index]
    #send message
    message_packet = create_message("MESSAGE", "Admin (private)", input_entry.get(), green)
    message_json = json.dumps(message_packet)
    client_socket.send(message_json.encode(connection.encoder))

    input_entry.delete(0, END)

def kick_client(connection):
    '''Kick client from server'''
    index = client_listbox.curselection()[0]
    client_socket = connection.client_sockets[index]
    #send message
    message_packet = create_message("DISCONNECT", "Admin (private)", "You have been kicked from the server", red)
    message_json = json.dumps(message_packet)
    client_socket.send(message_json.encode(connection.encoder))
    #close socket


def ban_client(connection):
    '''Ban client from server'''
    index = client_listbox.curselection()[0]
    client_socket = connection.client_sockets[index]
    #send message
    message_packet = create_message("DISCONNECT", "Admin (private)", "You have been banned from the server", red)
    message_json = json.dumps(message_packet)
    client_socket.send(message_json.encode(connection.encoder))
    #ban ip
    connection.banned_ips.append(connection.client_ips[index])

#define GUI
connection_frame = tkinter.Frame(root, bg=black)
history_frame = tkinter.Frame(root, bg=black)
client_frame = tkinter.Frame(root, bg=black)
message_frame = tkinter.Frame(root, bg=black)
admin_frame = tkinter.Frame(root, bg=black)

connection_frame.pack(pady=5)
history_frame.pack()
client_frame.pack(pady=5)
message_frame.pack()
admin_frame.pack()

#connection frame
port_label = tkinter.Label(connection_frame, text="Port Number:", font=my_font, bg=black, fg=green)
port_entry = tkinter.Entry(connection_frame, font=my_font, width=10, fg=green, borderwidth=5)
start_button = tkinter.Button(connection_frame, text="Start Server", font=my_font, bg=black, fg=green, width=10, borderwidth=5, command=lambda:start_server(my_connection))
end_button = tkinter.Button(connection_frame, text="End", font=my_font, bg=black, fg=green, width=9, borderwidth=5, state=DISABLED, command=lambda:end_server(my_connection))

#grid connection frame
port_label.grid(row=0, column=0, padx=2, pady=5)
port_entry.grid(row=0, column=1, padx=2, pady=5)
start_button.grid(row=0, column=2, padx=5, pady=5,)
end_button.grid(row=0, column=3, padx=5, pady=5)

#history frame
history_scrollbar = tkinter.Scrollbar(history_frame, orient=VERTICAL)
history_listbox = tkinter.Listbox(history_frame, width=47, height=9, font=my_font, bg=black, fg=green, yscrollcommand=history_scrollbar.set)
history_scrollbar.config(command=history_listbox.yview)

history_listbox.grid(row=0, column=0)
history_scrollbar.grid(row=0, column=1, sticky="NS")

#client frame
client_scrollbar = tkinter.Scrollbar(client_frame, orient=VERTICAL)
client_listbox = tkinter.Listbox(client_frame, width=47, height=9, font=my_font, bg=black, fg=green, yscrollcommand=client_scrollbar.set)
client_scrollbar.config(command=client_listbox.yview)

client_listbox.grid(row=1, column=0, pady=5)
client_scrollbar.grid(row=1, column=1, sticky="NS", pady=5)

#message frame
input_entry = tkinter.Entry(message_frame, font=my_font, width=30, fg=green, borderwidth=5)
self_broadcast_button = tkinter.Button(message_frame, text="Admin Send", font=my_font, bg=black, fg=green, width=15, borderwidth=5, state=DISABLED, command=lambda:self_broadcast_message(my_connection))

#grid message frame
input_entry.grid(row=0, column=0, padx=5, pady=5)
self_broadcast_button.grid(row=0, column=1, padx=5, pady=5)

#admin frame
message_button = tkinter.Button(admin_frame, text="PM", font=my_font, bg=black, fg=green, width=10, borderwidth=5, state=DISABLED ,command=lambda:private_message(my_connection))
kick_button = tkinter.Button(admin_frame, text="Kick", font=my_font, bg=black, fg=green, width=10, borderwidth=5, state=DISABLED, command=lambda:kick_client(my_connection))
ban_button = tkinter.Button(admin_frame, text="Ban", font=my_font, bg=black, fg=green, width=10, borderwidth=5, state=DISABLED, command=lambda:ban_client(my_connection))

#grid admin frame
message_button.grid(row=0, column=0, padx=5, pady=5)
kick_button.grid(row=0, column=1, padx=5, pady=5)
ban_button.grid(row=0, column=2, padx=5, pady=5)

# run program
my_connection = Connection()
root.mainloop()