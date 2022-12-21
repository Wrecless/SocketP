import tkinter, socket, threading, json
from tkinter import DISABLED, VERTICAL, NORMAL, END, Y, LEFT, RIGHT, BOTH, TOP, BOTTOM, X, YES, NO, W, E, S, N, messagebox, StringVar


# define window
root = tkinter.Tk()
root.title("Chat Room")
root.iconbitmap("Message_Icon.ico")
root.geometry("600x600")
root.resizable(False, False)

# define fonts and colors
my_font = ("Helvetica", 16)
black = "black"
green = "green"
root.config(bg=black)

#create connection class for the server socket
class Connection:
    def __init__(self, client, address):
        self.client = client
        self.address = address
        self.username = None
        self.color = None

# define functions
def start_server(connection):
    '''Start the server'''
    pass

def end_server(connection):
    '''End the server'''
    pass

def connect_client(connection):
    '''Connect to server'''
    pass

def create_message(flag, name, message, color):
    '''return message to client'''
    pass

def process_message(connection, message_json, client_socket, client_address=(0,0)):
    '''Process message from client'''
    pass

def broadcast_message(connection, message_json):
    '''Broadcast message to all clients'''
    pass

def receive_message(connection, cliente_socket):
    '''Receive message from client'''
    pass

def self_broadcast_message(connection):
    '''Broadcast message to all clients'''
    pass

def private_message(connection):
    '''Send message to specific client'''
    pass

def kick_client(connection):
    '''Kick client from server'''
    pass

def ban_client(connection):
    '''Ban client from server'''
    pass

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
port_entry = tkinter.Entry(connection_frame, font=my_font, width=10, bg=black, fg=green, borderwidth=5)
start_button = tkinter.Button(connection_frame, text="Start Server", font=my_font, bg=black, fg=green, width=10, borderwidth=5)
end_button = tkinter.Button(connection_frame, text="End", font=my_font, bg=black, fg=green, width=9, borderwidth=5, state=DISABLED)

#grid connection frame
port_label.grid(row=0, column=0, padx=2, pady=5)
port_entry.grid(row=0, column=1, padx=2, pady=5)
start_button.grid(row=0, column=2, padx=5, pady=5)
end_button.grid(row=0, column=3, padx=5, pady=5)

#history frame
history_scrollbar = tkinter.Scrollbar(history_frame)
history_listbox = tkinter.Listbox(history_frame, width=47, height=9, font=my_font, bg=black, fg=green, yscrollcommand=history_scrollbar.set)
history_scrollbar.config(command=history_listbox.yview)

history_listbox.grid(row=0, column=0)
history_scrollbar.grid(row=0, column=1, sticky=N+S)

#client frame
client_scrollbar = tkinter.Scrollbar(history_frame)
client_listbox = tkinter.Listbox(history_frame, width=47, height=9, font=my_font, bg=black, fg=green, yscrollcommand=client_scrollbar.set)
client_scrollbar.config(command=history_listbox.yview)

client_listbox.grid(row=1, column=0, pady=5)
client_scrollbar.grid(row=1, column=1, sticky=N+S)

#message frame
input_entry = tkinter.Entry(message_frame, font=my_font, width=30, bg=black, fg=green, borderwidth=5)
self_broadcast_button = tkinter.Button(message_frame, text="Self Broadcast", font=my_font, bg=black, fg=green, width=15, borderwidth=5, state=DISABLED)

#grid message frame
input_entry.grid(row=0, column=0, padx=5, pady=5)
self_broadcast_button.grid(row=0, column=1, padx=5, pady=5)

#admin frame
message_button = tkinter.Button(admin_frame, text="Message", font=my_font, bg=black, fg=green, width=10, borderwidth=5, state=DISABLED)
kick_button = tkinter.Button(admin_frame, text="Kick", font=my_font, bg=black, fg=green, width=10, borderwidth=5, state=DISABLED)
ban_button = tkinter.Button(admin_frame, text="Ban", font=my_font, bg=black, fg=green, width=10, borderwidth=5, state=DISABLED)

#grid admin frame
message_button.grid(row=0, column=0, padx=5, pady=5)
kick_button.grid(row=0, column=1, padx=5, pady=5)
ban_button.grid(row=0, column=2, padx=5, pady=5)



# run program
root.mainloop()