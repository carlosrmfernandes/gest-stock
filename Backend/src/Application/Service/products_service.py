from src.Infrastructure.Model.products_model import Products
from src.config.data_base import db

class ProductsService:
    @staticmethod
    def create_products(name, price, quantity, imagem, user):
        existing_product = Products.query.filter_by(name=name).first()
        if existing_product:
            raise ValueError("Este produto já está cadastrado.")

        product = Products(
            name=name,
            price=price,
            quantity=quantity,
            imagem=imagem,
            user=user
        )

        db.session.add(product)
        db.session.commit()
        return product
