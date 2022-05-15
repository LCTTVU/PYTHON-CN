import socket
import threading


def input_handler(user_input):
    if (user_input == ""):
        return user_input
    if (user_input == "!quit"):
        s.close()
        exit(0)
    if (user_input == "!who"):
        message = "WHO"
        return message
    if (user_input[0] == "@"):
        user_input = user_input[1:]
        user_to_send = user_input.partition(" ")[0]
        message = user_input.partition(" ")[2]
        message = "SEND " + user_to_send + " " + message
        return message
    else: return user_input

def send_func():
    while 1:
        message = input_handler(input()) + "\n"
        s.sendall(message.encode('utf-8'))


def receive_func():
    while 1:
        try:
            received_message = s.recv(2048).decode('utf-8')
            print(received_message)
        except ConnectionAbortedError:
            print("Connection closed.")
            exit(0)


def handshake():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = socket.gethostbyname("143.47.184.219")
    PORT = 5378
    s.connect((HOST,PORT))
    username = input("Enter username: ")
    msg = "HELLO-FROM %s\n" % (username)
    s.sendall(msg.encode('utf-8'))
    received_msg = s.recv(2048).decode('utf-8')
    s.close()
    if (received_msg == "IN-USE\n"):
        print(received_msg)
        username = handshake()
    if (received_msg == "BUSY\n"):
        print(received_msg)
        exit(0)
    return username
                

if __name__ == "__main__":   

    # Handshake
    username = handshake()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = socket.gethostbyname("143.47.184.219")
    PORT = 5378
    s.connect((HOST,PORT))
    
    msg = "HELLO-FROM %s\n" % (username)
    s.sendall(msg.encode('utf-8'))
    
    client_send = threading.Thread(target = send_func)
    client_send.start()
    
    client_receive = threading.Thread(target = receive_func)
    client_receive.start()
    

#main()