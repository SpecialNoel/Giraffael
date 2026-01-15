# check_op.py

from src.db.mongo.mongodb_initiator import rooms_collection
from src.db.mongo.msg_ops.general_op import room_code_exists_in_collection

# Check whether room with given room code exist in MongoDB
def check_room_existence_in_db(room_code):
    room_exists_in_db = room_code_exists_in_collection(room_code)
    if room_exists_in_db:
        print(f'Room [{room_code}] exists in MongoDB.')
    else:
        print(f'Room [{room_code}] does not exist in MongoDB.')
    return room_exists_in_db

# Try match given room code, uuid and username with records in MongDB 
async def check_client_existence_in_db(client_email, room_code):
    client = rooms_collection.find_one(
        {
            'room_code': room_code,
            'clientList': {
                '$elemMatch': {
                    'client_email': client_email
                }
            }
        },
        {'clientList.$': 1}
    )
    print(f'\nClient: [{client}]\n')
    return True if client is not None else False
