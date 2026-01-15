# definitions.py

from datetime import datetime
from pydantic import BaseModel
from typing import Literal
    
class EncryptedMsg(BaseModel):
    typeOfMsg: str
    senderID: str
    cipherText: str
    nonce: str
    
class Message(BaseModel):
    type: Literal['chat', 'file']
    room_code: str
    sender: str
    payload: dict
    timestamp: datetime
    