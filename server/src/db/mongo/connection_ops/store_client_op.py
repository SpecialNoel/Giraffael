# store_client_op.py

from src.db.mongo.mongodb_initiator import users_collection

# Store the client in MongoDB
def store_client_in_db(client_email, client_hashed_password, client_uuid, session_id):
    client_info = {'email': client_email, 
                   'password': client_hashed_password,
                   'user_id': client_uuid,
                   'session_id': session_id}
    
    try:
        users_collection.insert_one(
            client_info
        )
    except Exception as e:
        print(f'Error in store_client_in_db(): {e}.')
        return False
    return True
