import os
import socket

user_set = set()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ""
server_port = 9001
print("starting up on port {}".format(server_port))
sock.bind((server_address, server_port))

while True:
    print("\n waiting to receive message")
    message_all = ""
    username_len, client_address = sock.recvform(1)
    username_b = sock.recv(username_len)
    username = username_b.decode("utf-8")
    user_set.add(client_address)
    while True:
        message = socket.recv(4096)
        message_all += message
        if not message:
            message_all = message_all.decode("utf-8")
            break
    print(message_all)
    if message:
        for user in user_set:
            sock.sendto(message_all.encode(), client_address)

