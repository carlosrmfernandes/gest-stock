from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.Infrastructure.http.whats_app import twilio_whatsapp_code
from src.config.data_base import db
import random
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

class UserService:
    @staticmethod
    def generate_activation_code():
        return str(random.randint(1000, 9999))

    @staticmethod
    def create_user(name, email, cnpj, celular, password):
        code = UserService.generate_activation_code()
        senha_hash = generate_password_hash(password)

        user = User(name=name, cnpj=cnpj, email=email, celular=celular, password=senha_hash, activation_code=code)
        db.session.add(user)
        db.session.commit()
        
        twilio_whatsapp_code(user.celular, code)

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

        if not check_password_hash(user.password, password):
            return None, "Senha inválida"

        if user.status == False:
            return None, "Conta não ativada"

        token = create_access_token(identity=str(user.id))
        return token, None
    
    @staticmethod
    def update_user(user_id, data):
        user = User.query.get(user_id)

        if not user:
            return False
        
        campos = ["name", "email", "cnpj", "celular", "password"]

        for campo in campos:
            if campo in data:
                setattr(user, campo, data[campo])
        
        if "password" in data:
            user.password = generate_password_hash(data["password"])
        
        db.session.commit()
       
        return UserDomain(user.id, user.name, user.email)
