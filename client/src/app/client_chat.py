# client_chat.py

# To run this script: python3 -m client.src.app.client_chat

import asyncio
import uuid
from client.src.transport.websocket_client import connect

if __name__=='__main__':    
    server_ip = 'Giraffael.com' # domain for Giraffael
    tester_server_ip = '0.0.0.0'
    base_http_uri = f'http://{tester_server_ip}:8000/'
    base_ws_uri = f'ws://{tester_server_ip}:8000/ws'
    
    client_for_testing = {
        'username': 'dodo',
        'room_code': 'fWpO003k8b2',
        'client_uuid': uuid.uuid4()
    }
    asyncio.run(connect(base_ws_uri, 
                        base_http_uri,
                        client_for_testing['room_code'], 
                        client_for_testing['client_uuid'], 
                        client_for_testing['username']))
    