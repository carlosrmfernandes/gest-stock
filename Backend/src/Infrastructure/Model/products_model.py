from src.config.data_base import db
from flask import jsonify, request

class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer(8), nullable=False)
    quantity = db.Column(db.Integer(3), nullable=False, default=0)
    status = db.Column(db.Boolean, nullable=False, default=False)
    imagem = db.Column(db.String(255), nullable=True)

    def __init__(self, name, price, quantity, status=False, imagem=None):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.status = status
        self.imagem = None

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "status": self.status,
            "imagem": self.imagem
        }

def get_products():
    products = Products.query.all()
    return jsonify([products.name for products in products])

def update_products(products_id):
    products = Products.query.get(products_id)
    if not products:
        return jsonify({"erro": "Produto não encontrado"}), 404

    data = request.get_json()
    products.name = data.get("name", products.name)
    products.price = data.get("price", products.price)
    products.quantity = data.get("quantity", products.quantity)
    products.status = data.get("status", products.status)
    products.imagem = data.get("imagem", products.imagem)
    
    db.session.commit()

    return jsonify({"mensagem": "Produto atualizado com sucesso!"}), 200

def get_details_products(products_id):
    products = Products.query.all(products_id)
    return jsonify([products.to_dict() for products in products])
