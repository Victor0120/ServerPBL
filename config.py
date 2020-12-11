import os

class Config:
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'beep-boop')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///beepboop.db')

    CHATBOT_EMAIL = 'beepboop.faf@gmail.com'
    TIME_AUTH_CODE_IS_VALID = 300 #code will be valid 5 min
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_HEADERS = 'Content-Type'