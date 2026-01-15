# sned_msg.py

import requests

async def send_create_room_request(base_http_uri, session_id, room_code):
    print('Sending the create room request to server.')
    
    room_creation_uri = base_http_uri + '/room/create'
    data = {
        'room_code': room_code, 
        'session_id': session_id
    }
    
    response = requests.post(room_creation_uri, json=data)
    print(f'Response status code: {response.status_code}')
    print(f'Received status from server: {response.json()}')
    return

async def send_disconnect_request(websocket):
    await websocket.close()
    print('Disconnected from server. Exited')
    return
