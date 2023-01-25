import tkinter, socket, json, threading, random
from tkinter import DISABLED, VERTICAL, END, StringVar, NORMAL

#define window
root = tkinter.Tk()
root.title("Chat Room")
root.iconbitmap("Message_Icon.ico")
root.geometry("600x600")
root.resizable(False, False)

#define fonts and colors
my_font = ("Helvetica", 16)
black = "black"
light_green = "#00E53D"
white = "white"
red = "red"
purple = "#800080"
green = "#00FF00"
yellow = "#FFFF00"
orange = "#FFA500"
blue = "#0000FF"
dark_green = "#004913"

root.config(bg=black)

class Connection():
    '''Create connection class for the server socket'''
    def __init__(self):
        self.encoder = "utf-8"
        self.bytesize = 1024

#define functions
def connect(connection):
    '''Connect to server'''
    #clear previous chats
    my_listbox.delete(0, END)
    #get required info
    connection.name = name_entry.get()
    connection.target_ip = ip_entry.get()
    connection.port = port_entry.get()
    connection.color = color.get()
    connection.id = id

    try:
        #create client socket
        connection.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #connect to server
        connection.client_socket.connect((connection.target_ip, int(connection.port)))
        #receive incoming message from server
        message_json = connection.client_socket.recv(connection.bytesize)
        process_message(connection, message_json)
    except:
        my_listbox.insert(0, "Unable to connect to server")

def disconnect(connection):
    '''Disconnect from server'''
    #Create a message packet to be sent
    message_packet = create_message("DISCONNECT", connection.name, "I am leaving.", connection.color, connection.id)
    message_json = json.dumps(message_packet)
    connection.client_socket.send(message_json.encode(connection.encoder))

    #Disable GUI for chat
    gui_end()

def gui_start():
    '''Start GUI'''
    connect_button.config(state=DISABLED)
    disconnect_button.config(state=NORMAL)
    send_button.config(state=NORMAL)
    name_entry.config(state=DISABLED)
    ip_entry.config(state=DISABLED)
    port_entry.config(state=DISABLED)

    for button in color_buttons:
        button.config(state=DISABLED)

def gui_end():
    '''End GUI'''
    connect_button.config(state=NORMAL)
    disconnect_button.config(state=DISABLED)
    send_button.config(state=DISABLED)
    name_entry.config(state=NORMAL)
    ip_entry.config(state=NORMAL)
    port_entry.config(state=NORMAL)

    for button in color_buttons:
        button.config(state=NORMAL)

def create_message(flag, name, message, color, id):
    '''return message to client'''
    message_packet = {
        "flag": flag,
        "name": name,
        "message": message,
        "color": color,
        "id": id
    }

    return message_packet

def process_message(connection, message_json):
    '''Process message from client'''
    #convert json to dict
    message_packet = json.loads(message_json) #converts json to dictionary
    flag = message_packet["flag"]
    name = message_packet["name"]
    message = message_packet["message"]
    color = message_packet["color"]
    id = message_packet["id"]

    if flag == "INFO":
        message_packet = create_message("INFO",connection.name, "joined the chat", connection.color, connection.id)
        message_json = json.dumps(message_packet)
        connection.client_socket.send(message_json.encode(connection.encoder))

        #update GUI functions
        gui_start()

        #create a threat that constantly receives messages
        receive_thread = threading.Thread(target=receive_message, args=(connection,)) #needs comma
        receive_thread.start()

    elif flag == "MESSAGE":
        message = decrypt_caesar(message, shift)
        my_listbox.insert(0, f"ID:{id}-{name}: {message}")
        my_listbox.itemconfig(0, fg=color)

    elif flag == "DISCONNECT":
        #server telling the client to disconnect
        my_listbox.insert(0, f"ID:{id}-{name}: {message}")
        my_listbox.itemconfig(0, fg=color)
        disconnect(connection)


    else:
        #catch errors
        my_listbox.insert(0, "Error: Invalid flag")

def encrypt_caesar(plaintext, shift):
    """Encrypt the string and return the ciphertext"""
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            shift_char = chr((ord(char) + shift - 97) % 26 + 97)
            ciphertext += shift_char
        else:
            ciphertext += char
    return ciphertext

def decrypt_caesar(ciphertext, shift):
    """Decrypt the string and return the plaintext"""
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            shift_char = chr((ord(char) - shift - 97) % 26 + 97)
            plaintext += shift_char
        else:
            plaintext += char
    return plaintext

id = random.randint(1, 999)
shift = 3
print(shift)


def send_message(connection):
    '''Send message to client'''
    input_message = input_entry.get()
    input_message = input_message.lower()
    #print(input_message)
    #encrypt message
    input_message = encrypt_caesar(input_message, shift)
    #print(input_message)
    message_packet = create_message("MESSAGE", connection.name, input_message, connection.color, connection.id)
    print(message_packet)
    message_json = json.dumps(message_packet)
    connection.client_socket.send(message_json.encode(connection.encoder))
    #clear input entry
    input_entry.delete(0, END)


