# Server.py
# Run: `python3 Server.py` to start the web Server

from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_socketio import ConnectionRefusedError, Namespace

# Initialize flask and flask_socketio.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key!'
socketio = SocketIO(app)

''' Frontend Page '''
@app.route('/')
def index():
    return render_template('home.html', user_level='Server')





''' Socket Related '''    
@socketio.on('connect')
def handle_connect():
    app.logger.info('A Client connected successfully')
    print('Client connected')
    
@socketio.on('message')
def handle_message(data):
    print(f'Received message from Client:', data)
    app.logger.info('Received a message from Client successfully')
    socketio.emit('Message:', data)
    
@socketio.on('disconnect')
def handle_disconnect():
    print('Disconnected')


if __name__=='__main__':
    socketio.run(app, port=5000, debug=True) # run flask_socketio to start the SocketIO web server
    