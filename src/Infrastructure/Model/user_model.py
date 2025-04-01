from src.config.data_base import db
from flask import jsonify, request
from src.Infrastructure.http.whats_app import whats_app_api
from random import randint
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    code = db.Column(db.String(4), nullable=False)  
    is_active = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name, email, password, cnpj, phone, is_active=False):
        self.name = name
        self.email = email
        self.set_password(password)
        self.cnpj = cnpj
        self.phone = phone
        self.code = str(randint(1000, 9999))  
        self.is_active = is_active
        whats_app_api(self.phone, self.code)  
    
    def set_password(self, senha_plana):
        self.password = bcrypt.generate_password_hash(senha_plana).decode('utf-8')
        
    def check_password(self, senha_plana):
        return bcrypt.check_password_hash(self.password, senha_plana)

    def generate_auth_token(self):
        return create_access_token(identity=self.id)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "cnpj": self.cnpj,
            "phone": self.phone,
            "is_active": self.is_active
        }

def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    
    db.session.delete(user)
    db.session.commit()

    return jsonify({"mensagem": "Usuário deletado com sucesso!"}), 200

def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    data = request.get_json()
    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    
    if 'password' in data:
        user.set_password(data['password'])
        
    user.cnpj = data.get("cnpj", user.cnpj)
    user.phone = data.get("phone", user.phone)

    db.session.commit()

    return jsonify({"mensagem": "Usuário atualizado com sucesso!"}), 200