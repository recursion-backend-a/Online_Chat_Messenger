import socket
import time

M_SIZE = 4096

host = '127.0.0.1'
port = 8890

locaddr = (host, port)

# クライアント情報を格納するデータ構造（辞書）
clients = {}

def process_message(sender_info, message):
    # メッセージをリレー
    for client_username, client_info in clients.items():
        if client_username != sender_info['username']:
            send_message_to_client(message, client_info)

def send_message_to_client(message, client_info):
    # UDP通信でメッセージを送信
    # (client_info['ip'], client_info['port']) に送信先のアドレス情報が含まれていると仮定
    # 具体的な実装は、socketなどの通信ライブラリを使用する必要があります
    send_udp_message(message, (client_info['ip'], client_info['port']))

def remove_inactive_clients():
    # 不活性なクライアントを削除
    current_time = time.time()
    inactive_timeout = 300  # 5分未満メッセージがないクライアントを削除

    for username, client_info in list(clients.items()):
        if current_time - client_info['last_message_time'] > inactive_timeout:
            del clients[username]

def send_udp_message(message, address):
    # UDPメッセージを送信する具体的な実装
    # ここではsocket.sendto()を使用すると仮定
    sock.sendto(message.encode('utf-8'), address)

sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
sock.bind(locaddr)

while True:
    try:
        # Clientからのmessageの受付開始
        print('Waiting message')
        message, cli_addr = sock.recvfrom(M_SIZE)
        message = message.decode(encoding='utf-8')
        
        # 送信者のユーザー名を取得
        sender_username_len = ord(message[0])
        sender_username = message[1:sender_username_len + 1]

        # クライアント情報を更新または新規追加
        clients[sender_username] = {
            'ip': cli_addr[0],
            'port': cli_addr[1],
            'last_message_time': time.time(),
            'username': sender_username
        }

        # メッセージのリレー
        process_message(clients[sender_username], message[sender_username_len + 1:])

        # クライアントが受信待ちになるまで待つ
        time.sleep(1)

        # Clientへ受信完了messageを送信
        print('Send response to Client')
        sock.sendto('Success to receive message'.encode(encoding='utf-8'), cli_addr)

        # 不活性なクライアントを削除
        remove_inactive_clients()

    except KeyboardInterrupt:
        print('\n . . .\n')
        sock.close()
        break

