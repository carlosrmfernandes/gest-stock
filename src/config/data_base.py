import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """
    Inicializa a base de dados com o app Flask e o SQLAlchemy.
    
    Opções de banco de dados:
    1. SQLite (padrão) - Não precisa de Docker, ideal para desenvolvimento
    2. MySQL - Precisa subir o Docker com docker-compose up
    """
    
    # ========== OPÇÃO 1: SQLite (Sem Docker) ==========
    # Banco de dados local, arquivo criado na pasta do projeto
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, '..', '..', 'market_management.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    
    # ========== OPÇÃO 2: MySQL (Com Docker) ==========
    # Descomente a linha abaixo e comente a linha do SQLite acima
    # Depois rode: docker-compose up
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@mysql57:3306/market_management'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    # Cria as tabelas automaticamente
    with app.app_context():
        db.create_all()

