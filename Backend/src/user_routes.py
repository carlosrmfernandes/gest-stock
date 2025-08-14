from flask import Blueprint, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.Application.Controllers.user_controller import UserController

user_bp = Blueprint('user', __name__)

@user_bp.route('/api', methods=['GET'])
def health():
    return make_response(jsonify({ 
        "mensagem": "API - OK",
    }), 200)

@user_bp.route('/new_user', methods=['POST'])
def register_user():
    return UserController.register_user()

@user_bp.route('/list_users', methods=['GET'])
@jwt_required()
def get_users():
    return UserController.get_users()

@user_bp.route('/active_user', methods=['POST'])
def active_user():
    return UserController.active_user()

@user_bp.route('/delete_user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    return UserController.delete_user(user_id)

@user_bp.route('/update_user/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    return UserController.update_user(user_id)

@user_bp.route('/login', methods=['POST'])
def login():
    return UserController.login_user()

@user_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return make_response(jsonify({
        "usuario_logado": get_jwt_identity()
    }), 200)
