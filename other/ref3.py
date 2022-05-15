import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname("143.47.184.219")
port = 5378
s.connect((host, port))
print('Connected to chat server')
while 1:
    incoming_message = s.recv(1024)
    incoming_message = incoming_message.decode()
    print(' Server : ', incoming_message)
    print()
    message = input(str('>> '))
    message = message.encode()
    s.send(message)
    print('Sent')
    print()