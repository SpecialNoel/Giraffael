# session_id_generator.py

import secrets

def generate_session_id(nbytes=32):
    return secrets.token_urlsafe(nbytes)
