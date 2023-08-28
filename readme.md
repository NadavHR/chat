opcodes:
    * 0 - check connection with server
    * 1 - message to all
    * 2 - add admin to user, admin only
    * 4 - mute user, admin only
    * 5 - unmute user, admin only
    * 7 - error message from server
    * 8 - ask for admin priviliges, requires sending the admin secret password

json structure:
    * opcode - the opcode, all packets must have it
    * user_name - user from which the packet was sent, only on packets sent by users
    * content - the content of the packet, only on packets that have content


how to run:
    * to run the server you need to run the file main_server.py
    * to run an instance of the client you need to run the file main_client.py