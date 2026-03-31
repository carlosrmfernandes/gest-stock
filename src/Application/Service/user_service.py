from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.Infrastructure.http.whats_app import twilio_whatsapp_code
from src.config.data_base import db
import random
from flask_jwt_extended import create_access_token

class UserService:
    @staticmethod
    def generate_activation_code():
        return str(random.randint(1000, 9999))

    @staticmethod
    def create_user(name, email, cnpj, cell, password):
        code = UserService.generate_activation_code()

        user = User(name=name, cnpj=cnpj, email=email, cell=cell, password=password, activation_code=code)
        db.session.add(user)
        db.session.commit()
        twilio_whatsapp_code(user.cell, code)
        return UserDomain(user.id, user.name, user.email)

    @staticmethod
    def activate_user(email, code):
        user = User.query.filter_by(email=email).first()

        if not user:
            return False

        if user.activation_code != code:
            return False

        user.status = True
        user.activation_code = None
        db.session.commit()
        return True

    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email).first()

        if not user:
            return None, "Usuário não encontrado"

        if user.password != password:
            return None, "Senha inválida"

        if user.status == False:
            return {"msg": "Conta não ativada"}, 403

        token = create_access_token(identity=str(user.id))
        return token,

