from datetime import datetime
from src.config.data_base import db

class SoldProduct(db.Model):
    __tablename__ = "sold_products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Vendedor
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Comprador
    quantity = db.Column(db.Integer, nullable=False)
    price_at_sale = db.Column(db.Integer, nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Products', backref=db.backref('sold_entries', lazy=True))
    seller = db.relationship('User', foreign_keys=[user_id])
    buyer = db.relationship('User', foreign_keys=[buyer_id])

    def __init__(self, product_id, user_id, buyer_id, quantity, price_at_sale):
        self.product_id = product_id
        self.user_id = user_id
        self.buyer_id = buyer_id
        self.quantity = quantity
        self.price_at_sale = price_at_sale

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "seller_id": self.user_id,
            "buyer_id": self.buyer_id,
            "quantity": self.quantity,
            "price_at_sale": self.price_at_sale,
            "sale_date": self.sale_date.isoformat(),
        }
