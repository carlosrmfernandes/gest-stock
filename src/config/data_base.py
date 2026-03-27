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
    
    # Prioriza a URI vinda do ambiente (Docker/local).
    database_uri = os.getenv('SQLALCHEMY_DATABASE_URI')

    if not database_uri:
        # Fallback local para desenvolvimento sem Docker.
        basedir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(basedir, '..', '..', 'market_management.db')
        database_uri = f'sqlite:///{db_path}'

    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    # Cria as tabelas automaticamente
    with app.app_context():
        # Garante o registro dos modelos antes da criação das tabelas.
        from src.Infrastructure.Model.user import User
        
        db.create_all()

