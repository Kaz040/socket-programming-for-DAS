import socket
import threading

# CONSTANTS
header = 2048
encodeFormat = "utf-8"
disconnectMessage = "!DISCONNECT"


# Members
members = []

# MessageType
directMessage = "DM"
onlineMembers = "OM"

# server information
serverIP = "141.44.219.53"
port = 14550

conn = None
# setup socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to server
clientSocket.connect((serverIP, port))


def sendMessage(message2Send, recipient, Type):

    message = f"{Type} | {recipient} | {message2Send}".encode(encodeFormat)
    clientSocket.send(message)


threadAlive = True


def incommingMessage():

    while threadAlive:

        data = clientSocket.recv(header)

        messageReceived = data.decode(encodeFormat)
        if messageReceived:
            messageReceived = messageReceived.split("|")

            # online member message
            if messageReceived[0] == onlineMembers:
                members.append(messageReceived[2])

            # direct message
            if messageReceived[0] == directMessage:
                print(f"MESSAGE: From {messageReceived[1]}: {messageReceived[2]}")


disconnect = False

while not disconnect:

    option = str(
        input(
            "Press 'C' to Connect, 'S' to Send Message 'D' to disconnect and L to view online members: "
        )
    )

    if (option.lower() == "c") and (conn is None):
        try:
            clientSocket.connect((serverIP, port))
            print("Connection Successful!!!")

            thread = threading.Thread(target=incommingMessage)
            thread.start()

        except Exception as e:
            print(e)

    elif (option.lower() == "c") and (conn is not None):
        print("A connection has already been established...")

    else:
        print("You Must Connect first before doing other processes")

    if option.lower() == "s":
        Type = directMessage
        recipient = str(input("Choose message recipient: "))
        message = str(input("Type a Message: "))
        sendMessage(message, recipient, Type)

    if option.lower() == "d":
        disconnect = True
        threadAlive = False

    if option.lower() == "l":
        Type = onlineMembers
        recipient = ""
        message = "onlineMembers"
        members.clear()
        sendMessage(message, recipient, Type)
