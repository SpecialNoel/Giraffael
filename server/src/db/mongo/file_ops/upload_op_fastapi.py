# upload_op_fastapi.py

from bson.errors import InvalidId
from fastapi import File, UploadFile
from src.db.mongo.mongodb_initiator import rooms_collection, gfs

# Upload file to a room using FastAPI
def upload_file_with_fastapi(room_code: str, file: UploadFile = File(...)):        
    # # Find the given room
    room = None
    try:
        room = rooms_collection.find_one(
            {'room_code': room_code}
        )
    except InvalidId:
        print(f'Error in upload_file(). Room code [{room_code}] is invalid.')
        return -1
    
    if not room:
        print(f'Error in upload_file(). Room [{room_code}] does not exist.')
        return -1
    
    contents = file.file.read()
    fileID = gfs.put(contents, 
                     filename=file.filename, 
                     metadata={'room_code': room_code})
        # Update the fileList of the room
    rooms_collection.update_one(
        {'room_code': room_code},
        {'$push': {'fileList': {
            'fileID': fileID,
            'filename': file.filename
        }}}
    )
    print(f'Uploaded file [{file.filename}] with fileID [{fileID}] to room [{room_code}].')
    return fileID
