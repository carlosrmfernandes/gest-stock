from flask import Blueprint, jsonify, make_response
from src.Application.Controllers.products_controller import ProductsController
from flask_jwt_extended import jwt_required, get_jwt_identity
products_bp = Blueprint('products', __name__)

@products_bp.route('/new_product', methods=['POST'])
@jwt_required()
def register_products():
    return ProductsController.register_products(get_jwt_identity())

@products_bp.route('/list_products', methods=['GET'])
@jwt_required()
def get_products():
    return ProductsController.get_products() 

@products_bp.route('/list_user_products/<int:id>', methods=['GET'])
@jwt_required()
def get_user_products(id):
    return ProductsController.get_user_products(id) 

@products_bp.route('/update_products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_products(product_id):
    return ProductsController.update_products(product_id)

@products_bp.route('/toggle_product_status/<int:product_id>', methods=['PATCH'])
@jwt_required()
def toggle_product_status(product_id):
    return ProductsController.toggle_product_status(product_id)

@products_bp.route('/details_product/<int:id>', methods=['GET'])
@jwt_required()
def get_details_product(id):
    return ProductsController.get_details_product(id)

@products_bp.route('/buy_products/<int:id>', methods=['POST'])
@jwt_required()
def buy_product(id):
    user_id = get_jwt_identity()
    return ProductsController.buy_products(product_id=id, user_id=user_id)

