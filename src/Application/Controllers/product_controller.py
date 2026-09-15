from flask import jsonify, make_response, request

from src.Application.Service.product_service import ProductService
from src.Domain.exceptions import DomainError
from src.Domain.product import PRODUCT_ATIVO


class ProductController:
    """Camada HTTP de produtos."""

    @staticmethod
    def register_product(service=None):
        service = service or ProductService()
        data = request.get_json(silent=True) or {}

        try:
            product = service.create_product(
                seller_id=data.get('seller_id'),
                name=data.get('name'),
                price=data.get('price'),
                quantity=data.get('quantity'),
                status=data.get('status', PRODUCT_ATIVO),
                img=data.get('img'),
            )
        except DomainError as error:
            return make_response(jsonify({"erro": error.message}), error.status_code)

        return make_response(jsonify({
            "mensagem": "Produto cadastrado com sucesso",
            "produto": product.to_dict(),
        }), 201)

    @staticmethod
    def list_products(seller_id, service=None):
        service = service or ProductService()

        try:
            products = service.list_products(seller_id)
        except DomainError as error:
            return make_response(jsonify({"erro": error.message}), error.status_code)

        return make_response(jsonify({
            "produtos": [product.to_dict() for product in products],
        }), 200)
