import socket, json

# create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostbyname(socket.gethostname()), 12345))

# receive the json string
json_message_packet = s.recv(1024)
json_message_packet = json_message_packet.decode('utf-8')
json_message_packet = json.loads(json_message_packet)

print(json_message_packet)
print(type(json_message_packet))
