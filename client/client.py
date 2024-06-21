import socket
import threading
import constants



#Thread breakers
threadAlive = True
exitProgram = False

# Members
members = []


# server information
serverIP = "192.168.178.21"
port = 14550

conn = False

# setup socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to server
#clientSocket.connect((serverIP, port))


def sendMessage(message2Send, recipient, Type):

    message = f"{Type}|{recipient}|{message2Send}".encode(constants.format)
    clientSocket.send(message)




def incommingMessage():

    while threadAlive:
        data = clientSocket.recv(constants.header)
        messageReceived = data.decode(constants.format)
        if messageReceived:
            messageReceived = messageReceived.split("|")

            # online member message
            if messageReceived[0] == constants.onlineMembers:
                members.append(messageReceived[2])
                
                
        

            # direct message
            if messageReceived[0] == constants.directMessage:
                print(f"MESSAGE: From {messageReceived[1]}: {messageReceived[2]}")




while not exitProgram:

    option = str(
        input(
            "Press 'C' to Connect, 'S' to Send Message 'D' to disconnect and L to view online members: "
        )
    )

    if (option.lower() == "c") and not conn:
        try:
            clientSocket.connect((serverIP, port))
            print("Connection Successful!!!")
            conn =  True

            thread = threading.Thread(target=incommingMessage)
            thread.start()

        except Exception as e:
            print(e)

    elif (option.lower() == "c") and conn:
        print("A connection has already been established...")

    elif(option.lower() != 'c') and not conn:
        print("You Must Connect first before doing other processes")

    if option.lower() == "s":
        Type = constants.directMessage
        print(f"Members : {members}\n")
        recipientIndex = int(input("Choose message recipient: "))
        recipient = members[recipientIndex]
        message = str(input("Type a Message: "))
        sendMessage(message, recipient, Type)

    if option.lower() == "d":
        message = clientSocket.send(constants.disconnect.encode(constants.format))
        exitProgram = True
        threadAlive = False
        conn = False

    if option.lower() == "l":
        Type = constants.onlineMembers
        recipient = ""
        message = ""
        members.clear()
        sendMessage(message, recipient, Type)
