


HEALTH_OPCODE = 0
MESSAGE_TO_ALL_OPCODE = 1
GIVE_ADMIN_OPCODE = 2
MUTE_USER_OPCODE = 4
UNMUTE_USER_OPCODE = 5
SERVER_ERROR_OPCODE = 7
REQUEST_ADMIN_OPCODE = 8


OPCODE = "opcode"
USER_NAME = "user_name"
CONTENT = "content"

# MAX_MSG_LENGTH = 1024


def send_to_sock(sock, data:  bytes):
    data = len(data).to_bytes(4, 'big')+data
    sock.send(data)
def sendall(sock, data:  bytes):
    data = len(data).to_bytes(4, 'big')+data
    sock.sendall(data)
    
def recv(sock):
    size = int.from_bytes( sock.recv(4), "big")
    return sock.recv(size)