# delete_op.py

# Delete the room in Redis (useful for removing 'zombie clients')
async def delete_room(redis_client, room_code):
    await redis_client.delete(f'room_code:{room_code}:client_list')
    print(f'Deleted room [{room_code}] in Redis.')
    return       
