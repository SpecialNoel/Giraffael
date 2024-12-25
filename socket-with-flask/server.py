# Server.py
# Run: `python3 Server.py` to start the web Server

from flask import Flask, render_template, url_for, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_socketio import ConnectionRefusedError, Namespace

# Initialize flask and flask_socketio.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key!'
socketio = SocketIO(app)

connected_clients = [] # store all currently connected clients

''' Frontend Page '''
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def handle_enter_room_id_form_post():
    room_id = request.form['room-id']
    print(f'***Received client input for enter-room-id: {room_id}***')
    return
    
@app.route('/room1', methods=['POST'])
def handle_enter_room1_get():
    print(f'***Received client input of clicking the Enter-Room1 button.***')
    return render_template('room.html')

''' Socket Related '''    
@socketio.on('connect')
def handle_connect():
    print(f'***Client [{request.sid}] connected successfully***')
    connected_clients.append(request.sid)
    display_connecting_clients()
    emit('connect', {'clientId':request.sid})
    emit('client_list_update', {'clients':connected_clients}, broadcast=True)
    
@socketio.on('disconnect')
def handle_disconnect():
    print(f'***Client [{request.sid}] disconnected successfully***')
    connected_clients.remove(request.sid)
    display_connecting_clients()
    emit('client_list_update', {'clients':connected_clients}, broadcast=True)
    
@socketio.on('receive-message')
def handle_receive_message(data):
    print(f'***Received message from Client [{request.sid}]***')
    print(f'***Message: {data['msg']}***')
    
    data = 'Hi [' + request.sid + '], this is a response sent from Server!'
    handle_send_message(request.sid, data)
    
@socketio.on('send-message')
def handle_send_message(client_id, data):
    print(f'***Send message to Client [{client_id}]: {data}***')
    emit('response', data, room=client_id)
    
''' Helper Functions '''
def display_connecting_clients():
    print(f'***Current connecting Clients: {connected_clients}***')

''' Main '''
if __name__=='__main__':
    socketio.run(app, host='127.0.0.1', port=5001) # port cannot be 5000
    