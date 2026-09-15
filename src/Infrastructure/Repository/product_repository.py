from src.config.data_base import db
from src.Infrastructure.Model.product import Product


class ProductRepository:
    """Isola o acesso ao banco para produtos. Deve ser mockado nos testes."""

    def save(self, product):
        db.session.add(product)
        db.session.commit()
        return product

    def find_by_id(self, product_id):
        return db.session.get(Product, product_id)

    def find_by_seller(self, seller_id):
        return Product.query.filter_by(seller_id=seller_id).all()

    def find_by_name_and_seller(self, name, seller_id):
        return Product.query.filter_by(name=name, seller_id=seller_id).first()
