from flask import Flask
from src.config.data_base import init_db
from src.routes import init_routes
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "super-secret-key-da-nossa-app-jwt"
    jwt = JWTManager(app)

    init_db(app)
    init_routes(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
