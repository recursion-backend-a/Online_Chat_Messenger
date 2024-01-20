import socket
import os

def protocol_header(room_name, operation, state, payload):
    return len(room_name).to_bytes(1, "big") + operation.to_bytes(1, "big") + state.to_bytes(1, "big") + len(payload).to_bytes("utf-8")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ''
server_port = 9002

sock.bind((server_address, server_port))
sock.listen(5)

group_hash = {}
while True:
    connection, client_address = sock.accept()
    try:
        print("connection from", client_address)
        header = connection.recv(32)
        room_name_len = int.from_bytes(header[0], "big")
        operation = int.from_bytes(header[1], "big")
        state = int.from_bytes(header[2], "big")
        payload_len = int.from_bytes(header[3:32], "big")

        room_name = connection.recv(room_name_len).decode("utf-8")
        user_name = connection.recv(payload_len).decode("utf-8")

        if operation == 1: #操作コードが１のとき
            if room_name not in group_hash.keys():
                group_hash[room_name] = []
            group_hash[room_name].append((client_address, user_name, "host"))
            # クライアントに応答
            server_message = "The state is 1. Making a new room."
            header = protocol_header( room_name, operation, 1, server_message)
            sock.send(header)
            sock.send(server_message)
            # クライアントにルーム作成の完了を伝える
            server_message = "The state is 2. Finished making a new room."
            header = protocol_header( room_name, operation, 2, server_message)
            sock.send(header)
            sock.send(server_message)

        elif operation == 2: #操作コードが２のとき
            group_hash[room_name].append((client_address, user_name, ""))
            # クライアントに応答
            server_message = "The state is 1. Joining" + room_name
            header = protocol_header( room_name, operation, 1, server_message)
            sock.send(header)
            sock.send(server_message)
            # クライアントにルーム作成の完了を伝える
            server_message = "The state is 2. Joined" + room_name
            header = protocol_header( room_name, operation, 2, server_message)
            sock.send(header)
            sock.send(server_message)




        
        print("sending a token to ", client_address)
        sock.send(client_address)

    except Exception as e:
        print("Error: " + str(e))

    finally:
        print("Closing urrent connection")
        connection.close()

