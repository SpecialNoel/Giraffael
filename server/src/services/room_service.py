# room_service.py

import json
from fastapi import WebSocket
from src.db.mongo.room_ops.check_op import (check_room_existence_in_db, 
                                            check_client_existence_in_db)
from src.db.mongo.room_ops.create_op import create_room_in_db
from src.db.mongo.room_ops.join_op import join_room_in_db

async def handle_create_room_request(room_code, websocket: WebSocket):    
    # Check if the room exists in database
    room_exists_in_db = check_room_existence_in_db(room_code)
    if room_exists_in_db:
        data = {
            'message': f'Room {room_code} already exists in db',
            'status': 'failed'
        }
        await websocket.send_json(data)
        await websocket.close()
        return
    
    # Create the room
    create_room_in_db(room_code)
    return

async def handle_join_room_request(room_code, client_email, websocket: WebSocket):    
    # Check if the room exists in database
    room_exists_in_db = check_room_existence_in_db(room_code)
    if not room_exists_in_db:
        data = {
            'message': f'Room {room_code} does not exist in db',
            'status': 'failed'
        }
        await websocket.send_json(data)
        await websocket.close()
        return
    # Check if the client exists in the room and in database already
    client_exists_in_db = await check_client_existence_in_db(client_email, room_code)
    if client_exists_in_db:
        # Client tries to join a room they already in
        print(f'Client [{client_email}] was found in db.')
        data = {
            'message': f'Room {room_code} does not exist in db',
            'status': 'failed'
        }
        await websocket.send_json(data)
        await websocket.close()
        return
    else:
        print(f'Client [{client_email}] was not found in db.')
        join_room_in_db(room_code, client_email)
        return     
    