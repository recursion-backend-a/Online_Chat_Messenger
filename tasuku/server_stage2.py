import os 
import socket
import time

def protocol_header(room_name_len, operation, state, payload_len):
    return room_name_len.to_bytes(1, "big") + int(operation).to_bytes(1, "big") + state.to_bytes(1, "big") + payload_len.to_bytes(29, "big")

pid = os.fork()

if pid > 0:
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
        try:
            print("connection from", client_address) 
            
            header = connection.recv(32)
            room_name_len = int.from_bytes(header[:1], "big")  #ちなみにroom_name_len = header[0]という書き方もできる
            operation = int.from_bytes(header[1:2], "big")
            state = int.from_bytes(header[2:3], "big")
            payload_len = int.from_bytes(header[3:32], "big")
            room_name = connection.recv(room_name_len).decode("utf-8")
            user_name = connection.recv(payload_len).decode("utf-8")
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

        except Exception as e:
            print("Error: " + str(e))

        finally:
            print("Closing current connection")
            connection.close()

else:
    group_hash = {}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ""
server_port = 9001
print("starting up on port {}".format(server_port))
sock.bind((server_address, server_port))


time_hash = {} #ユーザーの最後のメッセージの時間をハッシュマップで保持


while True:
    print("\n waiting to receive message")
    data, client_address = sock.recvfrom(4096)
    print("room_name_size", data[0])
    room_name_len = data[0]
    token_len = data[1]
    room_name = data[2 : 2 + room_name_len].decode("utf-8")
    token = data[2 + room_name_len: 2 + room_name_len + token_len].decode("utf-8")
    message = data[2 + room_name_len + token_len:].decode("utf-8")
    print("token", token, type(token))
    print("meesage", message)
    print("client address", client_address)

    if token not in group_hash[room_name]:
        print("This message is from an unknown user.")
        continue

    #以下の処理はルーム作成のときにすべき。グループのハッシュマップにユーザーを登録
    ##追記：すでにTCPに実装済みのため反映不要
    # if room_name not in group_hash.keys():
    #     group_hash[room_name] = []
    # group_hash[room_name].append(client_address)


    # now = time.time()
    # time_hash[token] = now
    # # しばらく通信していない相手をuser_address_setから削除
    # for user_token in time_hash.keys():
    #     if time_hash[user_token] - now  > 10000:
    #         group_hash[room_name].remove(user_token)


    # メッセージをグループ内全員に送信            
    if message:
        for user_token in group_hash[room_name]:
            sock.sendto(message.encode(), user_token)
            print("sending the message to {}".format(user_token))
