import socket
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = "localhost"
server_port = 9001
address = ""
port = 9050

sock.bind((address, port))
header = "" 
try:
    # sock.sendto(b"Message to send to the client.", (server_address, server_port))
    username = input("Type in your name\n")
    username_len = len(username).to_bytes(1, "big")
    message = input("Type in your message\n")

    all_message = username_len + username.encode() + message.encode()
    sock.sendto(all_message, (server_address, server_port))
    print("sending all_messages")
    #after making format, send the message
    data, server_address = sock.recvfrom(4096)
    print(data.decode())

finally:
    print("closing socket")
    sock.close()


