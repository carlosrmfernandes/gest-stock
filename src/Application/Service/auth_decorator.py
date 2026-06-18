from functools import wraps
from flask import jsonify, make_response
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from src.Infrastructure.Model.user import User

def seller_required():
    """
    Decorator que valida se o token JWT pertence a um Seller válido e Ativo.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user_id = get_jwt_identity()
                
                user = User.query.get(user_id)
                if not user:
                    return make_response(jsonify({"erro": "Acesso negado. Usuário não encontrado."}), 404)
                
                if user.status != "Ativo":
                    return make_response(jsonify({
                        "erro": "Acesso negado. Esta conta encontra-se inativa ou aguardando verificação por WhatsApp."
                    }), 403)
                    
                return f(*args, **kwargs)
            except Exception as e:
                return make_response(jsonify({"erro": "Token ausente ou inválido.", "detalhes": str(e)}), 401)
        return decorated_function
    return decorator