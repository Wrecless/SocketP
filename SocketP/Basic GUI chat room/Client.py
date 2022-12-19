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

#define functions

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
connect_button = tkinter.Button(info_frame, text="Connect", font=my_font, bg=light_green, fg=black, borderwidth=5)
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
my_listbox = tkinter.Listbox(output_frame, width=50, height=20, font=my_font, yscrollcommand=my_scrollbar.set)


#run root window's main loop
root.mainloop()