import socket, pickle

# create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostbyname(socket.gethostname()), 12345))

# receive the pickled list
pickled_list = s.recv(1024)
print(pickled_list)
print(type(pickled_list))

unpickled_list = pickle.loads(pickled_list)
print(unpickled_list)
print(type(unpickled_list))
print(unpickled_list[0])
unpickled_list.append('fennel')
for item in unpickled_list:
    print(item)

    #************NOT SAFE**************#