import socket
import threading

def client_handler(conn,addr):
    print(f"Connected by {addr}")
    client_connected = True
    while client_connected:
        try:
            received_msg = conn.recv(2048).decode('utf-8')
            while not received_msg.endswith("\n"):
                received_msg = received_msg + conn.recv(2048).decode('utf-8')
            if (received_msg.startswith("HELLO-FROM")):
                client_name = received_msg.partition(" ")[2]
                client_name = client_name[:-1]
                if client_name in user_list.keys():
                    conn.sendall("IN-USE\n".encode('utf-8'))
                    print(f"Username {client_name} in use.")
                    client_connected = False
                user_list[client_name] = conn
                conn.sendall(f"HELLO {client_name}\n".encode('utf-8'))
                #print(f"{client_name}")
            if (received_msg == "!quit\n"):
                client_connected = False
                del user_list[client_name]
                print(f"{addr} disconnected")
            if (received_msg == "WHO\n"):
                print("a")
                response = "WHO-OK"
                for user, conn in user_list.items():
                    response += f" {user}"
                conn.sendall(f"{response}\n".encode('utf-8'))
            if (received_msg.startswith("SEND")):
                sender = client_name
                received_msg = received_msg[5:]
                recipient = received_msg.partition(" ")[0]
                msg = received_msg.partition(" ")[2]
                if recipient not in user_list.keys():
                    conn.sendall(f"UNKNOWN\n".encode('utf-8'))
                else:
                    recipient_conn = user_list[recipient]
                    recipient_conn.sendall(f"DELIVERY {sender} {msg}\n".encode('utf-8'))
                    conn.sendall(f"SEND-OK\n".encode('utf-8'))
        except ConnectionError as e:
            print(e)
            if conn in user_list:
                del user_list[conn]
            conn.close()
        except Exception as e:
            print(e)
    conn.close()

HOST = socket.gethostbyname("localhost")
PORT = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

user_list = {}
conn_list = {}

s.listen()
print(f"Server running on HOST: {HOST}, PORT: {PORT}")
while True:
    conn,addr = s.accept()
    thread = threading.Thread(target=client_handler,args=(conn,addr))
    thread.start()
    print(f"Connections: {threading.active_count() - 1}")




