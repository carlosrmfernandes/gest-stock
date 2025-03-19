import os

class Config:
    HOST = '0.0.0.0'
    PORT = 8000
    DEBUG = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, '../run.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
