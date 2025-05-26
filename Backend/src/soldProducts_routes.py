from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.Application.Controllers.sold_product_controller import SoldProductController

sold_product_bp = Blueprint('sold_products', __name__)

@sold_product_bp.route('/new_sale', methods=['POST'])
@jwt_required()
def create_sale():
    user_id = get_jwt_identity()
    return SoldProductController.create_sale(user_id)

@sold_product_bp.route('/list_user_sales', methods=['GET'])
@jwt_required()
def list_user_sales():
    user_id = get_jwt_identity()
    return SoldProductController.list_user_sales(user_id)

@sold_product_bp.route('/list_user_purchases', methods=['GET'])
@jwt_required()
def list_user_purchases():
    user_id = get_jwt_identity()
    return SoldProductController.list_user_purchases(user_id)
