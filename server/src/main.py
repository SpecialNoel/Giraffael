# main.py

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.services.connection_manager import manager
from src.routers import websocket_routes, room_routes, file_routes, message_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: manager connects to Redis
    await manager.start()
    yield
    # Shutdown: manager stops Pub/Sub services and closes connection to Redis
    await manager.stop()

app = FastAPI(lifespan=lifespan) # initialize the application with manager
app.include_router(websocket_routes.router) # enable the client to connect to the manager via '/ws'
app.include_router(room_routes.router)      # enable the client to connect to the manager via '/room/...'
app.include_router(file_routes.router)       # enable the client to connect to the manager via '/upload/...' and '/download/...'
app.include_router(message_routes.router)   # enable the client to connect to the manager via '/send' and '/fetch'

# The following code is commented due to it not being executed with 'docker build'.
# if __name__=='__main__':
#     # Run a uvicorn web server. Initialize a server socket and binds it to the 
#     #   given host and port.
#     uvicorn.run(app, host='0.0.0.0', port=8000)
