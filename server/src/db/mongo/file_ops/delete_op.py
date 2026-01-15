# delete_op.py

from bson import ObjectId
from bson.errors import InvalidId
from src.db.mongo.msg_ops.general_op import room_code_exists_in_collection
from src.db.mongo.mongodb_initiator import rooms_collection, gfs

# Delete a file in a room
def delete_file(fileID, room_code):
    try:
        file = gfs.find_one({'_id': ObjectId(fileID)})
        if not file:
            print(f'Error in delete_file(). File with fileID [{fileID}] does not exist in database.')
            return
    except InvalidId:
        print(f'Error in delete_file(). fileID [{fileID}] is invalid.')
                
    # Test if given room code is in invalid format
    if not room_code_exists_in_collection(room_code):
        print(f'Error in delete_file(). Room code [{room_code}] is invalid.')
        return
    
    if file.metadata['room_code'] != room_code:
        print(f'Error in delete_file(). File with fileID [{fileID}] does not exist in room code [{room_code}].')
        return 
    
    # Delete the file, indicated by the fileID, from the database
    gfs.delete(ObjectId(fileID))
    # Remove the filename, indicated by the fileID, from 'fileList' of this room    
    rooms_collection.update_one(
        {'room_code': room_code},
        {'$pull': {'fileList': {'fileID': ObjectId(fileID)}}}
    )
    print(f'Successfully deleted file with fileID [{fileID}] in room [{room_code}].')
    return

# Delete all files in a room
def delete_all_files(room_code):
    # Use room code to get all fileIDs of the room, then use the fileIDs to delete all files
    try:
        files = gfs.find({'metadata.room_code': room_code})
    except InvalidId:
        print(f'Error in delete_all_files(). Room code [{room_code}] is invalid')
        return
    
    if not files.alive:
        print(f'There are no existing files in room [{room_code}].')
        return
    for file in files:
        print(f'FileID to be deleted: [{file._id}]')
        delete_file(file._id, room_code)
    print(f'Successfully deleted all files from room [{room_code}].')
    return
