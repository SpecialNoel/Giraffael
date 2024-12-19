# Client.py
# Run: `python3 Client.py` to start the Client side

import socketio
import time

# Initialize socketio.
clientSIO = socketio.Client()

''' Socket Related '''
@clientSIO.event
def connect():
    print('Connection with Server established')

@clientSIO.event
def response(data):
    print('Received message from Server:', data)
    
@clientSIO.event
def disconnect():
    print('Disconnected from Server')


if __name__== '__main__':
    clientSIO.connect(url='http://127.0.0.1:5000', transports=['websocket'])
    print("Socket established")
        
    msg = 'Hello! This is Client'
    clientSIO.emit('Message from Client:', msg)
    
    clientSIO.wait()
    