# connection_manager.py

import redis.asyncio as redis
from fastapi import WebSocket
from src.services.client_service import (connect_with_client, 
                                                 disconnect_from_client, 
                                                 disconnect_all_clients_from_a_room)
from src.services.room_service import delete_room
from src.services.pub_sub_service import subscribe_to_channel

class ConnectionManager:
    def __init__(self, redisURL='redis://localhost:6379'):
        # room_code maps to { uuid maps to (WebSocket, username) }
        self.active: dict[str, dict[str, dict[WebSocket, str]]] = {}
        self.redisURL = redisURL
        self.redis = None
        self.TIME_THRESHOLD = 20
        self.MAX_USER_CAPACITY_PER_ROOM = 5
        
    # Connect to Redis and sub to the channel
    async def start(self):
        try: 
            self.redis = await redis.from_url(self.redisURL, decode_responses=True)
            subscribe_to_channel(self.redis, self.active, )
            print('Connected to Redis.')
        except:
            print('Failed to connect to Redis')
        return

    # Stop Pub/Sub listener and close Redis connection    
    async def stop(self):        
        if self.redis:
            for room_code in self.active:
                await self.disconnect_all(room_code)
                await delete_room(self.redis, room_code) # Delete room in Redis
            await self.redis.close()
            print('Server disconnected from Redis.')
    
    # Connect the client with a generated uuid, received username and socket to Redis
    async def connect(self, websocket: WebSocket):
        return await connect_with_client(self.redis, self.active, websocket, self.TIME_THRESHOLD)
    
    # Disconnect client by removing it from local cache, 
    #   closing the connection to its socket, and removing it from Redis.
    async def disconnect(self, uuid, room_code):
        return await disconnect_from_client(self.redis, self.active, uuid, room_code)
    
    # Disconnect all clients from a given room in Redis.
    async def disconnect_all(self, room_code):
        return await disconnect_all_clients_from_a_room(self.redis, self.active, room_code)

# A singleton that is used to share stored resources over functions in different scripts
# With Redis, data values like chat msg can be shared across multiple workers/service instances.
manager = ConnectionManager()
