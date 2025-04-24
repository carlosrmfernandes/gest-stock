from src.Application.Controllers.products_controller import ProductsController
from flask import jsonify, make_response

def init_routes(app):    
    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({ 
            "mensagem": "API - OK",
        }), 200)
    
    @app.route('/new_products', methods=['POST'])
    def register_products():
        return ProductsController.register_products()
    
    @app.route('/list_products', methods=['GET'])
    def get_products():
        return ProductsController.get_users()
    
    @app.route('/active_products', methods=['POST'])
    def active_products():
        return ProductsController.active_products()
    
    @app.route("/update_products/<string:products_name>", methods=["PUT"])
    def update_products(products_name):
        return ProductsController.update_user(products_name)
    
    @app.route("/details_products/<string:products_name>", methods=["GET"])
    def get_details_products(products_name):
        return ProductsController.details_user(products_name)
    