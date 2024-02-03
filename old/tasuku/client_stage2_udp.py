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

pid2 = os.fork()
if pid2 > 0:
    room_name = input("Type in the room name.\n")
    room_name_len = len(room_name).to_bytes(1, "big")
    token = socket.gethostbyname(socket.gethostname())
    token_len = len(token).to_bytes(1, "big")
    user_name = input("Type in your name\n")
    user_name_len = len(user_name).to_bytes(1, "big")
    while True:
        message = input("Type in your message\n")
        all_message = room_name_len + token_len + room_name.encode() + token.encode() + message.encode()
        sock.sendto(all_message, server_address_port)
        print("sending messages")
        time.sleep(1)
else:
    while True:
        data, server_address_port = sock.recvfrom(4096)
        if data:
            print("receiving : ", data.decode("utf-8"))
    