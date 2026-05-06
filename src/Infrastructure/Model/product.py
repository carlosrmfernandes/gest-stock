from src.config.data_base import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade_estoque = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, default=True) # Ativo/Inativo
    imagem_url = db.Column(db.String(255))
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Sale(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_no_momento = db.Column(db.Float, nullable=False)
    data_venda = db.Column(db.DateTime, default=datetime.utcnow)