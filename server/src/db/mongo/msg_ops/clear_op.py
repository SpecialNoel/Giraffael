# clear_op.py

from src.db.mongo.msg_ops.general_op import room_code_exists_in_collection
from src.db.mongo.mongodb_initiator import rooms_collection

# Clear all message history happened in this room
def clear_msg_history(room_code):
    if room_code_exists_in_collection(room_code):
        rooms_collection.update_one(
            {'room_code': room_code},
            {'$set': {'msgList':[]}}
        )
        print(f'Successfully cleared msg history in room with room code [{room_code}].')
    else: 
        print(f'Error in clear_msg(). Room [{room_code}] does not exist.')
    return
