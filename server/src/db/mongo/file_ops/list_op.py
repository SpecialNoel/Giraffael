# list_op.py

from bson import ObjectId
from bson.errors import InvalidId

from src.db.mongo.msg_ops.general_op import room_code_exists_in_collection
from src.db.mongo.mongodb_initiator import gfs

# List all files in a room
def get_file_history(room_code):
    if not room_code_exists_in_collection(room_code):
        print(f'Error in get_file_history(). Room code [{room_code}] is invalid')
        return 
    
    # Find all files of given room
    files = gfs.find({'metadata.room_code': room_code})
    if not files.alive:
        print(f'There are no existing files in room [{room_code}].')
        return
    
    return [file.filename for file in files]

def get_fileID(filename, room_code):
    if not room_code_exists_in_collection(room_code):
        print(f'Error in get_file_history(). Room code [{room_code}] is invalid')
        return None
    
    files = gfs.find({
        'filename': filename,
        'metadata.room_code': room_code
    })
    file_ids = [file._id for file in files]
    if not file_ids:
        print(f'⚠️ No file found with filename [{filename}] in room [{room_code}]')
        return None
    return file_ids[0]
