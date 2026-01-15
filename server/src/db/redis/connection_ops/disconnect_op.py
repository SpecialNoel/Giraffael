# disconnect_op.py

from starlette.websockets import WebSocketState

# Disconnect client by removing it from local cache, 
#   closing the connection to its socket, and removing it from Redis.
async def disconnect_from_client(redis_client, active, session_id: str, room_code: str):
    # Remove client from active client list (local cache)
    if room_code in active and session_id in active[room_code]:
        websocket = active[room_code][session_id]['websocket']
        
        # Close the client socket if it is not yet closed by client side
        if websocket.client_state != WebSocketState.DISCONNECTED:
            try:
                await websocket.close()
            except:
                pass
        del active[room_code][session_id]
        print('Removed client from local active client list.')
        
        # Remove the room from the active client list if the room becomes empty
        if not active[room_code]:
            del active[room_code]
            print('Removed empty room.')
    
    # Remove client from Redis
    await redis_client.srem(f'room_code:{room_code}:client_list', session_id)
    await redis_client.delete(f'presence:{room_code}:{session_id}')
    print(f'Client [{session_id}] removed from connection manager.')
    return

# Disconnect all clients from a given room.
async def disconnect_all_clients_from_a_room(redis_client, active, room_code):
    if room_code in active:
        # Get a copy of session_ids
        session_ids = list(active[room_code].keys())
        
        # Remove every client from active client list (local cache)
        for uuid in session_ids:
            del active[room_code][uuid]
    
        # Remove the room from the active client list if the room becomes empty
        if not active[room_code]:
            del active[room_code]
            print('Removed empty room.')
            
        # Remove all clients in the given room from Redis
        if session_ids:
            await redis_client.srem(f'room_code:{room_code}:client_list', *session_ids)
            print(f'Removed all clients in room [{room_code}] from Redis.')
            
        current = await redis_client.smembers(f'room_code:{room_code}:client_list')
        print('After removing the client, Redis status: ', current)
            
        print(f'Removed all clients from room [{room_code}].')
        return
