from src.Domain.exceptions import (
    BusinessRuleError,
    ConflictError,
    NotFoundError,
    ValidationError,
)
from src.Domain.product import PRODUCT_ATIVO, PRODUCT_INATIVO
from src.Domain.seller import STATUS_ATIVO
from src.Infrastructure.Model.product import Product
from src.Infrastructure.Repository.product_repository import ProductRepository
from src.Infrastructure.Repository.seller_repository import SellerRepository

MAX_NAME_LENGTH = 100


class ProductService:
    """
    Regras de negócio de produtos.
    Recebe os dois repositórios por injeção de dependência para permitir mocks.
    """

    def __init__(self, product_repository=None, seller_repository=None):
        self.product_repository = product_repository or ProductRepository()
        self.seller_repository = seller_repository or SellerRepository()

    def create_product(self, seller_id, name, price, quantity, status=PRODUCT_ATIVO, img=None):
        """
        Cadastra um produto para um seller.

        Regras:
          - seller precisa existir -> NotFoundError;
          - seller precisa estar Ativo -> BusinessRuleError;
          - nome obrigatório, com no máximo 100 caracteres;
          - preço deve ser numérico e maior que zero;
          - quantidade deve ser inteira e maior ou igual a zero;
          - status só pode ser 'Ativo' ou 'Inativo';
          - o mesmo seller não pode ter dois produtos com o mesmo nome -> ConflictError.
        """
        seller = self.seller_repository.find_by_id(seller_id)

        if seller is None:
            raise NotFoundError('Seller não encontrado')

        if seller.status != STATUS_ATIVO:
            raise BusinessRuleError('Seller inativo não pode cadastrar produtos')

        if not name or not str(name).strip():
            raise ValidationError('Nome do produto é obrigatório')

        clean_name = str(name).strip()

        if len(clean_name) > MAX_NAME_LENGTH:
            raise ValidationError(f'Nome do produto deve ter no máximo {MAX_NAME_LENGTH} caracteres')

        if not isinstance(price, (int, float)) or isinstance(price, bool):
            raise ValidationError('Preço deve ser numérico')

        if price <= 0:
            raise ValidationError('Preço deve ser maior que zero')

        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise ValidationError('Quantidade deve ser um número inteiro')

        if quantity < 0:
            raise ValidationError('Quantidade não pode ser negativa')

        if status not in (PRODUCT_ATIVO, PRODUCT_INATIVO):
            raise ValidationError("Status deve ser 'Ativo' ou 'Inativo'")

        if self.product_repository.find_by_name_and_seller(clean_name, seller_id):
            raise ConflictError('Este seller já possui um produto com esse nome')

        product = Product(
            seller_id=seller_id,
            name=clean_name,
            price=float(price),
            quantity=quantity,
            status=status,
            img=img,
        )

        self.product_repository.save(product)

        return product.to_domain()

    def list_products(self, seller_id):
        """Lista os produtos de um seller. Seller inexistente -> NotFoundError."""
        seller = self.seller_repository.find_by_id(seller_id)

        if seller is None:
            raise NotFoundError('Seller não encontrado')

        products = self.product_repository.find_by_seller(seller_id)
        return [product.to_domain() for product in products]
