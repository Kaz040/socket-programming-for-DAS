import socket
import threading

network_analysis = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_IP = "192.168.0.103"
server_Port = 14500
network_analysis.bind((server_IP, server_Port))
network_analysis.listen(10)
print("waiting for connection")
client_list = []
server = True

def client_message_listener(client_connection, client_address):
    while True:
        received_message = client_connection.recv(1024)
        data = received_message.decode("utf-8")
        print("data = ", data)
        if data != "":
            data = data.split("|")
            if data[2] == "2":
                for client_2_message in client_list:
                    if (data[0] == client_2_message[1][0] and int(data[1]) == client_2_message[1][1]):
                        print(f"message: {data[3]} received from {client_address} : going to {client_2_message[1]}")
                        client_2_message[0].send(bytes(f"{client_address[0]}|{client_address[1]}|2|{data[3]}", "utf-8"))
        
        if not received_message:
            if client_list:
                for client_2_remove in client_list:
                    if client_address == client_2_remove[1]:
                        client_list.pop(client_list.index(client_2_remove))
                        if client_list:
                            for client in client_list:
                                client[0].send(bytes(f"{client[1][0]}|{client[1][1]}|1|{server_IP}", "utf-8"))
                    break

            break
    print(f"connection with {client_connection} is closing")
    client_connection.close()
    
    return server
    



while server:
    client_connection, client_address = network_analysis.accept()
    try:
        print(f"client with IP_address {client_address[0]} and port number {client_address[1]} just connected")
        client_information = [client_connection, client_address]
        
        if client_list:
            for client in client_list:
                client_connection.send(bytes(f"{client[1][0]}|{client[1][1]}|1|{server_IP} ", "utf-8"))
                client[0].send(bytes(f"{client_address[0]}|{client_address[1]}|1|{server_IP} ", "utf-8"))
        client_list.append(client_information)
        #start a thread to listening for a message from client
        message_listener = threading.Thread(target=client_message_listener, args=(client_connection,client_address, ))
        message_listener.start()


    except KeyboardInterrupt:
        print(f"Closing Server")
        network_analysis.close()
        break

