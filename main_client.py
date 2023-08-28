import threading
from time import sleep
from tkinter import *
import client 
import socket
from protocol import *

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Impact 14"
FONT_BOLD = "Impact 17 bold"
main_window = Tk()
second_window = Toplevel()
txt = Text(main_window, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
msg_field = Entry(main_window, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
user_name_field = Entry(second_window, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=15)
args_field = Entry(second_window, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=15)

options = ["add admin (admin only)",
           "mute user (admin only)",
           "unmute user (admin only)",
           "request admin"]
options_to_opcode = {"add admin (admin only)": GIVE_ADMIN_OPCODE,
           "mute user (admin only)": MUTE_USER_OPCODE,
           "unmute user (admin only)": UNMUTE_USER_OPCODE,
           "request admin": REQUEST_ADMIN_OPCODE}
chosen = StringVar()
dropdown = OptionMenu(second_window, chosen, *options)

def main():
    # GUI
    recv = recieve_thread()
    conn = connection()
    conn.start()
    main_window.title("Chat")
    second_window.title("Settings")
    second_window.configure(bg=BG_COLOR)
    lable1 = Label(main_window, bg=BG_COLOR, fg=TEXT_COLOR, text="Chat here", font=FONT_BOLD, pady=10, width=20, height=1).grid(
        row=0)
    label2 = Label(second_window, bg=BG_COLOR, fg=TEXT_COLOR, text="enter username: ", font=FONT_BOLD, height=1).grid(
        row=0, column=0)
    user_name_field.grid(row=0, column=1)
    change_username_button = Button(second_window, text="change username", font=FONT_BOLD, bg=BG_GRAY,
                command=change_username).grid(row=0, column=2)
    label3  = Label(second_window, bg=BG_COLOR, fg=TEXT_COLOR, text="command: ", font=FONT_BOLD, height=1).grid(
        row=2, column=0)
    dropdown.grid(row=2, column=1)
    label4 = Label(second_window, bg=BG_COLOR, fg=TEXT_COLOR, text="command args: ", font=FONT_BOLD, height=1).grid(
        row=3, column=0)
    args_field.grid(row=3, column=1)
    send_command_button = Button(second_window, text="send command", font=FONT_BOLD, bg=BG_GRAY,
                command=send_command).grid(row=4)
    
    
    txt.grid(row=1, column=0, columnspan=2)
    scrollbar = Scrollbar(txt)
    scrollbar.place(relheight=1, relx=0.974)
    
    
    msg_field.grid(row=2, column=0)
    
    send_button = Button(main_window, text="Send", font=FONT_BOLD, bg=BG_GRAY,
                command=send).grid(row=2, column=1)
    txt.tag_config("this_user", foreground="#67ff4f")
    txt.tag_config("error", foreground="#ff0000")
    main_window.bind("<Return>", send)
    recv.start()
    
    txt.configure(state="disabled")
    main_window.mainloop()



# Send function
def send(self=None):
    if not len(client.name) > 0:
        txt.configure(state="normal")
        msg = "cant send message without username"
        txt.insert(END, msg+"\n")
        lines = count_lines(txt.get("1.0", END)) - 1
        txt.tag_add("error", f"{lines}.0", f"{lines}.{len(msg)}")
    elif len(msg_field.get()) > 0:
        send = "You: " + msg_field.get()
        txt.configure(state="normal")
        txt.insert(END, send+"\n")
        lines = count_lines(txt.get("1.0", END)) - 1
        try:
            client.send_msg(msg_field.get())
            txt.tag_add("this_user", f"{lines}.0", f"{lines}.{len(send)}")
        except:
            txt.tag_add("error", f"{lines}.0", f"{lines}.{len(send)}")
        msg_field.delete(0, END)
    txt.configure(state="disabled")



def change_username():
    client.name = user_name_field.get()


def send_command():
    if not len(client.name) > 0:
        txt.configure(state="normal")
        msg = "cant send comand without username"
        txt.insert(END, msg+"\n")
        lines = count_lines(txt.get("1.0", END)) - 1
        txt.tag_add("error", f"{lines}.0", f"{lines}.{len(msg)}")
    elif not len(chosen.get()) > 0:
        txt.configure(state="normal")
        msg = "cant send empty command"
        txt.insert(END, msg+"\n")
        lines = count_lines(txt.get("1.0", END)) - 1
        txt.tag_add("error", f"{lines}.0", f"{lines}.{len(msg)}")
    else:
        client.send(args_field.get(), options_to_opcode[chosen.get()])

def count_lines(s: str):
    return len(s.split("\n")) - 1
class recieve_thread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            try:
                msg = client.recv_msg()
                if (msg[OPCODE] == MESSAGE_TO_ALL_OPCODE): 
                    txt.configure(state="normal")
                    txt.insert(END, msg[USER_NAME] + ": " + msg[CONTENT]+"\n")
                    txt.configure(state="disabled")
                elif (msg[OPCODE] == SERVER_ERROR_OPCODE):
                    txt.configure(state="normal")
                    lines = count_lines(txt.get("1.0", END)) 
                    content =  msg[CONTENT]
                    txt.insert(END, content+"\n")
                    txt.tag_add("error", f"{lines}.0", f"{lines}.{len(content)}")
                    txt.configure(state="disabled")
                    
            except:
                pass
class connection (threading.Thread):
    def __init__(self):
        try:
            client.init_socket()
        except:
            pass
        threading.Thread.__init__(self)
    def run(self):
        while True:
            try:
                if not client.health():
                    try:
                        client.sock.close()
                        client.init_socket()
                        # sleep(3)
                    except:
                        client.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client.init_socket()
                        # client.sock.close()
                else:
                    sleep(3)
            except:
                pass
            
            
            
            
if __name__ == '__main__':
    main()
    