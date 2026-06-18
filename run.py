import os
from flask import Flask
from src.config.data_base import init_db
from src.routes import init_routes
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    
    jwt = JWTManager(app)

    # Inicializa o banco de dados (Cria pastas e tabelas)
    init_db(app)

    # Configura mapeamento de rotas
    init_routes(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)