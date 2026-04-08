from src.Domain.product import ProductDomain


class ProductUseCase:
    def __init__(self, product_repository):
        self.product_repository = product_repository


    def register_product(self, nome, preco, qtd, status, image, user):
        product = ProductDomain(
            id=None,
            nome=nome,
            preco=preco,
            qtd=qtd,
            status=status,
            image=image,
            user=user
        )

        saved_product = self.product_repository.save(product)
        return saved_product

    def list_products(self, user):
        return [product.to_dict() for product in self.product_repository.list_all(user)]

    def buscar_product_por_nome(self, nome, user):
        return self.product_repository.busca_por_nome(nome, user)

    def editar_product(self, nome, novo_nome, novo_preco, nova_qtd, novo_status, nova_image, user):
        product = self.product_repository.busca_por_nome(nome, user)
        if not product:
            return False

        product.preco = novo_preco
        product.qtd = nova_qtd
        product.status = novo_status
        product.image = nova_image

        self.product_repository.update(product, novo_nome)
        return True

    def ativa_product_via_nome(self, nome, user):
        return self.product_repository.ativa_product(nome, user)
    
    def desativar_product_via_nome(self, nome, user):
        return self.product_repository.desativar_product(nome, user)
