import socket, pickle

#create a list
unpickled_list = ['aubergine', 'beetroot', 'corn', 'dill', 'eggs']
print(unpickled_list)
print(type(unpickled_list))

pickle_list = pickle.dumps(unpickled_list)
print(pickle_list)
print(type(pickle_list))

#create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostbyname(socket.gethostname()), 12345))
s.listen()

while True:
    client, address = s.accept()
    print('Connection from', address)
    client.send(pickle_list)
    client.close()