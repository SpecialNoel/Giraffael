# connection_manager.py

import os
import time
import redis.asyncio as redis
from fastapi import WebSocket
from src.services.client_service import (connect_with_client, 
                                         disconnect_from_client, 
                                         disconnect_all_clients_from_a_room)
from src.services.room_service import delete_room
from src.services.pub_sub_service import subscribe_to_channel

redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_port = 6379

class ConnectionManager:
    def __init__(self):
        # room_code maps to { uuid maps to (WebSocket, username) }
        self.active: dict[str, dict[str, dict[WebSocket, str]]] = {}
        self.redis_client = None
        self.TIME_THRESHOLD = 60
        self.MAX_USER_CAPACITY_PER_ROOM = 5
        
    # Connect to Redis client
    async def start(self):
        while True:
            try: 
                # self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
                self.redis_client = redis.from_url(f'redis://{redis_host}:{redis_port}?decode_responses=True')
                await self.redis_client.ping()
                print('Connected to Redis.')
                break
            except redis.exceptions.ConnectionError:
                print("Redis connection failed, retrying...")
                time.sleep(2)
            except Exception as e:
                print('Failed to connect to Redis')
                print(f'Exception: {e}')
        return
    
    # Subscribe to a channel
    async def subscribe(self, room_code):
        try: 
            subscribe_to_channel(self.redis_client, self.active, room_code)
            print('Subscribed to channel.')
        except Exception as e:
            print(f'Failed to subscribe to channel {room_code}')
            print(f'Exception: {e}')
        return

    # Stop Pub/Sub listener and close Redis connection    
    async def stop(self):        
        if self.redis_client:
            for room_code in self.active:
                await self.disconnect_all(room_code)
                await delete_room(self.redis_client, room_code) # Delete room in Redis
            await self.redis_client.close()
            print('Server disconnected from Redis.')
    
    # Connect the client with a generated uuid, received username and socket to Redis
    async def connect(self, websocket: WebSocket):
        return await connect_with_client(self.redis_client, self.active, websocket, self.TIME_THRESHOLD)
    
    # Disconnect client by removing it from local cache, 
    #   closing the connection to its socket, and removing it from Redis.
    async def disconnect(self, uuid, room_code):
        return await disconnect_from_client(self.redis_client, self.active, uuid, room_code)
    
    # Disconnect all clients from a given room in Redis.
    async def disconnect_all(self, room_code):
        return await disconnect_all_clients_from_a_room(self.redis_client, self.active, room_code)

# A singleton that is used to share stored resources over functions in different scripts
# With Redis, data values like chat msg can be shared across multiple workers/service instances.
manager = ConnectionManager()
