# Server.py
# Run: `python3 Server.py` to start the web Server

from flask import Flask, render_template, url_for, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_socketio import ConnectionRefusedError, Namespace

# Initialize flask and flask_socketio.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key!'
socketio = SocketIO(app)

clients = [] # store all currently connected clients

''' Frontend Page '''
@app.route('/')
def index():
    return render_template('home.html')

''' Socket Related '''    
@socketio.on('connect')
def handle_connect():
    print(f'Client [{request.sid}] connected successfully')
    clients.append(request.sid)
    display_connecting_clients()
    emit('after connect', {'data':'Lets dance'})
    
@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client [{request.sid}] disconnected successfully')
    clients.remove(request.sid)
    display_connecting_clients()
    
@socketio.on('server-receive-message')
def handle_receive_message(data):
    print(f'Received message from Client [{request.sid}]')
    print('Message:', data)
    
    data = 'Hi [' + request.sid + '], this is a response sent from Server!'
    handle_send_message(request.sid, data)
    
@socketio.on('server-send-message')
def handle_send_message(client_id, data):
    print(f'Send message to Client [{client_id}]:', data)
    emit('response:', data, room=client_id)
    
''' Helper Functions '''
def display_connecting_clients():
    print('Current connecting Clients: ', clients)

''' Main '''
if __name__=='__main__':
    socketio.run(app, host='127.0.0.1', port=5001) # port cannot be 5000
    