def receive_message(connection):
    '''Receive message from client'''
    while True:
        try:
            message_json = connection.client_socket.recv(connection.bytesize)
            process_message(connection, message_json)
        except:
            my_listbox.insert(0, "Error: Unable to receive message")
            break

#define GUI
info_frame = tkinter.Frame(root, bg=black)
color_frame = tkinter.Frame(root, bg=black)
output_frame = tkinter.Frame(root, bg=black)
input_frame = tkinter.Frame(root, bg=black)

info_frame.pack(pady=5)
color_frame.pack(pady=5)
output_frame.pack(pady=5)
input_frame.pack(pady=5)


#create frames
name_label = tkinter.Label(info_frame, text="Name: ", font=my_font, bg=black, fg=light_green)
name_entry = tkinter.Entry(info_frame, font=my_font, width=20, bg="white")
ip_label = tkinter.Label(info_frame, text="Host IP: ", font=my_font, bg=black, fg=light_green)
ip_entry = tkinter.Entry(info_frame, font=my_font, width=20, bg="white")
port_label = tkinter.Label(info_frame, text="Port num: ", font=my_font, bg=black, fg=light_green)
port_entry = tkinter.Entry(info_frame, font=my_font, width=10, bg="white")
connect_button = tkinter.Button(info_frame, text="Connect", font=my_font, bg=light_green, fg=black, borderwidth=5, command=lambda:connect(my_connection))
disconnect_button = tkinter.Button(info_frame, text="Disconnect", font=my_font, bg=light_green, fg=black, borderwidth=5, state=DISABLED, command=lambda:disconnect(my_connection))

name_entry.grid(row=0, column=1, padx=5, pady=5)
name_label.grid(row=0, column=0, padx=5, pady=5)
port_label.grid(row=0, column=2, padx=5, pady=5)
port_entry.grid(row=0, column=3, padx=5, pady=5)
ip_label.grid(row=1, column=0, padx=5, pady=5)
ip_entry.grid(row=1, column=1, padx=5, pady=1)
connect_button.grid(row=1, column=2, padx=2, pady=1)
disconnect_button.grid(row=1, column=3, padx=2, pady=1)

#Color Frame layout
color = StringVar()
color.set(white)
white_button = tkinter.Radiobutton(color_frame, text="White", font=my_font, bg=black, fg=light_green, variable=color, value=white)
red_button = tkinter.Radiobutton(color_frame, text="Red", font=my_font, bg=black, fg=light_green, variable=color, value=red)
orange_button = tkinter.Radiobutton(color_frame, text="Orange", font=my_font, bg=black, fg=light_green, variable=color, value=orange)
yellow_button = tkinter.Radiobutton(color_frame, text="yellow", font=my_font, bg=black, fg=light_green, variable=color, value=yellow)
green_button = tkinter.Radiobutton(color_frame, text="Green", font=my_font, bg=black, fg=light_green, variable=color, value=green)
blue_button = tkinter.Radiobutton(color_frame, text="Blue", font=my_font, bg=black, fg=light_green, variable=color, value=blue)
purple_button = tkinter.Radiobutton(color_frame, text="Purple", font=my_font, bg=black, fg=light_green, variable=color, value=purple)

color_buttons = [white_button, red_button, orange_button, yellow_button, green_button, blue_button] #purple_button

white_button.grid(row=1, column=0, padx=0, pady=0)
red_button.grid(row=1, column=1, padx=0, pady=0)
orange_button.grid(row=1, column=2, padx=0, pady=0)
yellow_button.grid(row=1, column=3, padx=0, pady=0)
green_button.grid(row=1, column=4, padx=0, pady=0)
blue_button.grid(row=1, column=5, padx=0, pady=0)
purple_button.grid(row=1, column=6, padx=0, pady=0)

#output frame
my_scrollbar = tkinter.Scrollbar(output_frame, orient=VERTICAL)
my_listbox = tkinter.Listbox(output_frame, width=46, height=15, borderwidth=3, font=my_font, yscrollcommand=my_scrollbar.set, bg="black")
my_scrollbar.config(command=my_listbox.yview)

my_listbox.grid(row=0, column=0)
my_scrollbar.grid(row=0, column=1, sticky="NS")

#input frame
input_entry = tkinter.Entry(input_frame, width=40, borderwidth=3, font=my_font)
send_button = tkinter.Button(input_frame, text="Send", font=my_font, bg=light_green, fg=black, borderwidth=5, state=DISABLED, command=lambda:send_message(my_connection))
input_entry.grid(row=0, column=0, padx=5)
send_button.grid(row=0, column=1, padx=5)

#run root window's main loop
my_connection = Connection()
root.mainloop()