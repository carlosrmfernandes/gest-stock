from src.Application.Controllers.user_controller import UserController
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

def init_routes(app):
    @app.route('/user', methods=['POST'])
    def register_user():
        return UserController.register_user()

    @app.route("/activate", methods=["POST"])
    def activate_user():
        return UserController.activate_user()

    @app.route("/login", methods=["POST"])
    def login_user():
        return UserController.login_user()

    @app.route("/teste", methods=["GET"])
    @jwt_required()
    def teste():
        user_id = int(get_jwt_identity())
        return jsonify({
            "mensagem": "Acesso autorizado",
            "user_id": user_id
        })