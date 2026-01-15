# file_routes.py

from fastapi import APIRouter, UploadFile, File
from src.services.file_service import upload_file_service, download_file_service

router = APIRouter()

# FastAPI endpoint for handling a 'upload' request from a client
@router.post('/upload/{room_code}')
def upload_file(room_code: str, file: UploadFile = File(...)):
    return upload_file_service(room_code, file)

# FastAPI endpoint for handling a 'download' request from a client
@router.get('/download/{room_code}/{filename}')
def download_file(room_code: str, filename: str):
    return download_file_service(room_code, filename)
