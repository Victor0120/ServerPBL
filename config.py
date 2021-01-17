import os

class Config:
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'beep-boop')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///beepboop.db')

    CHATBOT_EMAIL = 'beepboop.faf@gmail.com'
    TIME_AUTH_CODE_IS_VALID = 300 #code will be valid 5 min

    CHATBOT_ID = 0
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_HEADERS = 'Content-Type'
    UPLOAD_MATERIAL_FOLDER_PREFIX = 'static/courses/materials'

    BASE_URL = 'http://localhost:5000/'
    QA_API_BASE_URL = 'http://localhost:8000/'
