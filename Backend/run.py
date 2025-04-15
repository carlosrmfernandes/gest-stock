from flask import Flask
from Backend.src.config.config import Config  
from Backend.src.config.data_base import db, init_db  
from Backend.src.routes import init_routes  
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
db.init_app(app)
init_routes(app)

if __name__ == "__main__":
    init_db(app)
    print(f"Servidor rodando em http://{Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
    