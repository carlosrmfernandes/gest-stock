from Backend.src.Application.Controllers.user_controller import UserController
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity

def init_routes(app):    
    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({ 
            "mensagem": "API - OK",
        }), 200)
    
    @app.route('/new_user', methods=['POST'])
    def register_user():
        return UserController.register_user()
    
    @app.route('/list_users', methods=['GET'])
    @jwt_required()  
    def get_users():
        return UserController.get_users()
    
    @app.route('/active_user', methods=['POST'])
    def active_user():
        return UserController.active_user()
    
    @app.route("/delete_user/<int:user_id>", methods=["DELETE"])
    @jwt_required()  
    def delete_user(user_id):
        return UserController.delete_user(user_id)
    
    @app.route("/update_user/<int:user_id>", methods=["PUT"])
    @jwt_required()  
    def update_user(user_id):
        return UserController.update_user(user_id)
    
    @app.route('/login', methods=['POST'])
    def login():
        return UserController.login_user()
    
    @app.route('/protected', methods=['GET'])
    @jwt_required()
    def protected():
        return make_response(jsonify({
            "mensagem": "Esta é uma rota protegida!",
            "usuario_logado": get_jwt_identity()
        }), 200)