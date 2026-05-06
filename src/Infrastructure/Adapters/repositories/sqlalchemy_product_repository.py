from src.Application.Ports.product_repository_port import ProductRepositoryPort
from src.Domain.product import ProductDomain
from src.Infrastructure.Model.produto import Product
from src.config.data_base import and_, db


class SqlAlchemyProductRepository(ProductRepositoryPort):
    @staticmethod
    def _to_domain(product):
        return ProductDomain(
            id=product.id,
            nome=product.nome,
            preco=product.preco,
            qtd=product.qtd,
            status=product.status,
            image=product.imagem,
            user=product.user
        )

    def save(self, product_domain):
        product = Product(
            nome=product_domain.nome,
            preco=product_domain.preco,
            qtd=product_domain.qtd,
            status=product_domain.status,
            imagem=product_domain.image,
            user=product_domain.user
        )
        
        db.session.add(product)
        db.session.commit()
        return self._to_domain(product)

    def list_all(self, user):
        return [self._to_domain(product) for product in Product.query.filter(Product.user == user).all()]

    def busca_por_nome(self, nome, user):
        product = db.session.query(Product).where(
            and_(
                Product.nome == nome,
                Product.user == user
            )
        ).first()
        return self._to_domain(product) if product else None

    def ativa_product(self, nome, user):
        product = db.session.query(Product).where(
            and_(
                Product.nome == nome,
                Product.user == user
            )
        ).first()

        if product:
            product.status = True
            db.session.add(product)
            db.session.commit()
            return True
        return False
    
    def desativar_product(self, nome, user):
        product = db.session.query(Product).where(
            and_(
                Product.nome == nome,
                Product.user == user
            )
        ).first()

        if product:
            product.status = False
            db.session.add(product)
            db.session.commit()
            return True
        return False
    
    def update(self, product_domain, novo_nome):
        product = db.session.query(Product).where(
            and_(
                Product.nome == product_domain.nome,
                Product.user == product_domain.user
            )
        ).first()

        if product:
            product.nome = novo_nome
            product.preco = product_domain.preco
            product.qtd = product_domain.qtd
            product.status = product_domain.status
            product.imagem = product_domain.image

            db.session.add(product)
            db.session.commit()
            return True
        return False
