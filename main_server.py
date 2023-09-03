import json
import socket
import select
from protocol import *
SERVER_PORT = 7112
SERVER_IP = "0.0.0.0"
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADMIN_SECRET_PASSWORD = "Admin"

open_client_sockets = []
messages_to_send = []
admin_users = []
muted_users = []
def main():
    
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    client_sockets = []
    print("Listening for clients...")
    while True:
        rlist, wlist, xlist = select.select([server_socket] + client_sockets, client_sockets, [])
        for sock in rlist:
            if sock is server_socket:
                connection, client_address = sock.accept()
                print("New client joined!", client_address)
                client_sockets.append(connection)
            else:
                try:
                    data = sock.recv(MAX_MSG_LENGTH).decode()
                    if data == "":
                        print("Connection closed" )
                        client_sockets.remove(sock)
                        sock.close()
                    else:
                        try:
                            msg = json.loads(data)
                            opcode = msg[OPCODE]
                            if opcode == MESSAGE_TO_ALL_OPCODE:
                                if (msg[USER_NAME] not in muted_users):
                                    messages_to_send.append((sock, data))
                                else:
                                    sock.send((json.dumps({OPCODE: SERVER_ERROR_OPCODE,
                                        CONTENT: f'message "{msg[CONTENT]}" not sent because you are muted'})).encode())
                            elif opcode == HEALTH_OPCODE:
                                sock.send((json.dumps({OPCODE: HEALTH_OPCODE})).encode())
                            elif opcode == GIVE_ADMIN_OPCODE:
                                if msg[USER_NAME] in admin_users:
                                    admin_users.append(msg[CONTENT])
                                elif msg[CONTENT] in admin_users:
                                    sock.send((json.dumps({OPCODE: SERVER_ERROR_OPCODE,
                                        CONTENT: "user already an admin"})).encode())
                                else:
                                    sock.send((json.dumps({OPCODE: SERVER_ERROR_OPCODE,
                                        CONTENT: "you can not make someone an admin as you are not an admin yourself"})).encode())
                            elif opcode == REQUEST_ADMIN_OPCODE:
                                if msg[USER_NAME] in admin_users:
                                    sock.send((json.dumps({OPCODE: SERVER_ERROR_OPCODE,
                                        CONTENT: "you are already an admin"})).encode())
                                elif msg[CONTENT] == ADMIN_SECRET_PASSWORD:
                                    admin_users.append(msg[USER_NAME])
                                else:
                                    sock.send((json.dumps({OPCODE: SERVER_ERROR_OPCODE,
                                        CONTENT: "incorrect password"})).encode())
                            elif opcode == MUTE_USER_OPCODE:
                                if msg[USER_NAME] in admin_users:
                                    if msg[CONTENT] not in muted_users:
                                        muted_users.append(msg[CONTENT])
                                    else:
                                        sock.send((json.dumps({OPCODE: SERVER_ERROR_OPCODE,
                                        CONTENT: "user already muted"})).encode())
                                else:
                                    sock.send((json.dumps({OPCODE: SERVER_ERROR_OPCODE,
                                        CONTENT: "not an admin"})).encode())
                            elif opcode == UNMUTE_USER_OPCODE:
                                if msg[USER_NAME] in admin_users:
                                    if msg[CONTENT] in muted_users:
                                        muted_users.remove(msg[CONTENT])
                                    else:
                                        sock.send((json.dumps({OPCODE: SERVER_ERROR_OPCODE,
                                        CONTENT: "user was not muted"})).encode())
                                else:
                                    sock.send((json.dumps({OPCODE: SERVER_ERROR_OPCODE,
                                        CONTENT: "not an admin"})).encode())
                        except:
                            sock.send((json.dumps({OPCODE: SERVER_ERROR_OPCODE, CONTENT: "general server error"})).encode())
                except:
                    print("Connection closed" )
                    client_sockets.remove(sock)
                    sock.close()
                    
        for message in messages_to_send:
            current_socket, data = message
            for sock in wlist:
                if (sock != current_socket):
                    sock.send(data.encode())
                    try:
                        messages_to_send.remove(message)
                    except:
                        pass
            # if current_socket in wlist:
            #     current_socket.send(data.encode())
            #     messages_to_send.remove(message)
if __name__ == '__main__':
    main()
    