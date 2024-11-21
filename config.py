import os
from pathlib import Path as PathlibPath

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
    UPLOAD_FOLDER = './uploads'
    DOWNLOAD_FOLDER = './downloads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Max file size of 16MB
    DOWNLOAD_NAME = 'processed_data.csv'
    COLUMN_ALIASES = {
    "Timestamp": ["Period", "Timestamp", "Date", "Datetime", "Time"],
    "Consumption": ["Förbrukning", "Consumption", "Value", "Usage", "Amount"]
    }

class DirectoryPath:
    BASE_DIR = PathlibPath(__file__).resolve().parent
    WEATHER_DIRECTORY = os.path.join(BASE_DIR, 'weatherData')
    DOWNLOAD_FOLDER = os.path.join(BASE_DIR,'downloads')
    UPLOAD_FOLDER = os.path.join(BASE_DIR,'uploads')
    PLOTS_FOLDER = os.path.join(BASE_DIR,'app','static','plots')

