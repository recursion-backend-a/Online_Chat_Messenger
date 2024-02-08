# ソケットとモジュールをインポート
import socket
import sys
import os
import time

def protocol_header(room_name_len, operation, state, payload_len):
    return room_name_len.to_bytes(1, "big") + int(operation).to_bytes(1, "big") + state.to_bytes(1, "big") + payload_len.to_bytes(29, "big")
#ソケットを作成
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#入力されたアドレスのサーバーに接続。ポートは指定しておく
server_address = input("Type in the server's address to connect to : ")
server_port = 9002

try:
    tsp_sock.connect((server_address, server_port))
    print("conneted with", server_address)
except socket.error as err:
    print(err)
    sys.exit(1)

try:
    flag = 1
    while flag:
        operation = input("1 : Create a room  2: Join a room\n")
        room_name = input("Type in the room name.\n")
        user_name = input("Type in your name\n")
        header = protocol_header(len(room_name.encode()), operation, 0, len(user_name.encode()))
        tcp_sock.send(header)
        tcp_sock.send(room_name.encode("utf-8"))
        tcp_sock.send(user_name.encode("utf-8"))
        # サーバーからのレスポンスを受信
        header = tcp_sock.recv(32)
        room_name_len = header[0] #ちなみにheader[:1]という書き方をするとroom_name_len = int.from_bytes(header[:1], "big")と書かないと駄目
        state = header[2]
        payload_len = int.from_bytes(header[3:32], "big")
        server_response = tcp_sock.recv(payload_len).decode("utf-8")
        print(server_response)
        if state == 0: #stateが0のままのときはリクエストが失敗（とサーバー側で決める。）
            flag = 1
        elif state == 1: #stateが1であればリクエストが成功‥
            header = tcp_sock.recv(32)
            #room_name_len = header[0]
            state = header[2]
            payload_len = int.from_bytes(header[3:32], "big")
            server_response = tcp_sock.recv(payload_len).decode("utf-8")
            print(server_response)
            flag = 0
            # サーバーから完了のメッセージを受信
            if state == 2:
                token = server_response.split('\n')[2] #tokenは３行目にあるので、配列の添字は2
                print(token)
finally:
    print("closing tcp_socket")
    tcp_sock.close()

# 以降UDP通信が始まる

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address = "127.0.0.1"
server_port = 9001
server_address_port = (server_address, server_port)

pid2 = os.fork()
if pid2 > 0:
    room_name = input("Type in the room name.\n")
    room_name_len = len(room_name).to_bytes(1, "big")
    token = socket.gethostname()
    #token = socket.gethostbyname(socket.gethostname())
    print(token)
    token_len = len(token).to_bytes(1, "big")
    user_name = input("Type in your name\n")
    user_name_len = len(user_name).to_bytes(1, "big")
    while True:
        message = input("Type in your message\n")
        all_message = room_name_len + token_len + room_name.encode() + token.encode() + message.encode()
        udp_sock.sendto(all_message, server_address_port) ##ここが通っているか怪しい
        print("sending messages")
        time.sleep(1)
else:
    while True:
        data, server_address_port = udp_sock.recvfrom(4096)
        if data:
            print("receiving : ", data.decode("utf-8"))
