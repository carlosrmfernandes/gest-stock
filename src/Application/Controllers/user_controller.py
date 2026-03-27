from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService

class UserController:
    @staticmethod
    def register_user():
        data = request.get_json()
        name = data.get('name')
        cnpj = data.get('cnpj')
        email = data.get('email')
        celular = data.get('celular')
        password = data.get('password')

        if not name or not email or not password or not cnpj:
            return make_response(jsonify({"erro": "Missing required fields"}), 400)

        user = UserService.create_user(name, email, cnpj, celular, password)

        return make_response(jsonify({
            "mensagem": "Seller cadastrado. Código enviado no WhatsApp",
            "usuarios": user.to_dict()
        }), 201)

    @staticmethod
    def activate_user():
        data = request.get_json()
        email = data.get("email")
        code = data.get("code")

        if not email or not code:
            return make_response(jsonify({"erro": "Dados inválidos"}), 400)

        activated = UserService.activate_user(email, code)

        if not activated:
            return make_response(jsonify({"erro": "Código inválido"}), 400)

        return make_response(jsonify({
            "mensagem": "Conta ativada com sucesso"
        }), 200)

    @staticmethod
    def login_user():
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return make_response(jsonify({"erro": "Dados inválidos"}), 400)

        token, error = UserService.login(email, password)

        if error:
            return make_response(jsonify({"erro": error}), 401)

        return make_response(jsonify({
            "mensagem": "Login realizado",
            "token": token
        }), 200)
    
    @staticmethod
    def update_user(user_id):
        data = request.get_json()

        user = UserService.update_user(user_id, data)

        if user:
            return make_response(jsonify({
            "mensagem": "Atualização realizada com sucesso!",
            "usuarios": user.to_dict()
            }), 200)
        else:
           return make_response(jsonify({"erro": "Usuário não encontrado"}), 404)
        