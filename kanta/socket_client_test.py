import socket
import time

M_SIZE = 4096

# Serverのアドレスを用意。Serverのアドレスは確認しておく必要がある。
serv_address = ('127.0.0.1', 8890)

# クライアントのユーザー名を取得
print('Enter your username:')
username = input()

# ①ソケットを作成する
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    try:
        # ②messageを送信する
        print('Input any messages, Type [end] to exit')
        message = input()
        if message != 'end':
            # ユーザー名の長さを1バイトで送信
            send_len = sock.sendto(bytes([len(username)]) + username.encode('utf-8') + message.encode('utf-8'), serv_address)
            
            # ③Serverからのmessageを受付開始
            print('Waiting response from Server')
            rx_message, addr = sock.recvfrom(M_SIZE)
            print(f"[Server]: {rx_message.decode(encoding='utf-8')}")

        else:
            print('closing socket')
            sock.close()
            print('done')
            break

    except KeyboardInterrupt:
        print('closing socket')
        sock.close()
        print('done')
        break
