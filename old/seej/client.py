import socket
import threading

def receive_message(client_socket):
    while True:
        try:
            message, _ = client_socket.recvfrom(4096)
            print(message.decode('utf-8'))
        except OSError:
            break

def main():
    # Serverと同じ
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 3002)

    # ユーザー名の入力。最大255バイトは仕様より。
    username = input("ユーザー名を入力してください: ")
    if len(username) > 255:
        raise ValueError("ユーザー名は255バイトを超えることはできません。")

    # メッセージの送信プロトコル
    encoded_username_length = bytes([len(username)]) # バイトに変換

    # バックグラウンドスレッドの作成
    threading.Thread(
        target=receive_message, 
        args=(client_socket,), 
        daemon=True
        ).start()

    try:
        while True: # 無限ループだが、try...except...finally 構文で抜けられる
            message = input("メッセージを入力してください: ")
            if message:
                # UTF-8エンコーディング
                full_message = encoded_username_length + username.encode('utf-8') + message.encode('utf-8')
                client_socket.sendto(full_message, server_address) # 単一のサーバーに送信

    except KeyboardInterrupt:
        print("クライアントを終了します...")
    finally:
        client_socket.close() # 最後にリソース解放

# スクリプトが直接実行された場合のみ発動
if __name__ == "__main__":
    main()
