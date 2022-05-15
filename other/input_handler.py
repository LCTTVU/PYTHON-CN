import socket
import threading

'''
        received_message = s.recv(2048).decode('utf-8')
        print(received_message)

        try:
            received_message = s.recv(2048).decode('utf-8')
            print(received_message)
        except ConnectionAbortedError:
            print("Threads closed.")
            exit(0)
'''
def send_func(msg, s):
    msg = msg + "\n"
    s.sendall(msg.encode('utf-8'))
    #print(msg)


def receive_func(s):
    data = s.recv(2048)
    received_msg = data.decode('utf-8')
    print(received_msg)
    return received_msg   


def process_input(user_input):
    user_input = user_input[1:]
    user_to_send = user_input.partition(" ")[0]
    msg = user_input.partition(" ")[2]
    msg = "SEND " + user_to_send + " " + msg
    return msg


def input_handler_func(s):
    while 1:
        user_input = input()
        if (user_input == "!quit"):
            print("Closing connection.")
            s.close()
            exit(0)
        
        if (user_input == "!who"):
            msg = "WHO"
            send_func(msg, s)
            
        if (user_input[0] == "@"):
            msg = process_input(user_input)
            send_func(msg, s)
        

def output_handler_func(s):
    while 1:
        data = s.recv(2048)
        received_msg = data.decode('utf-8')
        print(received_msg)    


def main():

    # Handshake
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostbyname("143.47.184.219")
    port = 5378

    s.connect((host,port))
    
    username = input("Enter username: ")
    
    msg = "HELLO-FROM %s" % (username)
    send_func(msg, s)
    
    received_msg = receive_func(s)
    
    if (received_msg == "IN-USE\n"):
        print("Username taken.")
        s.close()
        main()                                          # Handshake again if username taken
    if (received_msg == "BUSY\n"):
        print("Server is full.")
        s.close()
        
    input_handler = threading.Thread(target = input_handler_func(s))
    input_handler.start()
    
    output_handler = threading.Thread(target = output_handler_func(s))
    output_handler.start()
        

main()
