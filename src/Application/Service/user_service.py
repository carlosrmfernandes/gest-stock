from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db
from twilio.rest import Client 
from dotenv import load_dotenv
from flask import jsonify, make_response
import random
import os

class UserService:
    # ======== MÉTODO REUTILIZÁVEL PARA ENVIAR WHATSAPP ========
    @staticmethod
    def _enviar_whatsapp(celular, mensagem):
        try:
            account_sid = os.getenv("TWILIO_ACCOUNT_SID")
            auth_token = os.getenv("TWILIO_AUTH_TOKEN")
            twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                from_=twilio_number, 
                body=mensagem,
                to=f'whatsapp:{celular}'
            )
            print(f"Mensagem enviada via WhatsApp! SID: {message.sid}")
            return True
        except Exception as e:
            print(f"Erro ao enviar WhatsApp: {e}")
            return False

    # ======== MÉTODO PARA CRIAR USUÁRIO ========
    @staticmethod
    def create_user(name, cnpj, email, celular, password, status="Inativo"):        
        user = User(
            name=name,
            cnpj=cnpj,
            email=email,
            celular=celular,
            password=password,
            status=status
        )
        db.session.add(user)

        codigo = str(random.randint(1000, 9999))
        user.codigo_ativacao = codigo
        print(f"CÓDIGO GERADO PARA O WHATSAPP: {codigo}")
        db.session.commit()

        # Usando a função reutilizável
        mensagem = f'Olá {name}! Seu código de ativação do Mini Mercado é: {codigo}'
        UserService._enviar_whatsapp(celular, mensagem)

        return UserDomain(user.id, user.name, user.cnpj, user.email, user.celular, user.password)
    
    # ======== MÉTODOS PARA ATIVAÇÃO ========
    @staticmethod
    def verify_code(email, code_received):
        user = User.query.filter_by(email=email).first()
        
        if user and user.codigo_ativacao == code_received:
            user.status = "Ativo"
            user.codigo_ativacao = None
            db.session.commit()
            return user
        return None
    
    # ======== MÉTODO PARA LISTAR USUÁRIOS ========
    @staticmethod
    def get_all():
        users = User.query.all()
        
        lista_usuarios = []
        for u in users:
            lista_usuarios.append({
                "id": u.id,
                "name": u.name,
                "cnpj": u.cnpj,
                "email": u.email,
                "celular": u.celular,
                "status": u.status,
                "codigo_ativacao": u.codigo_ativacao
            })
        return lista_usuarios
    
    # ======== MÉTODO PARA ATUALIZAR USUÁRIO ========
    @staticmethod
    def update_user(user_id, new_email=None, new_celular=None, new_password=None):
        user = User.query.get(user_id)
        if not user:
            return None

        if new_email:
            user.email = new_email
        if new_password:
            user.password = new_password

        if new_celular and new_celular != user.celular:
            user.celular = new_celular
            user.status = "Inativo"
            
            codigo = str(random.randint(1000, 9999))
            user.codigo_ativacao = codigo
            print(f"NOVO CÓDIGO GERADO PARA O WHATSAPP: {codigo}")
            
            mensagem = f'Olá {user.name}! Seu número foi atualizado. Seu NOVO código do Mini Mercado é: {codigo}'
            UserService._enviar_whatsapp(user.celular, mensagem)

        db.session.commit()
        return user

    # ======== MÉTODOS PARA REDEFINIÇÃO DE SENHA ========
    @staticmethod
    def solicitar_redefinir_senha(email):
        user = User.query.filter_by(email=email).first()
        if not user:
            return make_response(jsonify({"erro": "Nenhum usuário encontrado com este e-mail."}), 404)

        # Gera código de 4 dígitos para manter seu padrão
        codigo = str(random.randint(1000, 9999))
        user.codigo_ativacao = codigo
        db.session.commit()

        mensagem = f"Olá {user.name}! Seu código para recuperar a senha do Mini Mercado é: {codigo}"
        enviado = UserService._enviar_whatsapp(user.celular, mensagem)
        
        if enviado:
            return make_response(jsonify({"mensagem": "Código de recuperação enviado ao seu WhatsApp!"}), 200)
        else:
            return make_response(jsonify({"erro": "Erro ao tentar enviar o código via WhatsApp."}), 500)

    @staticmethod
    def confirmar_redefinir_senha(email, codigo, nova_senha):
        user = User.query.filter_by(email=email).first()
        if not user:
            return make_response(jsonify({"erro": "Usuário não encontrado."}), 404)

        if user.codigo_ativacao != codigo:
            return make_response(jsonify({"erro": "Código de verificação inválido ou expirado."}), 400)

        user.password = nova_senha
        user.codigo_ativacao = None
        db.session.commit()

        return make_response(jsonify({"mensagem": "Senha alterada com sucesso!"}), 200)