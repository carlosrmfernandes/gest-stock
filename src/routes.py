from src.Application.Controllers.user_controller import UserController
from flask import jsonify, make_response


def init_routes(app):    
    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({ #def do prof só para mostrar que a api está funcionando
            "mensagem": "API - OK",
        }), 200)
    
    @app.route('/user', methods=['POST'])
    def register_user():
        return UserController.register_user()
    
    @app.route('/users',methods=['GET'])
    def get_users():
        return UserController.get_users()
    
    
    @app.route("/users/<int:user_id>", methods=["DELETE"])
    def delete_user(user_id):
        return UserController.delete_user(user_id)
    
