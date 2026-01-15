# client_chat.py

# To run this script: python3 -m client.src.app.client_chat

import asyncio
from client.src.transport.websocket_client import connect

if __name__=='__main__':    
    server_ip = 'Giraffael.com' # domain for Giraffael
    tester_server_ip = '0.0.0.0'
    
    base_http_uri = f'http://{tester_server_ip}:8000/'
    base_ws_uri = f'ws://{tester_server_ip}:8000/ws'
    
    room_code = 'fWpO003k8b2'
    
    client = {
        'email': 'dodo321@gmail.com',
        'password': 'dodo123'
    }
    asyncio.run(connect(base_ws_uri, 
                        base_http_uri,
                        client['email'],
                        client['password']))
    