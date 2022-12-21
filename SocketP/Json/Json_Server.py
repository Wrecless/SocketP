import socket, json

# create a list
message_packet = {
    'message': 'Hello, World!',
    'sender': 'John Smith',
    'recipient': 'Jane Doe',
    'timestamp': '2019-01-01 12:00:00',
    'color': 'red'
}

print(message_packet)
print(type(message_packet))

#turn the list into a json string
json_message_packet = json.dumps(message_packet)
print(json_message_packet)
print(type(json_message_packet))
json_message_packet = json_message_packet.encode('utf-8')
print(json_message_packet)
print(type(json_message_packet))

# create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostbyname(socket.gethostname()), 12345))
s.listen()

while True:
    client, address = s.accept()
    print('Connection from', address)
    client.send(json_message_packet)
    client.close()