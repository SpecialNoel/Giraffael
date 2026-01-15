# websocket_client.py

import asyncio
import json
import websockets
from client.src.transport.send_msg import (send_create_room_request,
                                           send_disconnect_request)
from client.src.transport.recv_msg import receive_msg
from client.src.crypto.hash_client_password import hash_password

async def user_input_loop(websocket, http_uri, session_id):
    async def send(msg_type, http_uri, session_id, websocket=None, room_code=None):
        if msg_type == 'create':
            await send_create_room_request(http_uri, session_id, room_code)
        elif msg_type == 'disconnect':
            await send_disconnect_request(websocket)
        return

    msg_type_prompt = (f'\nEnter "create" to create a room.\n'
                        'Enter "disconnect" to disconnect from server.\n')
    msg_prompt = ('\nEnter "disconnect" to disconnect from server.\n'
                  'Enter anything else to input your message.\n')
    while True:
        msg_type = input(msg_type_prompt).lower()

        if msg_type == 'create' or msg_type == 'disconnect':
            await send(msg_type, http_uri, session_id, websocket)
            if msg_type == 'disconnect':
                break
        else:
            print('Please enter a valid option.\n')
    return

async def connect(ws_uri, http_uri, client_email, client_password):    
    # Try connecting to server via '/ws', the WebSocket endpoint
    # A sample uri: ws_uri + f'?client_email={email}&client_password={password}'
    async with websockets.connect(ws_uri) as websocket:      
        # Hash client password
        hashed_password = None
        while hashed_password == None:
            hashed_password = hash_password(client_password)            
        
        # Send client credentials to server
        credentials = {
            'email': client_email,
            'password': hashed_password
        }
        await websocket.send(json.dumps(credentials))
        print('Sent credentials to server.')
        
        # Receive response from server
        data_json = await websocket.recv()
        data = json.loads(data_json)
        print(f'Response from server: {data}')
                
        if data['status'] != 'succeeded':
            print('Failed to connect to server.')
            websocket.close()
            print('Websocket connection closed')
            return
        print('Successfully connected to server.')
        
        # Obtain session id for this client from server
        session_id = data['session_id']
        print(f'Obtained session id from server: {session_id}')
        
        # Start receiving heartbeat in the background
        receiver_thread = asyncio.create_task(receive_msg(websocket))
        sender_thread = asyncio.create_task(user_input_loop(websocket, http_uri, session_id))
        
        # Wait until either thread to finish (either disconnects or error occurs)
        done, pending = await asyncio.wait(
            [receiver_thread, sender_thread],
            return_when=asyncio.FIRST_COMPLETED
        )
        
        # Cancel the unfinished tasks before stopping the client loop
        for task in pending:
            task.cancel()
        print('Client loop ended.')
