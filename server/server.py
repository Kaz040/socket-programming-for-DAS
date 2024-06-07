import socket
import threading


# [CONSTANTS]

# clients list
clients_list = []



# message information
header = 2048
decodeFormat = "utf-8"
disconnect = "!DISCONNECT"


# server information
serverIP = socket.gethostbyname(socket.gethostname())
port = 14550

# socket instance
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((serverIP, port))

def getActiveConnection():

    pass

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
    print(f"On Connection: {clients_list}")
    print(f"[ACTIVE CONNECTIONS] {len(clients_list)}")

    connected = True

    while connected:
        msg = conn.recv(header).decode(decodeFormat)
        if msg == disconnect:
            print(f"[{addr}] is disconnecting...")
            print(f"Before Removing: {clients_list}")
            for client in clients_list:
                if client["addr"] == str(addr):
                    clients_list.remove(client)
                    print(f"After Removing: {clients_list}")
                    connected = False
                
        elif msg:    
            print(f"[{addr}] {msg}")

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
