# upload_op.py

import os
from bson import ObjectId
from bson.errors import InvalidId
from src.db.mongo.msg_ops.general_op import room_code_exists_in_collection
from src.db.mongo.file_ops.general_op import check_file_existence_in_room
from src.db.mongo.mongodb_initiator import rooms_collection, gfs

# Upload file to a room
def upload_file(file_path, room_code):    
    # Generate a unique filename to avoid uploading a file with a duplicated filename
    #   as existing files in given room
    # Note: room_code used here will be in correct format as we'll check it before executing here
    def generate_filename_with_unique_postfix(filenameWithExt, room_code):
        counter = 1
        filename, extension = os.path.splitext(filenameWithExt)
        temp_filename = filenameWithExt
        # If there is a file with the same filename stored in current room, try a new postfix
        while check_file_existence_in_room(temp_filename, room_code):
            temp_filename = f'{filename}_{counter}{extension}'
            counter += 1
        return temp_filename
    
    # Check if file_path is valid here
    print(f'File path: [{file_path}]')
    if not check_if_file_exists(file_path):
        print(f'Error in upload_file(). File path [{file_path}] is invalid.')
        return -1
        
    # Find the given room
    room = None
    try:
        room = rooms_collection.find_one(
            {'room_code': room_code}
        )
    except InvalidId:
        print(f'Error in upload_file(). Room code [{room_code}] is invalid.')
        return -1
    
    if not room:
        print(f'Error in upload_file(). Room code [{room_code}] does not exist.')
        return -1
    
    # Handle name of the file, if it is not unique
    nameOfFile = os.path.basename(file_path)
    if check_file_existence_in_room(nameOfFile, room_code):
        nameOfFile = generate_filename_with_unique_postfix(nameOfFile, room_code)
    
    # Store the file along with its name and metadata to the database
    with open(file_path, 'rb') as f:
        fileID = gfs.put(
            f,
            filename=nameOfFile,
            metadata={'room_code': room_code}
        )
    # Update the fileList of the room
    rooms_collection.update_one(
        {'room_code': room_code},
        {'$push': {'fileList': {
            'fileID': fileID,
            'filename': nameOfFile
        }}}
    )
    print(f'Uploaded file [{nameOfFile}] with fileID [{fileID}] to room [{room_code}].')
    return fileID
