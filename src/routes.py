from src.Application.Controllers.user_controller import UserController
from src.Application.Controllers.product_controller import ProductController

from flask import jsonify, make_response

def init_routes(app):    
    @app.route('/', methods=['GET'])
    def index():
        return make_response(jsonify({
            "message": "Server is running",
        }), 200)

    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)
    
    @app.route('/user', methods=['POST'])
    def register_user():
        return UserController.register_user()
    
    @app.route('/testarNumero', methods=['GET'])
    def testar_numero():
        return UserController.testarNumero()

    @app.route('/users', methods=['GET'])
    def ver_usuarios():
        return UserController.verUsuarios()
    
    @app.route('/ativarUsuario', methods=["POST"])
    def ativar_usuario():
        return UserController.ativar_usuario()

    @app.route('/login', methods=['POST'])
    def login_user():
        return UserController.login_user()
    
    @app.route('/product', methods=['POST'])
    def register_product():
        return ProductController.register_product()

    @app.route('/products/<int:user_id>', methods=['GET'])
    def list_all_products(user_id=None):
        return ProductController.list_all_products(user_id)
    
    @app.route('/ativarProduto', methods=["POST"])
    def ativar_produto():
        return ProductController.ativar_product()
    
    @app.route('/desativarProduto', methods=["POST"])
    def desativar_produto():
        return ProductController.desativar_product()
    
    @app.route('/buscarProduto', methods=["POST"])
    def buscar_produto_por_nome():
        return ProductController.buscar_product_por_nome()
    
    @app.route('/editarProduto', methods=["POST"])
    def editar_produto():
        return ProductController.editar_product()
    
