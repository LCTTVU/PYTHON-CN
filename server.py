import socket
import threading

HOST = socket.gethostbyname("localhost")
PORT = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

user_list = {}

user_limit = 128


def client_handler(conn,addr):
    print(f"Connected by {addr}")
    client_connected = True
    while client_connected:
        try:
            #print(f"user_list: {user_list}")
            received_msg = conn.recv(2048).decode('utf-8')
            while not received_msg.endswith("\n"):
                received_msg += conn.recv(2048).decode('utf-8')
            print(f"{addr}: {received_msg[:-1]}")
            
            if (received_msg.startswith("HELLO-FROM")):
                client_name = received_msg.partition(" ")[2]
                client_name = client_name[:-1]
                if (len(user_list.keys()) == user_limit):
                    response = "BUSY"
                    conn.sendall(f"{response}\n".encode('utf-8'))
                    print(f"(Server): {response}")
                    client_connected = False
                elif (client_name in user_list.keys()):
                    response = "IN-USE"
                    conn.sendall(f"{response}\n".encode('utf-8'))
                    print(f"(Server): {response}")
                    client_connected = False
                else:
                    user_list[client_name] = conn
                    response = f"HELLO {client_name}"
                    conn.sendall(f"{response}\n".encode('utf-8'))
                    print(f"(Server): {response}")
                    #print(f"{client_name}")
            
            elif (received_msg == "!quit\n"):
                client_connected = False
                del user_list[client_name]
                print(f"{addr} disconnected")
            
            elif (received_msg == "WHO\n"):
                response = "WHO-OK"
                #print(f"user_list: {user_list}")
                #print(f"This is the conn before: {conn}")
                for key, value in user_list.items():
                    response += f" {key}"
                conn.sendall(f"{response}\n".encode('utf-8'))
                print(f"(Server): {response}")
                #print(f"This is the conn after: {conn}")
            
            elif (received_msg.startswith("SEND")):
                sender = client_name
                received_msg = received_msg[5:-1]
                recipient = received_msg.partition(" ")[0]
                msg = received_msg.partition(" ")[2]
                if not msg:
                    response = "BAD-RQST-BODY\n"
                    conn.sendall(f"{response}".encode('utf-8'))
                    print(f"(Server): {response}")
                elif recipient not in user_list.keys():
                    #print(f"Unknown recipient {recipient}")
                    response = "UNKNOWN"
                    conn.sendall(f"{response}\n".encode('utf-8'))
                    print(f"(Server): {response}")
                else:
                    recipient_conn = user_list[recipient]
                    response = f"DELIVERY {sender} {msg}"
                    recipient_conn.sendall(f"{response}\n".encode('utf-8'))
                    print(f"(Server to {recipient}): {response}")
                    conn.sendall(f"SEND-OK\n".encode('utf-8'))
                    print(f"(Server): SEND-OK")
                    
            else:
                response = "BAD-RQST-HDR\n"
                conn.sendall(f"{response}".encode('utf-8'))
                print(f"(Server): {response}")
            
        except (OSError, ConnectionAbortedError) as e:
            print(e)
            client_connected = False
            del user_list[client_name]
            print(f"{addr} disconnected")
            conn.close()
            break
        
        except Exception as e:
            print(e)
            conn.close()
            break
    conn.close()



s.listen(64)
print(f"Server running on HOST: {HOST}, PORT: {PORT}")
while True:
    conn,addr = s.accept()
    thread = threading.Thread(target=client_handler,args=(conn,addr))
    thread.start()
    print(f"Connections: {threading.active_count() - 1}")
