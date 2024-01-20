import socket
import os
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = "127.0.0.1"
server_port = 9001
server_address_port = (server_address, server_port)
address = ""
port = 9050
sock.bind((address, port))

pid = os.fork()
if pid > 0:
    username = input("Type in your name\n")
    username_len = len(username).to_bytes(1, "big")
    while True:
        message = input("Type in your message\n")
        all_message = username_len + username.encode() + message.encode()
        sock.sendto(all_message, server_address_port)
        print("sending messages")
        time.sleep(1)
else:
    while True:
        data, server_address_port = sock.recvfrom(4096)
        if data:
            print("receiving : ", data.decode("utf-8"))
    