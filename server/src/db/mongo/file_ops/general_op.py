# general_op.py

from bson.errors import InvalidId
from src.db.mongo.mongodb_initiator import rooms_collection, gfs

'''
  File structure:      (file_content, filename, metadata: {'room_code'})
  File List structure: {{fileID, filename}, ...}
  # Note1: fileID for operations in backend; filename for better user experience. 
  # Note2: filename is unique per room. fileID is unique globally.
'''

# Get the file in a room by filename
def get_file_by_filename_and_room_code(filename, room_code):
    file = None
    try:
        file = gfs.find_one({
            'filename': filename,
            'metadata.room_code': room_code
        })
    except InvalidId:
        print(f'Error in get_file_by_filename_and_room_code(). Room code [{room_code}] is invalid.')
    return file

# Check if the target file is stored in a room by filename
def check_file_existence_in_room(filename, room_code):
    return get_file_by_filename_and_room_code(filename, room_code) is not None

# Get the corresponding fileID with given filename in a room
def get_fileID_by_filename_and_room_code(filename, room_code):
    file = get_file_by_filename_and_room_code(filename, room_code)
    if file is None:
        print('Error in get_fileID_by_filename_and_room_code(). '
              f'File with filename [{filename}] cannot be found in room [{room_code}].')
        return ''
    return file._id
    