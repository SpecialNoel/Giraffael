# websocket_client.py

import asyncio
import websockets
import json
from client.src.transport.send_msg import (send_chat_message,
                                           send_create_room_request,
                                           send_disconnect_request)
from client.src.transport.recv_msg import receive_msg

async def user_input_loop(websocket, http_uri, username, room_code, uuid):
    async def send(msg_type, http_uri=None, username=None, uuid=None, room_code=None, websocket=None, msg=None):
        if msg_type == 'chat':
            await send_chat_message(room_code, str(uuid), msg, websocket)
        elif msg_type == 'create':
            await send_create_room_request(http_uri, username, room_code)
        elif msg_type == 'disconnect':
            await send_disconnect_request(websocket)
        return

    msg_type_prompt = (f'\nEnter "create" to create a room with room code {room_code}.\n'
                        'Enter "disconnect" to disconnect from server.\n'
                        'Enter "chat" to start chatting.\n')
    msg_prompt = ('\nEnter "disconnect" to disconnect from server.\n'
                  'Enter anything else to input your message.\n')
    while True:
        msg_type = input(msg_type_prompt).lower()
        
        if msg_type == 'chat':
            msg = input(msg_prompt).lower()
            await send(msg_type, http_uri, username, uuid, room_code, websocket, msg)
        elif msg_type == 'create' or msg_type == 'disconnect':
            await send(msg_type, http_uri, username, uuid, room_code, websocket, '')
            if msg_type == 'disconnect':
                break
        else:
            print('Please enter a valid option.\n')
    return

async def connect(ws_uri, http_uri, room_code, uuid, username):
    uri = ws_uri + f'?room_code={room_code}&uuid={uuid}&username={username}'
    print(f'uri: [{uri}].')
    
    # Client connects to server via WebSocket endpoint
    async with websockets.connect(uri) as websocket:        
        msg = await websocket.recv()
        data = json.loads(msg)
        print(f'Response from server: {data}')
        
        if data['status'] != 'succeeded':
            print('Failed to connect to server.')
            return
        print('Successfully connected to server.')
        
        # Start receiving heartbeat in the background
        receiver_thread = asyncio.create_task(receive_msg(websocket))
        sender_thread = asyncio.create_task(user_input_loop(websocket, http_uri, username, room_code, uuid))
        
        # Wait until either thread to finish (either disconnects or error occurs)
        done, pending = await asyncio.wait(
            [receiver_thread, sender_thread],
            return_when=asyncio.FIRST_COMPLETED
        )
        
        # Cancel the unfinished tasks before stopping the client loop
        for task in pending:
            task.cancel()
        print('Client loop ended.')
