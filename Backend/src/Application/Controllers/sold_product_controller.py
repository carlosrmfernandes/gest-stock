from flask import request, jsonify
from src.Infrastructure.Model.sold_products import SoldProduct  # ajusta o caminho conforme seu projeto
from src.config.data_base import db

class SoldProductController:

    @staticmethod
    def create_sale(user_id):
        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        price_at_sale = data.get('price_at_sale')

        if not all([product_id, quantity, price_at_sale]):
            return jsonify({"error": "Campos product_id, quantity e price_at_sale são obrigatórios"}), 400

        sale = SoldProduct(product_id=product_id, user_id=user_id, quantity=quantity, price_at_sale=price_at_sale)
        db.session.add(sale)
        db.session.commit()

        return jsonify({"message": "Venda criada com sucesso", "sale": sale.to_dict()}), 201

    @staticmethod
    def list_user_sales(user_id):
        try:
            sales = SoldProduct.query.filter_by(user_id=user_id).all()
            return jsonify([sale.to_dict() for sale in sales]), 200
        except Exception as e:
            return jsonify({"erro": str(e)}), 500

    @staticmethod
    def list_user_purchases(user_id):
        try:
            purchases = SoldProduct.query.filter_by(buyer_id=user_id).all()
            return jsonify([purchase.to_dict() for purchase in purchases]), 200
        except Exception as e:
            return jsonify({"erro": str(e)}), 500
