import os
import socket

user_address_set = set()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ""
server_port = 9001
print("starting up on port {}".format(server_port))
sock.bind((server_address, server_port))

while True:
    print("\n waiting to receive message")
    data, client_address = sock.recvfrom(4096)
    user_address_set.add(client_address)
    print(data[0])
    username_len = data[0]
    username = data[1:username_len + 1].decode("utf-8")
    message = data[username_len + 1:].decode("utf-8")
    print("username", username)
    print("message:", message)

    if message:
        for user_address in user_address_set:
            sock.sendto(message.encode(), user_address)
            print("sending the message to {}".format(user_address))

