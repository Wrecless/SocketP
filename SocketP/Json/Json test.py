import json

# create a list
message_packet = {
    'message': 'Hello, World!',
    'sender': 'John Smith',
    'recipient': 'Jane Doe',
    'timestamp': '2019-01-01 12:00:00',
    'color': 'red'
}

json_message_packet = json.dumps(message_packet['sender'])
print(json_message_packet)
print(type(json_message_packet))




