import socket
import sys

def protocol_header(room_name, operation, state, payload):
    return len(room_name).to_bytes(1, "big") + operation.to_bytes(1, "big") + state.to_bytes(1, "big") + len(payload).to_bytes("utf-8")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = input("Tyoe in the server's address to connect to : ")
server_port = 9002

try:
    sock.connect((server_address, server_port))
except socket.error as err:
    print(err)
    sys.exit(1)

try:
    flag = 0
    while flag:
        operation = input("1 : Create a room  2: Join a room")
        room_name = input("Tyoe in athe room name.")
        user_name = input("Type in your name")
        header = protocol_header(room_name, operation, 0, user_name)
        sock.send(header)
        sock.send(user_name)
        # サーバーからのレスポンスを受信
        header = sock.recv(32)
        room_name_len = int.from_bytes(header[0], "big")
        payload_len = int.from_bytes(header[3:32], "big")
        sock.recv(room_name_len)
        server_response = sock.recv(payload_len).decode("utf-8")
        print(server_response)
        if server_response == "This room does not exist.":
            fleg = 0
        # サーバーから完了のメッセージを受信
        elif server_address == "The state is 1. Joining" + room_name:
            header = sock.recv(32)
            room_name_len = int.from_bytes(header[0], "big")
            payload_len = int.from_bytes(header[3:32], "big")
            sock.recv(room_name_len)
            server_response = sock.recv(payload_len).decode("utf-8")
            print(server_response)
            flag = 1

finally:
    print("closing socket")
    sock.close()

# 以降UDP通信が始まる
