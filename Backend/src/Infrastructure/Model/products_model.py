from src.config.data_base import db
from flask import jsonify, request


class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.Boolean, nullable=False, default=True)
    imagem = db.Column(db.String(255), nullable=True)
    user = db.Column(db.Integer, nullable=False)  

    def __init__(self, name, price, quantity, status=True, imagem=None, user=None):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.status = status
        self.imagem = imagem
        self.user = user

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "status": self.status,
            "imagem": self.imagem,
            "user": self.user
        }

def get_products():
    all_products = Products.query.all()
    return jsonify([product.to_dict() for product in all_products])

def update_products(products_id):
    product = Products.query.get(products_id)
    if not product:
        return jsonify({"erro": "Produto não encontrado"}), 404

    data = request.get_json()
    product.name = data.get("name", product.name)
    product.price = data.get("price", product.price)
    product.quantity = data.get("quantity", product.quantity)
    product.status = data.get("status", product.status)
    product.imagem = data.get("imagem", product.imagem)
    
    db.session.commit()
    return jsonify({"mensagem": "Produto atualizado com sucesso!"}), 200

def get_details_products(products_id):
    product = Products.query.get(products_id)
    if not product:
        return jsonify({"erro": "Produto não encontrado"}), 404
    return jsonify(product.to_dict()), 200
