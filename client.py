import socket
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = "127.0.0.1"
server_port = 9001
server_address_port = (server_address, server_port)
address = ""
port = 9050

sock.bind((address, port))

username = input("Type in your name\n")
username_len = len(username).to_bytes(1, "big")

try:
    while True:
        message = input("Type in your message\n")
        all_message = username_len + username.encode() + message.encode()
        sock.sendto(all_message, server_address_port)
        print("sending messages")
        #after making format, send the message
        data, server_address_port = sock.recvfrom(4096)
        print(data.decode())

        will_continue = input("Do you continue?\t Y or N\n")
        if will_continue == 'n' or will_continue == 'N':
            break

finally:
    print("closing socket")
    sock.close()



