# websocket_routes.py

from fastapi import APIRouter, WebSocket
from src.services.connection_manager import manager

router = APIRouter()

# WebSocket endpoint that acts like listen() and accept() in python socket
@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    print(f'websocket [{websocket}] is trying to connect to server.')
    await manager.connect(websocket)
