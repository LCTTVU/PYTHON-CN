received_message = "DELIVERY echobot test test 123123 hhyhdyhasdyhad\n"
if (received_message.startswith("DELIVERY")):
    received_message = received_message[9:]
    print(received_message)
    username = received_message.partition(" ")[0]
    print(username)
    message = received_message.partition(" ")[2]
    message = "FROM: " + username + "\nMESSAGE: " + message
    print(message)