import os
import time
import socket

# user_address_set = set() #ユーザーの集合、グループ内に存在するユーザーを保持
# ステージ２では上のコードを
#　group = {}　キー：グループネーム　値：ユーザーのリスト、　のハッシュマップ
#  group[A] = [username1, username2, ....]とかにするべきか 

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


    if token not in group_hash.keys():
        print("This message is from an unknown user.")
        continue

    #以下の処理はルーム作成のときにすべき。グループのハッシュマップにユーザーを登録
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



