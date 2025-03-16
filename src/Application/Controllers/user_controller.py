from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService

class UserController:
    @staticmethod
    def register_user():
        try:
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')

            if not name or not email or not password:
                return make_response(jsonify({"erro": "Missing required fields"}), 400)

            user = UserService.create_user(name=name, email=email, password=password)

            return make_response(jsonify({
                "mensagem": "Usuário salvo com sucesso",
                "usuario": user.to_dict()
            }), 201)

        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 409)

        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)
