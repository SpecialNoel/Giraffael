# pub_sub_service.py

# Redis is used to transfer messages from the sender to the channel.

from datetime import datetime
from zoneinfo import ZoneInfo
from src.schemas.definitions import Message

# Redis subscribes to the channel (NOT client subscribe to channel)
async def subscribe_to_channel(redis, active, room_code):
    async def broadcast(room_code, msg_obj: Message):
        clients = active.get(room_code, {})
        for uuid, info in clients.items():
            try:
                await info['websocket'].send_json(msg_obj.model_dump())
                print(f'Sent json message to client [{uuid}].')
            except Exception as e:
                print(f'Failed to send json message to client [{uuid}]. Reason: {e}.')
    
    # Subscribe to channel
    pubsub = redis.pubsub()
    await pubsub.subscribe(f'room_code:{room_code}:channel')
    
    # Note: 'async for' runs indefinitely as a background task.
    async for msg in pubsub.listen():
        # Handle msg (with type of dict, defaulted by pubsub.listen() returns)
        if msg['type'] == 'message':
            print('Received a message from ')
            msg_obj = Message.model_validate_json(msg['data'].decode())
            await broadcast(room_code, msg_obj)
    return

# Publish Message to channel via Redis
async def publish_to_channel(redis, room_code, msg: Message):
    await redis.publish(f'room_code:{room_code}:channel', msg.model_dump_json())
    return     

# Publish chat message to channel via Redis
async def publish_chat_msg_to_channel(room_code, uuid, chat_msg):
    tz_NY = ZoneInfo('America/New_York')
    current_time = datetime.datetime.now(tz=tz_NY)
    
    msg = Message(
        type='chat',
        room_code=room_code,
        sender=uuid,
        payload={'data': chat_msg},
        timestamp=current_time
    )
    await publish_to_channel(room_code, msg)
    return
