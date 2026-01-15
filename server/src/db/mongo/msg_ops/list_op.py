# list_op.py

from src.db.mongo.msg_ops.general_op import room_code_exists_in_collection
from src.db.mongo.mongodb_initiator import rooms_collection

# List out all messages sent over this room
def list_msg_history(room_code):
    if room_code_exists_in_collection(room_code):
        print(f'Msg history stored in room [{room_code}]:')
        room = rooms_collection.find_one(
            {'room_code': room_code}
        )
        msgMetadatas = room['msgList']
        for msgMetadata in msgMetadatas:
            print(f'[{msgMetadata['senderName']}]: [{msgMetadata['message']}]')
    else:
        print(f'Error in list_msg(). Room [{room_code}] does not exist.')
    return

def get_msg_history(room_code):
    if room_code_exists_in_collection(room_code):
        print(f'Msg history stored in room [{room_code}]:')
        room = rooms_collection.find_one(
            {'room_code': room_code}
        )
        msgHistory = []
        msgMetadatas = room['msgList']
        for msgMetadata in msgMetadatas:
            msgHistory.append({msgMetadata['senderName']: msgMetadata['message']})
        return msgHistory
    else:
        print(f'Error in list_msg(). Room [{room_code}] does not exist.')
    return None
