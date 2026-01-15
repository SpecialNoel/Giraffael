# recv_msg.py

import websockets

async def handle_incoming_message(msg):
    print(f'Received msg: {msg}')
    return

async def receive_msg(websocket):
    try:
        async for raw_msg in websocket:
            await handle_incoming_message(raw_msg)
    except websockets.ConnectionClosed:
        # websockets library manages the heartbeat mechanism automatically
        print('Connection closed by server.')
    except Exception as e:
        print(f'Unexpected error in recv_heartbeat(): {e}.')
