from flask import jsonify, make_response

from src.Application.Controllers.product_controller import ProductController
from src.Application.Controllers.seller_controller import SellerController
from src.Application.Controllers.user_controller import UserController


def init_routes(app):
    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)

    @app.route('/user', methods=['POST'])
    def register_user():
        return UserController.register_user()

    # ---------- Seller ----------
    @app.route('/api/sellers', methods=['POST'])
    def register_seller():
        return SellerController.register_seller()

    @app.route('/api/sellers/activate', methods=['POST'])
    def activate_seller():
        return SellerController.activate_seller()

    # ---------- Produtos ----------
    @app.route('/api/products', methods=['POST'])
    def register_product():
        return ProductController.register_product()

    @app.route('/api/sellers/<int:seller_id>/products', methods=['GET'])
    def list_products(seller_id):
        return ProductController.list_products(seller_id)
