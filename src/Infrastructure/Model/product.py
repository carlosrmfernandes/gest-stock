from src.config.data_base import db
from src.Domain.product import ProductDomain, PRODUCT_ATIVO


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default=PRODUCT_ATIVO)
    img = db.Column(db.String(255), nullable=True)

    def to_domain(self):
        return ProductDomain(
            id=self.id,
            seller_id=self.seller_id,
            name=self.name,
            price=self.price,
            quantity=self.quantity,
            status=self.status,
            img=self.img,
        )
