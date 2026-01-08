# create_op.py

import datetime
from zoneinfo import ZoneInfo
from src.db.mongo.mongodb_initiator import rooms_collection

# Create a room in MongoDB
def create_room_in_db(room_code, roomName='NewRoom'):
    try: 
        tz_NY = ZoneInfo('America/New_York')
        current_time = datetime.datetime.now(tz=tz_NY)
        
        # Room default template
        room_data = {
            'roomCode': room_code,
            'roomName': roomName,
            'clientList': [],
            'msgList': [],
            'fileList': [],
            'creationDate': current_time
        }

        # Add room to the room collection
        rooms_collection.insert_one(room_data)
        print(f'Created room in DB with room code [{room_code}]. ')
        return True
    except: 
        print(f'Error in create_room_in_db() with room code [{room_code}].')
        return False
