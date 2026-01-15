# room_routes.py

from fastapi import APIRouter, WebSocket
from src.schemas.definitions import RoomRequest
from src.services.room_service import (handle_create_room_request, 
                                       handle_join_room_request)

router = APIRouter()

# FastAPI endpoint for handling a 'create room' request from a client
@router.post('/room/create')
async def create_room(request: RoomRequest, websocket: WebSocket):
    room_code = request.room_code
    return await handle_create_room_request(room_code, websocket)

# FastAPI endpoint for handling a 'join room' request from a client
@router.post('/room/join')
async def join_room(request: RoomRequest, websocket: WebSocket):
    room_code = request.room_code
    client_email = request.client_email
    return await handle_join_room_request(room_code, client_email, websocket)
