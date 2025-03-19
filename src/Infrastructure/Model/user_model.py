from src.config.data_base import db
from flask import jsonify, request

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    def __init__(self, name, email, password, cnpj, phone):
        self.name = name
        self.email = email
        self.password = password
        self.cnpj = cnpj
        self.phone = phone

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "cnpj": self.cnpj,
            "phone": self.phone
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

    return jsonify({"mensagem": "Usuáro deletado com sucesso!"}), 200


def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    data = request.get_json()
    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    user.password = data.get("password", user.password)
    user.cnpj = data.get("cnpj", user.cnpj)
    user.phone = data.get("phone", user.phone)

    db.session.commit()

    return jsonify({"mensagem": "Usuário atualizado com sucesso!"}), 200
