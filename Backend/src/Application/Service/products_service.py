from src.Infrastructure.Model.products_model import Products
from src.config.data_base import db
from src.Infrastructure.Model.user_model import User

class ProductsService:
    @staticmethod
    def create_products(name, price, quantity, imagem, user):

        if isinstance(user, int):
            user = User.query.get(user)
            if not user:
                raise ValueError("Usuário não encontrado.")

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
