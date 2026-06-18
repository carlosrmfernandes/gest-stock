from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService
from flask_jwt_extended import create_access_token, get_jwt_identity
from src.Infrastructure.Model.user import User
from sqlalchemy.exc import IntegrityError
from src.config.data_base import db

class UserController:
    
    @staticmethod
    def register_user():
        data = request.get_json()
        name = data.get('name')
        cnpj = data.get('cnpj')
        email = data.get('email')
        celular = data.get('celular')
        password = data.get('password')

        if not name or not cnpj or not email or not celular or not password:
            return make_response(jsonify({"erro": "Parâmetro(s) obrigatório(s) não informado(s)"}), 400)

        try:
            user = UserService.create_user(name, cnpj, email, celular, password)
            return make_response(jsonify({
                "mensagem": "User salvo com sucesso e código enviado por WhatsApp.",
                "usuarios": user.to_dict()
            }), 201) 
        except IntegrityError:
            db.session.rollback()
            return make_response(jsonify({"erro": "Conflito de dados: E-mail, CNPJ ou Celular já cadastrados."}), 409)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"erro": f"Erro interno: {str(e)}"}), 500)

    @staticmethod
    def activate_account():
        data = request.get_json()
        email = data.get('email')
        code = data.get('codigo_ativacao')

        if not email or not code:
            return make_response(jsonify({"erro": "Email e código são obrigatórios"}), 400)

        user_activated = UserService.verify_code(email, code)

        if user_activated:
            access_token = create_access_token(identity=str(user_activated.id))
            return make_response(jsonify({
                "mensagem": "Conta ativada com sucesso!",
                "token": access_token
            }), 200)
        else:
            return make_response(jsonify({"erro": "Código inválido ou usuário não encontrado."}), 400)

    @staticmethod
    def login():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or user.password != password:
            return make_response(jsonify({"erro": "E-mail ou senha incorretos."}), 401)

        if user.status != "Ativo":
            return make_response(jsonify({"erro": "Conta inativa. Ative via código enviado ao seu WhatsApp."}), 403)

        access_token = create_access_token(identity=str(user.id))
        return make_response(jsonify({
            "mensagem": "Login realizado com sucesso",
            "token": access_token
        }), 200)

    @staticmethod
    def get_all_users():
        try:
            usuarios = UserService.get_all()
            return make_response(jsonify({
                "mensagem": "Usuários listados com sucesso",
                "quantidade": len(usuarios),
                "usuarios": usuarios
            }), 200)
        except Exception as e:
            return make_response(jsonify({"erro": f"Erro ao buscar usuários: {str(e)}"}), 500)
        
    @staticmethod
    def solicitar_redefinir_senha():
        data = request.get_json()
        email = data.get('email')

        if not email:
            return make_response(jsonify({"erro": "O e-mail é obrigatório."}), 400)
            
        return UserService.solicitar_redefinir_senha(email)

    @staticmethod
    def confirmar_redefinir_senha():
        data = request.get_json()
        email = data.get('email')
        codigo = data.get('codigo_verificacao')
        nova_senha = data.get('nova_senha')

        if not email or not codigo or not nova_senha:
            return make_response(jsonify({"erro": "Todos os campos são obrigatórios."}), 400)
            
        return UserService.confirmar_redefinir_senha(email, codigo, nova_senha)
    
    @staticmethod
    def obter_dados_vendedor():
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user:
                return make_response(jsonify({"erro": "Usuário não encontrado."}), 404)
                
            return make_response(jsonify({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "celular": user.celular,
                "cnpj": user.cnpj
            }), 200)
        except Exception as e:
            return make_response(jsonify({"erro": f"Erro interno: {str(e)}"}), 500)

    @staticmethod
    def update_user(user_id):
        user_logado_id = get_jwt_identity()
        if str(user_id) != str(user_logado_id):
            return make_response(jsonify({"erro": "Acesso negado para editar este perfil."}), 403)

        data = request.get_json()
        user = User.query.get(user_id)
        
        if not user:
            return make_response(jsonify({"erro": "Usuário não encontrado."}), 404)

        if 'name' in data: user.name = data['name']
        if 'email' in data: user.email = data['email']
        if 'celular' in data: user.celular = data['celular']
        if 'password' in data and data['password'].strip() != "":
            user.password = data['password'] 

        try:
            db.session.commit()
            return make_response(jsonify({"mensagem": "Perfil atualizado com sucesso!"}), 200)
        except IntegrityError:
            db.session.rollback()
            return make_response(jsonify({"erro": "E-mail ou Celular já estão em uso."}), 409)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"erro": f"Erro interno: {str(e)}"}), 500)