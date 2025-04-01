import os
from datetime import timedelta 

class Config:
    HOST = '0.0.0.0'
    PORT = 8000
    DEBUG = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, '../run.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")  #sei la mas precisa
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1000)  # Token expira em 1000 hora
