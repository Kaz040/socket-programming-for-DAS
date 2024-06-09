import socket
import threading
import time

# [CONSTANTS]

# clients list
clients_list = []

# MessageType
directMessage = "DM"
onlineMembers = "OM"

# message information
header = 20480
decodeFormat = "utf-8"
disconnect = "!DISCONNECT"


# server information
serverIP = socket.gethostbyname(socket.gethostname())
port = 14550

# socket instance
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((serverIP, port))


def handle_connection(conn, addr):
    print(f"[NEW COONECTION] {addr} connected.")
    client_object = {
        "conn" : "",
        "addr" : ""
    }
    #register_client

    client_object["conn"] = conn
    client_object["addr"] = str(addr)
    clients_list.append(client_object)
    print(f"[ACTIVE CONNECTIONS] {len(clients_list)}")

    connected = True

    while connected:
        msg = conn.recv(header).decode(decodeFormat)
        msg = str(msg)
        if msg == disconnect:
            print(f"[{addr}] is disconnecting...")
            for client in clients_list:
                if client["addr"] == str(addr):
                    clients_list.remove(client)
                    
                    connected = False
                
        elif msg:
            message = msg.split("|")
            if message[0] == directMessage:
                for client in clients_list:
                    if client["addr"] == message[1]:
                        forwardConnection = client["conn"]
                        message[1] = str(addr)
                        msg = f"{message[0]}|{message[1]}|{message[2]}".encode(decodeFormat)
                        forwardConnection.send(msg)
            
            if str(message[0]) == onlineMembers:
                for client in clients_list:
                    time.sleep(0.2)
                    clientMembers2String = client["addr"]
                    msg = f"{message[0]}|{message[1]}|{clientMembers2String}".encode(decodeFormat)
                    conn.send(msg)
                

    print(f"INFO: [{addr}] is disconnected")
    print(f"[ACTIVE CONNECTIONS] {len(clients_list)}")
    conn.close()


def startServer():
    serverSocket.listen(4)
    print("[STARTING] server is starting")
    print(f"[LISTENING] Server is listening on {serverIP}")
    while True:
        conn, addr = serverSocket.accept()
        thread = threading.Thread(target=handle_connection, args=(conn, addr))
        thread.start()
        


startServer()
