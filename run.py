from flask import Flask
from src.config.config import Config  
from src.config.data_base import db, init_db  
from src.routes import init_routes  

app = Flask(__name__)
app.config.from_object(Config)  

print("Banco de dados conectado em:", app.config["SQLALCHEMY_DATABASE_URI"])

init_routes(app)
db.init_app(app) 

if __name__ == "__main__":
    init_db(app) 
    print("Rotas registradas:")
    for rule in app.url_map.iter_rules():
        print(rule)

    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
