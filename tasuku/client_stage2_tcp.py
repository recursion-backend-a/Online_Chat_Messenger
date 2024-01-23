import socket
import sys

def protocol_header(room_name_len, operation, state, payload_len):
    return room_name_len.to_bytes(1, "big") + int(operation).to_bytes(1, "big") + state.to_bytes(1, "big") + payload_len.to_bytes(29, "big")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = input("Tyoe in the server's address to connect to : ")
server_port = 9002

try:
    sock.connect((server_address, server_port))
    print("conneted with", server_address)
except socket.error as err:
    print(err)
    sys.exit(1)

# try:
flag = 1
while flag:
    operation = input("1 : Create a room  2: Join a room\n")
    room_name = input("Type in the room name.\n")
    user_name = input("Type in your name\n")
    header = protocol_header(len(room_name.encode()), operation, 0, len(user_name.encode()))
    sock.send(header + user_name.encode("utf-8"))
    # サーバーからのレスポンスを受信
    header = sock.recv(32)
    room_name_len = header[0] #ちなみにheader[:1]という書き方をするとroom_name_len = int.from_bytes(header[:1], "big")と書かないと駄目
    state = header[2]
    payload_len = int.from_bytes(header[3:32], "big")
    sock.recv(room_name_len)
    server_response = sock.recv(payload_len).decode("utf-8")
    print(server_response)
    if state == 0: #stateが0のままのときはリクエストが失敗（とサーバー側で決める。）
        fleg = 0
    elif state == 1: #ｓstateが1であればリクエストが成功‥
        header = sock.recv(32)
        room_name_len = header[0]
        state = header[2]
        payload_len = int.from_bytes(header[3:32], "big")
        sock.recv(room_name_len)
        server_response = sock.recv(payload_len).decode("utf-8")
        print(server_response)
        flag = 0
        # サーバーから完了のメッセージを受信
        if state == 2:
            token = server_response.split('\n')[2] #tokenは３行目にあるので、配列の添字は2
            print(token)
# finally:
#     print("closing socket")
#     sock.close()

# 以降UDP通信が始まる
