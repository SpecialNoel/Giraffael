# check_op.py

# Get the online status of clients in Redis
async def get_online_status_of_clients_in_room(redis_client, room_code):
    # Get all uuids from the given room in Redis
    uuids = await redis_client.smembers(f'room_code:{room_code}:client_list')
    result = {}
    for uuid in uuids:
        presence = await redis_client.get(f'presence:{room_code}:{uuid}')
        result[uuid] = 'online' if presence else 'offline'
    return result