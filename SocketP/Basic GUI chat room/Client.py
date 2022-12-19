import tkinter, socket, threading
from tkinter import DISABLED, VERTICAL, NORMAL, END, Y, LEFT, RIGHT, BOTH, TOP, BOTTOM, X, YES, NO, W, E, S, N, messagebox

#define window
root = tkinter.Tk()
root.title("Chat Room")
root.iconbitmap("Message_Icon.ico")
root.geometry("600x600")
root.resizable(False, False)

#define fontsd and colors
my_font = ("Helvetica", 16)
black = "black"
light_green = "green"
root.config(bg=black)

#define socket consts
ENCODER = "utf-8"
BYTESIZE = 1024
global client_socket


#define functions
def connect():
    '''Connect to server'''
    global client_socket

    #clear previous chars
    my_listbox.delete(0, END)

    #get connection info
    name = name_entry.get()
    ip = ip_entry.get()
    port = port_entry.get()

    #only try to connect if all fields are filled
    if name and ip and port:
        #if conditions are meet
        my_listbox.insert(0, f"{name} is trying to connect to {ip}:{port}")

        #creates cliente socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, int(port)))

        #verify connection
        verify_connection(name)
    else:
        #if conditions are not meet
        my_listbox.insert(0, "Please fill all fields")
        messagebox.showerror("Error", "Please fill all fields")


def verify_connection(name):
    '''Verify connection to server'''
    global client_socket

    #server sends a name flag
    flag = client_socket.recv(BYTESIZE).decode(ENCODER)
    if flag == "NAME":
        #check
        client_socket.send(name.encode(ENCODER))
        message = client_socket.recv(BYTESIZE).decode(ENCODER)

        if message:
            #server sent verification
            my_listbox.insert(0, message)
            #button functions
            connect_button.config(state=DISABLED)
            disconnect_button.config(state=NORMAL)
            send_button.config(state=NORMAL)

            name_entry.config(state=DISABLED)
            ip_entry.config(state=DISABLED)
            port_entry.config(state=DISABLED)

            #create a thread to receive constantly messages from server
            receive_thread = threading.Thread(target=receive_message)
            receive_thread.start()
        else:
            #no verification
            my_listbox.insert(0, "Connection not verified")
            client_socket.close()

    else:
        my_listbox.insert(0, "Connection refused. BYYEEEEE")
        client_socket.close()



def disconnect():
    '''Disconnect from server'''
    pass



def send_message():
    '''Send message to server'''
    pass

def receive_message():
    '''Receive message from server'''
    pass

def security_check():
    '''Check for security issues'''
    pass

#define GUI
info_frame = tkinter.Frame(root, bg=black)
output_frame = tkinter.Frame(root, bg=black)
input_frame = tkinter.Frame(root, bg=black)
info_frame.pack(pady=10)
output_frame.pack(pady=10)
input_frame.pack(pady=10)
#create frames
name_label = tkinter.Label(info_frame, text="Name: ", font=my_font, bg=black, fg=light_green)
name_entry = tkinter.Entry(info_frame, font=my_font, width=20, bg="white")
ip_label = tkinter.Label(info_frame, text="Host IP: ", font=my_font, bg=black, fg=light_green)
ip_entry = tkinter.Entry(info_frame, font=my_font, width=20, bg="white")
port_label = tkinter.Label(info_frame, text="Port num: ", font=my_font, bg=black, fg=light_green)
port_entry = tkinter.Entry(info_frame, font=my_font, width=10, bg="white")
connect_button = tkinter.Button(info_frame, text="Connect", font=my_font, bg=light_green, fg=black, borderwidth=5, command=connect)
disconnect_button = tkinter.Button(info_frame, text="Disconnect", font=my_font, bg=light_green, fg=black, borderwidth=5)

name_entry.grid(row=0, column=1, padx=5, pady=5)
name_label.grid(row=0, column=0, padx=5, pady=5)
port_label.grid(row=0, column=2, padx=5, pady=5)
port_entry.grid(row=0, column=3, padx=5, pady=5)
ip_label.grid(row=1, column=0, padx=5, pady=5)
ip_entry.grid(row=1, column=1, padx=5, pady=5)
connect_button.grid(row=1, column=2, padx=5, pady=5)
disconnect_button.grid(row=1, column=3, padx=5, pady=5)

#output frame
my_scrollbar = tkinter.Scrollbar(output_frame, orient=VERTICAL)
my_listbox = tkinter.Listbox(output_frame, width=47, height=15, borderwidth=3, font=my_font, yscrollcommand=my_scrollbar.set)
my_scrollbar.config(command=my_listbox.yview)

my_listbox.grid(row=0, column=0)
my_scrollbar.grid(row=0, column=1, sticky="NS")

#input frame
input_entry = tkinter.Entry(input_frame, width=40, borderwidth=3, font=my_font)
send_button = tkinter.Button(input_frame, text="Send", font=my_font, bg=light_green, fg=black, borderwidth=5, state=DISABLED)
input_entry.grid(row=0, column=0, padx=5, pady=5)
send_button.grid(row=0, column=1, padx=5, pady=5)


#run root window's main loop
root.mainloop()