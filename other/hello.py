import socket
import threading
import sys

def test_func(msg):
    msg = msg + "\n"
    s.sendall(msg.encode('utf-8'))
    receive_func()

def test_func2(msg):
    msg = msg + "\n"
    s.sendall(msg.encode('utf-8'))
    receive_func()
    receive_func()
    
def receive_func():
    data = s.recv(2048)
    received_msg = data.decode('utf-8')
    print(received_msg)

s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostbyname("143.47.184.219")
port = 5378

s.connect((host, port))
print("Connected to server.")

username = input("Enter username: ")
msg = "HELLO-FROM %s" % (username)
test_func(msg)
s.close()

s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostbyname("143.47.184.219")
port = 5378

s.connect((host, port))
username = input("Enter username: ")
msg = "HELLO-FROM %s" % (username)
test_func(msg)

msg = "!who"

'''
if (msg == "!who"):
    msg = "WHO"
    test_func(msg)


msg = "SEND echobot test 123 bsb sjdiajia"

test_func2(msg)
    
msg = input()

if (msg == "!quit"):
    print("Closing connection.")
    s.close()
    exit(0)
'''