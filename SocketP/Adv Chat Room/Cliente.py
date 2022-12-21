import tkinter, socket, threading
from tkinter import DISABLED, VERTICAL, NORMAL, END, Y, LEFT, RIGHT, BOTH, TOP, BOTTOM, X, YES, NO, W, E, S, N, messagebox, StringVar

#define window
root = tkinter.Tk()
root.title("Chat Room")
root.iconbitmap("Message_Icon.ico")
root.geometry("600x600")
root.resizable(False, False)

#define fonts and colors
my_font = ("Helvetica", 16)
black = "black"
light_green = "green"
light_red = "#ff4d4d"
blue = "blue"
orange = "orange"
pink = "#FF69B4"
white = "white"
red = "red"
purple = "#800080"
green = "#00FF00"
yellow = "#FFFF00"

root.config(bg=black)

#define socket consts
ENCODER = "utf-8"
BYTESIZE = 1024

class Connection:
    '''Create connection class for the server socket'''
    def __init__(self, client, address):
        self.client = client
        self.address = address
        self.username = None
        self.color = None

#define functions
def connect():
    '''Connect to server'''
    pass

def disconnect():
    '''Disconnect from server'''
    pass

def gui_start():
    '''Start GUI'''
    pass

def gui_end():
    '''End GUI'''
    pass

def create_message(flag, name, message, color):
    '''return message to client'''
    pass

def process_message(connection, message_json):
    '''Process message from client'''
    pass

def send_message(connection, message_json):
    '''Send message to client'''
    pass

def receive_message(connection):
    '''Receive message from client'''
    pass



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
connect_button = tkinter.Button(info_frame, text="Connect", font=my_font, bg=light_green, fg=black, borderwidth=5, command=connect)
disconnect_button = tkinter.Button(info_frame, text="Disconnect", font=my_font, bg=light_green, fg=black, borderwidth=5, command=disconnect)

name_entry.grid(row=0, column=1, padx=5, pady=5)
name_label.grid(row=0, column=0, padx=5, pady=5)
port_label.grid(row=0, column=2, padx=5, pady=5)
port_entry.grid(row=0, column=3, padx=5, pady=5)
ip_label.grid(row=1, column=0, padx=5, pady=5)
ip_entry.grid(row=1, column=1, padx=5, pady=1)
connect_button.grid(row=1, column=2, padx=5, pady=1)
disconnect_button.grid(row=1, column=3, padx=5, pady=1)

#Color Frame layout
color = StringVar()
color.set(white)
white_button = tkinter.Radiobutton(color_frame, text="White", font=my_font, bg=black, fg=light_green, variable=color, value=white, command=security_check)
red_button = tkinter.Radiobutton(color_frame, text="Red", font=my_font, bg=black, fg=light_green, variable=color, value=red, command=security_check)
orange_button = tkinter.Radiobutton(color_frame, text="Orange", font=my_font, bg=black, fg=light_green, variable=color, value=orange, command=security_check)
yellow_button = tkinter.Radiobutton(color_frame, text="yellow", font=my_font, bg=black, fg=light_green, variable=color, value=yellow, command=security_check)
green_button = tkinter.Radiobutton(color_frame, text="Green", font=my_font, bg=black, fg=light_green, variable=color, value=green, command=security_check)
blue_button = tkinter.Radiobutton(color_frame, text="Blue", font=my_font, bg=black, fg=light_green, variable=color, value=blue, command=security_check)
purple_button = tkinter.Radiobutton(color_frame, text="Purple", font=my_font, bg=black, fg=light_green, variable=color, value=purple, command=security_check)

color_buttons = [white_button, red_button, orange_button, yellow_button, green_button, blue_button, purple_button]

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
send_button = tkinter.Button(input_frame, text="Send", font=my_font, bg=light_green, fg=black, borderwidth=5, state=DISABLED, command=send_message)
input_entry.grid(row=0, column=0, padx=5)
send_button.grid(row=0, column=1, padx=5)

#run root window's main loop
root.mainloop()