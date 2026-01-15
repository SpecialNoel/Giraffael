# encryption.py

# Every thing here is bytes, not strings.

import base64
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Encrypt a plain text with AESGCM
# nonce: a 12 bytes random nonce; add: user uuid in bytes
def encrypt(key: bytes, plain_text: bytes, add: bytes) -> dict:
    if len(key) not in (16, 24, 32):
        raise ValueError('Invalid AES key length')
    
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    cipher_text = aesgcm.encrypt(nonce, plain_text, add)
    encrypted_text = {'cipher_text': cipher_text, 'nonce': nonce}
    return encrypted_text

# Decrypt a cipher text with AESGCM and the same nonce and add used for the encryption
def decrypt(key: bytes, cipher_text: bytes, nonce: bytes, add: bytes) -> bytes:
    aesgcm = AESGCM(key)
    plain_text = aesgcm.decrypt(nonce, cipher_text, add)
    return plain_text

# Encode both cipher text and nonce with base 64 for transportation purpose
def encode_encrypted_text_with_b64(encrypted_text: dict) -> dict:
    encoded_cipher_text = base64.b64encode(encrypted_text['cipher_text'])
    encoded_nonce = base64.b64encode(encrypted_text['nonce'])
    return {'encoded_cipher_text': encoded_cipher_text, 'encoded_nonce': encoded_nonce}

# Decode both cipher text and nonce with base 64 for transportation purpose
def decode_encrypted_text_with_b64(encoded_encrypted_text: dict) -> dict:
    decoded_cipher_text = base64.b64decode(encoded_encrypted_text['encoded_cipher_text'])
    decoded_nonce = base64.b64decode(encoded_encrypted_text['encoded_nonce'])
    return {'cipher_text': decoded_cipher_text, 'nonce': decoded_nonce}
    
# Convert plain text into base64-encoded encrypted text
def get_b64_encoded_cipher_text_and_nonce(key: bytes, plain_text: bytes, add: bytes) -> dict:
    encrypted_text = encrypt(key, plain_text, add)
    b64_encoded_encrypted_text = encode_encrypted_text_with_b64(encrypted_text)
    encoded_cipher_text = b64_encoded_encrypted_text['encoded_cipher_text']
    encoded_nonce = b64_encoded_encrypted_text['encoded_nonce']
    return encoded_cipher_text, encoded_nonce

# Convert a base64-encoded encrypted text into plain text
def get_plain_text_from_b64_encoded_message(key: bytes, encoded_cipher_text: bytes, encoded_nonce: bytes, add: bytes) -> bytes:
    cipherText = base64.b64decode(encoded_cipher_text)
    nonce = base64.b64decode(encoded_nonce)
    plainText = decrypt(key, cipherText, nonce, add)
    return plainText
