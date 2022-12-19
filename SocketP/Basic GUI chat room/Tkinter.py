#Tkinter test
#iconarchive.com
import tkinter
from tkinter import BOTH
from tkinter import StringVar
from tkinter import END

#define window
root = tkinter.Tk()
root.title("Chat Room")
root.iconbitmap("chat.ico")
root.geometry("400x400")
root.resizable(False, False) #disable resizing

#define colors
root_color = "#2c3e50"
input_color = "#34495e"
output_color = "#7f8c8d"
root.config(bg=root_color)

#define functions
def send_message():
    '''sends message to output box'''
    message = tkinter.Label(output_frame, text=message_entry.get(), bg=output_color, fg=text_color.get(), font=("Arial", 12))
    message.pack()
    #clear entry for next message
    message_entry.delete(0, END)


#define GUI
#difine frames
input_frame = tkinter.Frame(root, bg=input_color)
output_frame = tkinter.Frame(root, bg=output_color)
input_frame.pack(pady=10)
output_frame.pack(padx=10, pady=(0, 10), fill=BOTH, expand=True)

#define widgets
message_entry = tkinter.Entry(input_frame, text='Enter message', width=35, font=("Arial", 12))
send_button = tkinter.Button(input_frame, text="Send",bg=output_color, command=send_message)
message_entry.grid(row=0, column=0,columnspan=3, padx=10, pady=10)
send_button.grid(row=0, column=3, rowspan=2, padx=5, pady=5, ipadx=5, ipady=10)

#text_color
text_color = StringVar()
text_color.set("black")
red_button = tkinter.Radiobutton(input_frame, text="Red", variable=text_color, value="red", bg=input_color)
green_button = tkinter.Radiobutton(input_frame, text="Green", variable=text_color, value="green", bg=input_color)
blue_button = tkinter.Radiobutton(input_frame, text="Blue", variable=text_color, value="blue", bg=input_color)
red_button.grid(row=1, column=0, padx=5, pady=5)
green_button.grid(row=1, column=1, padx=5, pady=5)
blue_button.grid(row=1, column=2, padx=5, pady=5)

output_label = tkinter.Label(output_frame, text="--- Stored Messages ---", fg=input_color, bg=output_color, font=("Arial", 12))
output_label.pack(pady=10)


#run window
root.mainloop()

