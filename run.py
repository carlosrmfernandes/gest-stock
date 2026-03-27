import os

from flask import Flask
from src.config.data_base import init_db
from src.routes import init_routes
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["TWILIO_ACCOUNT_SID"] = os.getenv("TWILIO_ACCOUNT_SID")
    app.config["TWILIO_AUTH_TOKEN"] = os.getenv("TWILIO_AUTH_TOKEN")
    app.config["TWILIO_WHATSAPP_NUMBER"] = os.getenv("TWILIO_WHATSAPP_NUMBER")

    required_vars = [
        "SECRET_KEY",
        "TWILIO_ACCOUNT_SID",
        "TWILIO_AUTH_TOKEN",
        "TWILIO_WHATSAPP_NUMBER",
    ]
    
    missing_vars = [var for var in required_vars if not app.config.get(var)]
    if missing_vars:
        raise RuntimeError(f"Missing environment variables: {', '.join(missing_vars)}")

    JWTManager(app)

    init_db(app)
    init_routes(app)
    return app

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)