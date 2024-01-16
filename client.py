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
    print("sending {!r}".format(b"Message to send to the client."))
    sock.sendto(b"Message to send to the client.", (server_address, server_port))
    username = input("Type in your name")
    username_len = len(username).to_bytes(1, "big")
    message = input("Type in your message")
    #after making format, send the message
    sock.sendto(username_len, (server_address, server_port))
    sock.sendto(username.encode(), (server_address, server_port))
    sock.sendto(message.encode(), (server_address, server_port))


finally:
    print("closing socket")
    sock.close()


