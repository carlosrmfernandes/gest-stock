from functools import wraps

from flask import current_app, jsonify, make_response, request

from src.Infrastructure.Adapters.repositories.sqlalchemy_product_repository import (
    SqlAlchemyProductRepository,
)

from src.Application.UseCases.product_use_case import ProductUseCase

def _build_product_use_case():
    return ProductUseCase(
        product_repository=SqlAlchemyProductRepository()
    )

class ProductController:
    @staticmethod
    def register_product():
        data = request.get_json() or {}

        nome = data.get("nome")
        preco = data.get("preco")
        qtd = data.get("qtd")
        status = data.get("status")
        image = data.get("image")
        user = data.get("user")

        if not nome or preco is None or qtd is None or status is None or not image or user is None:
            return make_response(jsonify({"erro": "Um campo nao foi preenchido."}), 400)

        if preco < 0:
            return make_response(jsonify("O preço não pode ser negativo"), 401)


        try:
            product = _build_product_use_case().register_product(
                nome=nome,
                preco=preco,
                qtd=qtd,
                status=status,
                image=image,
                user=user
            )
        except Exception as exc:
            return make_response(
                jsonify(
                    {
                        "erro": "Falha no cadastro.",
                        "detalhe": str(exc),
                    }
                ),
                502,
            )

        return make_response(
            jsonify(
                {
                    "mensagem": "Produto salvo com sucesso."
                }
            ),
            200,
        )
    
    @staticmethod
    def list_all_products(user_id=None):
        data = request.get_json(silent=True) or {}
        user = user_id or request.args.get("user") or data.get("user")

        if user is None:
            return make_response(jsonify({"erro": "Usuario nao informado."}), 400)

        try:
            user = int(user)
        except (TypeError, ValueError):
            return make_response(jsonify({"erro": "Usuario invalido."}), 400)
        
        try:
            products = _build_product_use_case().list_products(user)
        except Exception as exc:
            return make_response(
                jsonify(
                    {
                        "erro": "Falha ao listar produtos.",
                        "detalhe": str(exc),
                    }
                ),
                502,
            )

        return make_response(jsonify(products), 200)
    
    @staticmethod
    def buscar_product_por_nome():
        data = request.get_json() or {}

        nome = data.get("nome")
        user = data.get("user")

        if not nome or not user:
            return make_response(jsonify({"erro": "Um dos campos não foi preenchido."}), 400)

        product = _build_product_use_case().buscar_product_por_nome(nome, user)

        if product:
            return make_response(jsonify(product.to_dict()), 200)
        return make_response(jsonify({"erro": "Produto não encontrado."}), 404)


    @staticmethod
    def ativar_product():
        data = request.get_json() or {}

        nome = data.get("nome")
        user = data.get("user")

        if not nome or not user:
            return make_response(jsonify({"erro": "Um dos campos não foi preenchido."}), 400)

        usuario = _build_product_use_case().ativa_product_via_nome(nome, user)

        if usuario:
            return "Produto ativo com sucesso!", 200
        return "Erro ao ativar produto, verifique o nome.", 400
    
    @staticmethod
    def desativar_product():
        data = request.get_json() or {}

        nome = data.get("nome")
        user = data.get("user")

        if not nome or not user:
            return make_response(jsonify({"erro": "Um dos campos não foi preenchido."}), 400)

        product = _build_product_use_case().desativar_product_via_nome(nome, user)

        if product:
            return "Produto desativado com sucesso!", 200
        return "Erro ao desativar produto, verifique o nome.", 400
    
    @staticmethod
    def editar_product():
        data = request.get_json() or {}

        nome = data.get("nome")
        novo_nome = data.get("novo_nome")
        novo_preco = data.get("novo_preco")
        nova_qtd = data.get("nova_qtd")
        novo_status = data.get("novo_status")
        nova_image = data.get("nova_image")
        user = data.get("user")

        if not nome or not user:
            return make_response(jsonify({"erro": "Nome do produto ou usuário não informado."}), 400)

        success = _build_product_use_case().editar_product(
            nome, novo_nome, novo_preco, nova_qtd, novo_status, nova_image, user
        )

        if success:
            return "Produto editado com sucesso!", 200
        return "Erro ao editar produto, verifique o nome.", 400
    
    

