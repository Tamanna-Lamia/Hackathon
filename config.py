import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
    UPLOAD_FOLDER = './uploads'
    DOWNLOAD_FOLDER = './downloads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Max file size of 16MB
