from flask import Flask
from src.config.config import Config  
from src.config.data_base import db, init_db  
from src.user_routes import init_routes 
from flask_jwt_extended import JWTManager
from flask_cors import CORS


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'minha_chave_muito_segura_123456'
app.config.from_object(Config)
CORS(app)
jwt = JWTManager(app)
db.init_app(app)
init_routes(app)

if __name__ == "__main__":
    init_db(app)
    print(f"Servidor rodando em http://{Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
    