import socket

# MessageType
directMessage = "DM"
onlineMembers = "OM"

# message information
header = 20480
format = "utf-8"
disconnect = "!DISCONNECT"


# server information
serverIP = socket.gethostbyname(socket.gethostname())
port = 14550