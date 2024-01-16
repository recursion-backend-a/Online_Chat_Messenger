import socket
import time
import threading # マルチスレッドプログラミングに使う

CLIENT_TIMEOUT = 30

# 非アクティブクライアントの管理
def check_client_timeout(clients, client_last_active):
    while True: # 無限ループ（サーバーの動作中は常にクライアントを監視）
        current_time = time.time() # 現在に時刻（Unixエポック秒）を取得
        inactive_clients = []
        for client, last_active in client_last_active.items():
            if current_time - last_active > CLIENT_TIMEOUT:
                inactive_clients.append(client) # 差分で非アクティブ認定

        for client in inactive_clients:
            print(f"タイムアウト：{client}")
            clients.remove(client) # クライアントリストから削除
            del client_last_active[client] # 最終アクティブ辞書から削除

        time.sleep(5) # 5秒おきに上のチェックをする。リクエストを減らしてリソースの過剰な消費を防ぐ

def main():
    # UDPネットワークソケットを使ったメッセージのやり取り = メインスレッドが担当
    # memo: AF_INET はIPv4アドレスを使うインターネット（線路）
    # memo: SOCK_DGRAM は「データグラム」ソケット。UDPに対応（駅）
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # ソケットをネットワークアドレス（IPアドレスとポート番号）にバインドする
    # →特定のポートでクライアントからの接続要求を待ち受けるようになる
    server_socket.bind(('localhost', 3002))

    clients = [] # 各クライアントのネットワークアドレス
    client_last_active = {} # key: ネットワークアドレス, value: 最終更新時刻

    # 新しいスレッド（バックグラウンドスレッド）の作成
    # check_client_timeout関数を実行することが目的
    # memo: daemon は、メインスレッドの終了時に自動的に終了すること
    threading.Thread(
        target = check_client_timeout, 
        args = (clients, client_last_active), 
        daemon = True
        ).start()
    print("サーバーが起動し、メッセージを待機中です...")

    try:
        while True: # 無限ループだが、try...except...finally 構文で抜けられる
            # メッセージサイズの処理
            # memo: recvfrom はUDPで使われ、ソケットを通じてデータをバイト列として受信。
            # 受信データと送信元のアドレスを返す。引数は最大バイト数。4096バイトは仕様より。
            message, address = server_socket.recvfrom(4096)
            if address not in clients:
                clients.append(address) # 新しいアドレスならクライアントとしてクライアントリストに登録
            client_last_active[address] = time.time() # 最後のアクティブタイムを辞書に登録

            # メッセージの送信プロトコル（受信したバイト列の解釈を決定）
            # メッセージは「①ユーザー名の長さ、②ユーザー名、③チャットメッセージ」で構成する。
            username_length = message[0] # バイト配列の最初にユーザー名の長さを入れる
            # UTF-8デコーディング
            username = message[1:1+username_length].decode('utf-8') # データ配列の2番目からユーザー名の長さ分を確保
            chat_message = message[1+username_length:].decode('utf-8') # それ以降は全てチャットメッセージとする
            print(f"Received message from {username}: {chat_message}")

            # サーバのリレーシステム
            # messageは全てのクライアントに送信される
            for client in clients:
                server_socket.sendto(message, client)
                
    except KeyboardInterrupt:
        print("サーバーを終了します...")
    finally:
        server_socket.close() # 最後にリソース解放

# スクリプトが直接実行された場合のみ発動
if __name__ == "__main__":
    main()
