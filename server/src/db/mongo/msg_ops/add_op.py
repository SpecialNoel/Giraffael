# add_op.py

from bson import ObjectId
from src.db.mongo.msg_ops.general_op import room_code_exists_in_collection
from src.db.mongo.mongodb_initiator import rooms_collection

# Add msg to the msg history in a room
def add_msg_to_history(room_code, senderID, senderName, msg):
    # Generate a metadata for msg in the following format
    # Note: senderID must be unique; senderName can be duplicate.
    def generate_metadata(senderID, senderName, msg):
        return {
            'senderID': senderID,
            'senderName': senderName,
            'message': msg
        }

    if room_code_exists_in_collection(room_code):
        msgWithMetadata = generate_metadata(senderID, senderName, msg)
        rooms_collection.update_one(
            {'room_code': room_code},
            {'$push': {'msgList': msgWithMetadata}}
        )
        print(f'Successfully added msg to the msgList of room with room code [{room_code}].')
    else: 
        print(f'Error in add_msg(). Room with room_code [{room_code}] does not exist.')
    return    
