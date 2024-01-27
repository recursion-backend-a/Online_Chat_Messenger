# socketとosモジュールをインポート
import socket
import os

def protocol_header(room_name_len, operation, state, payload_len):
    return room_name_len.to_bytes(1, "big") + int(operation).to_bytes(1, "big") + state.to_bytes(1, "big") + payload_len.to_bytes(29, "big")

#ソケットを作成し、アドレスとポートを作成
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ''
server_port = 9002

sock.bind((server_address, server_port))
sock.listen(1)

group_hash = {}
while True:
    print("waiting for connections.")
    connection, client_address = sock.accept()
    # try:
    print("connection from", client_address)  #ここまでは通っている
    
    header = connection.recv(32)
    print(header) #テスト用に追加、ここまで通っている
    room_name_len = int.from_bytes(header[:1], "big")  #ちなみにroom_name_len = header[0]という書き方もできる
    print(room_name_len)
    operation = int.from_bytes(header[1:2], "big")
    print(operation)
    state = int.from_bytes(header[2:3], "big")
    print(state)
    payload_len = int.from_bytes(header[3:32], "big")
    print(payload_len)
    room_name = connection.recv(room_name_len).decode("utf-8")
    print(room_name)
    user_name = connection.recv(payload_len).decode("utf-8")
    print(user_name)
    print(room_name_len, operation, state, payload_len, room_name, user_name)

    if operation == 1: #操作コードが１のとき(ルーム作成のとき)
        if room_name not in group_hash.keys():
            group_hash[room_name] = []
        group_hash[room_name].append((client_address[0], user_name, "host"))
        # クライアントに応答
        server_message = "The state is 1. Making a new room."
        header = protocol_header( len(room_name.encode()), operation, 1, len(server_message.encode()))
        connection.send(header)
        connection.send(server_message.encode("utf-8"))
        #上のコード、ズレてる。The stateのはずがstateとなってる
        # クライアントにルーム作成の完了を伝える
        server_message = "The state is 2. Finished making a new room." + '\n' + "Your token is\n" + str(client_address[0])
        header = protocol_header(len(room_name.encode()), operation, 2, len(server_message.encode()))
        print(header) #テスト
        connection.send(header)
        connection.send(server_message.encode("utf-8"))

    elif operation == 2: #操作コードが２のとき(ルームに参加のとき)
        if room_name not in group_hash.keys():
            server_message = "This room does not exist."
            print(server_message)
            header = protocol_header(len(room_name.encode()), operation, 0, len(server_message.encode()))
            connection.send(header)
            connection.send(server_message.encode("utf-8"))
        else:
            group_hash[room_name].append((client_address[0], user_name, ""))
            # クライアントに応答
            server_message = "The state is 1. Joining" + room_name
            header = protocol_header(len(room_name.encode()), operation, 1, len(server_message.encode()))
            connection.send(header)
            connection.send(server_message.encode("utf-8"))
            # クライアントにルーム参加の完了を伝える
            server_message = "The state is 2. Joined" + room_name + '\n' + "Your token is\n" + str(client_address[0])
            header = protocol_header(len(room_name.encode()), operation, 2, len(server_message.encode()))
            connection.send(header)
            connection.send(server_message.encode("utf-8"))

    # except Exception as e:
    #     print("Error: " + str(e))

    # finally:
    #     print("Closing current connection")
    #     connection.close()

