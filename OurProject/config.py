import os

class Config:
    # Veritabanı bağlantı URL'si
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:1234@localhost/kadinguvenlik'
    SQLALCHEMY_TRACK_MODIFICATIONS = False