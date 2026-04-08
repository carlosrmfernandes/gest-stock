import os

from flask import Flask

from src.config.data_base import init_db
from src.routes import init_routes


def create_app():
    """
    Funcao que cria e configura a aplicacao Flask.
    """
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-only-change-me")

    init_db(app)
    init_routes(app)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
