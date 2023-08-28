import json
import socket
import threading
import sys
from time import sleep
from protocol import *

uncaught_msgs = []
host = '127.0.0.1'#input("Host: ")
port = 7112 #int(input("Port: "))
name = ""
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
is_ack = False

class send_thread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            message = input("")
            send_msg(message)
class recieve_thread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            try:
                print(recv_msg())
            except:
                pass
def recv_msg():
    global is_ack
    if (len(uncaught_msgs) == 0):
        data = json.loads(sock.recv(MAX_MSG_LENGTH).decode()) #sock.recv(1024).decode()
    else:
        data = uncaught_msgs[0]
        del uncaught_msgs[0]
    if (data[OPCODE] == HEALTH_OPCODE):
        is_ack = True
    return data

def send_msg(message: str):
    # l = len(message) % 100
    # if (l < 10):
    #     l = "0"+ str(l)
    # else:
    #     l = str(l)
    # msg = l + message
    sock.sendall((json.dumps({OPCODE: MESSAGE_TO_ALL_OPCODE ,USER_NAME: name, CONTENT: message})).encode())
def send(args: str, opcode: int):
    sock.sendall((json.dumps({OPCODE: opcode ,USER_NAME: name, CONTENT: args})).encode())
        
def health():
    global is_ack
    try:
        sock.send((json.dumps({OPCODE: HEALTH_OPCODE, USER_NAME: name})).encode())
        # data = json.loads((sock.recv(MAX_MSG_LENGTH)).decode())
        # opcode = data.get(OPCODE, -1)
        # if (opcode == HEALTH_OPCODE):
        #     return True
        # elif (opcode == -1):
        #     return False
        # else:
        #     uncaught_msgs.append(data)
        #     return True
        sleep(3)
        if is_ack:
            is_ack = False
            return True
        return False
    except:
        return False

def init_socket():
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
def main():
    global name
    name = input("UserName: ")

    #Attempt connection to server
    try:
       
        init_socket()
    except:
        print("Could not make a connection to the server")
        input("Press enter to quit")
        sys.exit(0)

    #Create new thread to wait for data
    # receiveThread = threading.Thread(target = receive, args = (sock, True))
    # receiveThread.start()
    
    #Send data to server
    #str.encode is used to turn the string message into bytes so it can be sent across the network


    send = send_thread()
    recv = recieve_thread()
    recv.start()
    send.start()


    while True:
        pass
        # threading.start_new_thread(send_msg, () )
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # loop.run_until_complete(send_msg)
        # loop2 = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop2)
        # loop2.run_until_complete(recv_and_print_msg)
        
if __name__ == '__main__':
    main()
    