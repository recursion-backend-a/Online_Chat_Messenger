import os
import time
import socket

user_address_set = set() #ユーザーの集合、グループ内に存在するユーザーを保持
# ステージ２では上のコードを
#　group = {}　キー：グループネーム　値：ユーザーのリスト、　のハッシュマップ
#  group[A] = [username1, username2, ....]とかにするべきか 

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ""
server_port = 9001
print("starting up on port {}".format(server_port))
sock.bind((server_address, server_port))


time_hash = {} #ユーザーの最後のメッセージの時間をハッシュマップで保持
name_hash = {} #ユーザーの名前とアドレスの対応をハッシュマップで保持 

while True:
    print("\n waiting to receive message")
    data, client_address = sock.recvfrom(4096)
    user_address_set.add(client_address)
    print(data[0])
    username_len = data[0]
    username = data[1 : username_len + 1].decode("utf-8")
    message = data[username_len + 1:].decode("utf-8")
    print("username", username)
    print("message:", message)

    name_hash[username] = client_address

    now = time.time()
    time_hash[username] = now
    # しばらく通信していない相手をuser_address_setから削除
    for user_name in time_hash:
        if time_hash[user_name] - now  > 10000:
            user_address_set.remove(name_hash[user_name])
    
    # メッセージをグループない全員に送信
    if message:
        for user_address in user_address_set:
            sock.sendto(message.encode(), user_address)
            print("sending the message to {}".format(user_address))



