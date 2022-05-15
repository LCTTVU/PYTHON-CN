received_msg = "SEND bucac hi\n"
if (received_msg.startswith("SEND")):
    received_msg = received_msg[5:]
    forward_user = received_msg.partition(" ")[0]
    message = received_msg.partition(" ")[2]
    print(f"{forward_user}\n")
    print(f"{message}")