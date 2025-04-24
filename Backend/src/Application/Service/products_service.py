from src.Infrastructure.Model.products_model import Products
from src.config.data_base import db 

class ProductsService:
    @staticmethod
    def create_products(name, price, quantity, status=False, imagem=None):

        existing_user = Products.query.filter_by(name=name).first()
        if existing_user:
            raise ValueError("Este produto já está cadastrado.")

        products = Products(  
            name=name,
            price=price,
            quantity=quantity,
            status=status,
            imagem=imagem
        )

        db.session.add(products)
        db.session.commit()
        return products
