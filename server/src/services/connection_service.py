# connection_service.py

# Steps to inspect the keys stored in Redis (without <>): 
# 1. docker exec -it <container_name> sh
# 2. redis-cli
# 3. KEYS *
# 4. GET <key_name>

import json
import asyncio
import uuid
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Any
from src.services.message_service import handle_incoming_message
from src.crypto.session_id_generator import generate_session_id
from src.db.redis.connection_ops.disconnect_op import disconnect_from_client
from src.db.mongo.connection_ops.store_client_op import store_client_in_db

async def get_client_credentials(websocket: WebSocket):
    try:   
        credentials: Dict[str, Any] = await websocket.receive_json()
        client_email = credentials['email']
        client_hashed_password = credentials['password']
        return client_email, client_hashed_password
    except Exception as e:
        print(f'Error in get_client_credentials(): {e}')
        return None, None
    
async def handle_client_session_id_generation(websocket: WebSocket): 
    client_uuid = uuid.uuid4()
    client_uuid_str = str(client_uuid)
    session_id = generate_session_id()
    connection_result = {
        'message': 'Successfully connected to server',
        'status': 'succeeded',
        'user_id': client_uuid_str,
        'session_id': session_id
    }
    await websocket.send_json(connection_result)
    return client_uuid_str, session_id
    
async def client_loop(redis_client, websocket, TIME_THRESHOLD, session_id, room_code=None):
    async def safe_task(task):
        try:
            await task
        except Exception as e:
            print(f'Task failed: {e}.')
            
    while True:
        data = websocket.receive_json() # the old TIME_THRESHOLD mechanism were removed here
        asyncio.create_task(safe_task(handle_incoming_message(uuid, room_code, data)))
            
        # In Redis, set 'presence' of this uuid to 'online', which times out after TIME_THRESHOLD*2 seconds
        if room_code != None: 
            await redis_client.setex(f'presence:{room_code}:{session_id}', TIME_THRESHOLD*2, 'online')

# Connect the client with a generated uuid, received username and socket
async def connect_with_client(redis_client, active, websocket: WebSocket, TIME_THRESHOLD):
    try: 
        # Accept the connection established by client
        await websocket.accept()
        print('Accepted connection from the client')
        
        # Get credentials inputted by the client
        client_email, client_hashed_password = await get_client_credentials(websocket)
        if client_email == None or client_hashed_password == None:
            print(f'Received invalid credentials from client. Disconnect from the client.')
            connection_result = {
                'message': 'Failed connected to server',
                'status': 'failed'
            }
            await websocket.send_json(connection_result)
            await websocket.close()
            return 
        print('Received credentials from the client')

        # Generate a session id and send it to the client
        client_uuid, session_id = await handle_client_session_id_generation(websocket)
        print('Sent session id to the client')
        
        # Store this client to the 'Users' collection in MongoDB
        store_client_in_db(client_email, client_hashed_password, client_uuid, session_id)
        print(f'Successfully added the client to the database.')
        
        # Keep connection alive and forward incoming messages to other functions
        await client_loop(redis_client, websocket, TIME_THRESHOLD, session_id)
    except WebSocketDisconnect as wsde:
        print(f'Client disconnects from server. Exception: {wsde}')
    except Exception as e:
        print(f'Error in connect_with_client(): {e}.')
    finally:
        # Clean up client when it disconnects in any mean
        room_code = None # ------------------------------------- Use "Users" collection to find the room the client is in
        await disconnect_from_client(redis_client, active, session_id, room_code)
    return 

