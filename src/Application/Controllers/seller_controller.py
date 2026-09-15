from flask import jsonify, make_response, request

from src.Application.Service.seller_service import SellerService
from src.Domain.exceptions import DomainError


class SellerController:
    """Camada HTTP: traduz request/response e converte erros de domínio em status code."""

    @staticmethod
    def register_seller(service=None):
        service = service or SellerService()
        data = request.get_json(silent=True) or {}

        try:
            seller = service.create_seller(
                name=data.get('name'),
                cnpj=data.get('cnpj'),
                email=data.get('email'),
                phone=data.get('phone'),
                password=data.get('password'),
            )
        except DomainError as error:
            return make_response(jsonify({"erro": error.message}), error.status_code)

        return make_response(jsonify({
            "mensagem": "Seller cadastrado. Código de ativação enviado por WhatsApp.",
            "seller": seller.to_dict(),
        }), 201)

    @staticmethod
    def activate_seller(service=None):
        service = service or SellerService()
        data = request.get_json(silent=True) or {}

        try:
            seller = service.activate_seller(
                phone=data.get('phone'),
                code=data.get('code'),
            )
        except DomainError as error:
            return make_response(jsonify({"erro": error.message}), error.status_code)

        return make_response(jsonify({
            "mensagem": "Seller ativado com sucesso",
            "seller": seller.to_dict(),
        }), 200)
