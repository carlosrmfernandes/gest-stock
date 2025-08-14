from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def init_db(app):
    with app.app_context():
        if not os.path.exists(app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")):
            db.create_all()
            print("Banco de dados criado com sucesso! ✅")
        else:
            print("Banco de dados já existe! ✅")

