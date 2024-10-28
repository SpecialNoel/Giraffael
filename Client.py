import socket

def create_client_socket(serverAddress, serverPort):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverAddress, serverPort)) 
    return clientSocket

def send(clientSocket, message):
    clientSocket.send(message.encode())
    print(f'Sent message: "{message}" to Server')

if __name__ == '__main__':
    serverAddress = ''
    serverPort = 17990
    clientSocket = create_client_socket(serverAddress, serverPort)

    send(clientSocket, 'Hello, server')

    clientSocket.close()
    print('Client socket closed')