import socket

def create_server_socket(serverAddress, serverPort):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((serverAddress, serverPort))
    return serverSocket

def accept_connection(serverSocket):
    (conn, address) = serverSocket.accept()
    print(f'Accepted connection request from Client[{address}].')
    
    with conn:
        while True:
            rcvpkt = conn.recv(1024)
            if not rcvpkt: break
            print(f'Received from Client[{address}]: ', rcvpkt.decode())
    print(f'Disconnected from Client[{address}].')
    
if __name__=='__main__':
    serverAddress = "127.0.0.1"
    serverPort = 17990
    serverSocket = create_server_socket(serverAddress, serverPort)
    
    serverSocket.listen()
    print(f'Server socket[{serverAddress}, {serverPort}] started listening.')
    accept_connection(serverSocket)
    
    serverSocket.close()
    print('Server socket closed')
    