import socket
import threading
client_network = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
friend_list = []


#server_IP = str(input("Enter Server IP: "))

#server_port = int(input("Enter Server Port "))

def message_sender(client):

    while True:
        client_index = int(input())
        message_to_send = input()
        client_to_message = friend_list[client_index]
        client.send(bytes(f"{client_to_message[0]}|{client_to_message[1]}|2|{message_to_send}", "utf-8"))

def message_listener(client_network):
    while True:
        try:
            data_received = client_network.recv(1024)
            data = data_received.decode("utf-8")
            if data != "":
                data = data.split("|")
                if data[2] == "1":
                    friend_list.append((data[0],data[1]))
                    print(friend_list)
                elif data[2] == "2":
                    if len(data) > 4:
                        newData = ""
                        for extractedData in data[3:]:
                            if extractedData[0] == " ":
                                newData = newData + extractedData[1:]
                            else: 
                                newData = newData + extractedData
                        print(f"[{data[0]}, {data[1]}]: {newData}")
                    else:
                        print(f"[{data[0]}, {data[1]}]: {data[3]}")
            

        except KeyboardInterrupt:
            client.close()


client_network.connect(('192.168.0.103', 14500))
messageListenerThread = threading.Thread(target=message_listener, args=(client_network, ))
messageListenerThread.start()

message_sender(client_network)

    
