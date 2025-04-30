from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService
from src.Infrastructure.Model.user_model import User
from src.config.data_base import db 
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

class UserController:
    @staticmethod
    def register_user():
        try:
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            cnpj = data.get('cnpj')
            phone = data.get('phone')
            is_active = data.get('is_active')

            if not name or not email or not password:
                return make_response(jsonify({"erro": "Preencha todos os campos!"}), 400)

            user = UserService.create_user(name=name, email=email, password=password, cnpj=cnpj, phone=phone)

            return make_response(jsonify({
                "mensagem": "Usuário salvo com sucesso!",
                "usuario": user.to_dict()
            }), 201)

        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 409)

        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)
        
    @staticmethod
    @jwt_required()
    def get_users():
        try:
            current_user = get_jwt_identity()  
            users = User.query.all()
            return make_response(jsonify([user.to_dict() for user in users]), 200)

        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    @jwt_required()
    def delete_user(user_id):
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user:
                return make_response(jsonify({"erro": "Usuário não encontrado"}), 404)
            
            if str(user.id) != current_user_id:
                return make_response(jsonify({"erro": "Não autorizado"}), 403)

            db.session.delete(user)
            db.session.commit()

            return make_response(jsonify({"mensagem": "Usuário deletado com sucesso!"}), 200)

        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    @jwt_required()
    def update_user(user_id):
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user:
                return make_response(jsonify({"erro": "Usuário não encontrado"}), 404)
            
            if str(user.id) != current_user_id:
                return make_response(jsonify({"erro": "Não autorizado"}), 403)

            data = request.get_json()
            user.name = data.get("name", user.name)
            user.email = data.get("email", user.email)
            
            if 'password' in data:
                user.password = data['password']

            db.session.commit()

            return make_response(jsonify({"mensagem": "Usuário atualizado com sucesso!"}), 200)

        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def active_user():
        data = request.get_json()
        email = data.get('email')
        code = data.get('code')
        print(email)
        user = User.query.filter_by(email=email).first()

        if user and user.is_active == False and code == user.code:
            user.is_active = True
            db.session.commit()
            return make_response(jsonify({"mensagem": "Usuário ativado com sucesso!"}), 200)
        
        elif user.is_active == True:
            return make_response(jsonify({"ERRO": "ja atualizo porra"}), 666)
    
    @staticmethod
    def login_user():
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            print(data)
            user = User.query.filter_by(email=email).first()
            print(user)
            
            if not user:
                return make_response(jsonify({"erro": "Usuário não encontrado!"}), 404)
            
            if not user.is_active:
                return make_response(jsonify({"erro": "Usuário não está ativo!"}), 403)

            if not user.check_password(password):
                return make_response(jsonify({"erro": "Senha incorreta!"}), 401)

            access_token = create_access_token(identity=str(user.id))
            
            return make_response(jsonify({
                "mensagem": "Login realizado com sucesso!",
                "usuario": user.to_dict(),
                "access_token": access_token
            }), 200)

        except Exception as e:
            print(str(e))
            return make_response(jsonify({"erro": str(e)}), 500)
