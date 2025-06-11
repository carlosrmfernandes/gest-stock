from flask import request, jsonify, make_response
from src.Application.Service.products_service import ProductsService
from src.Infrastructure.Model.products_model import Products
from src.config.data_base import db 
from src.Infrastructure.Model.sold_products import SoldProduct

from flask import request, jsonify, make_response


class ProductsController:
    @staticmethod
    def register_products(user_id):
        try:
            
            data = request.get_json()
            name = data.get('name')
            price = data.get('price')
            quantity = data.get('quantity')
            imagem = data.get('imagem')

            if not name or not price or not quantity:
                return make_response(jsonify({"erro": "Preencha todos os campos!"}), 400)

            product = ProductsService.create_products(
                name=name,
                price=price,
                quantity=quantity,
                imagem=imagem,
                user=user_id
            )

            return make_response(jsonify({
                "mensagem": "Produto salvo com sucesso!",
                "produto": product.to_dict()
            }), 201)

        except ValueError as e:
            
            return (make_response(jsonify({"erro": str(e)}), 409))
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

        
    @staticmethod
    def get_products():
        try:
            products = Products.query.all()
            return make_response(jsonify([product.to_dict() for product in products if product.status == 1]), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

        
    @staticmethod
    def get_user_products(user_id):
        try:
            products = Products.query.filter_by(user=user_id).all()
            return make_response(jsonify([product.to_dict() for product in products]), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)



    @staticmethod
    def update_products(product_id):
        try:
            product = Products.query.get(product_id)
            if not product:
                return make_response(jsonify({"erro": "Produto não encontrado"}), 404)

            data = request.get_json()
            product.name = data.get("name", product.name)
            product.price = data.get("price", product.price)
            product.quantity = data.get("quantity", product.quantity)

            product.status = product.quantity >= 1

            db.session.commit()

            return make_response(jsonify({"mensagem": "Produto atualizado com sucesso!", "produto": product.to_dict()}), 200)

        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)


    @staticmethod
    def get_details_product(product_id):
        try:
            product = Products.query.get(product_id)
            if not product:
                return make_response(jsonify({"erro": "Produto não encontrado"}), 404)

            return make_response(jsonify(product.to_dict()), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)


    @staticmethod
    def buy_products(product_id, user_id):
        try:
            product = Products.query.get(product_id)

            if not product:
                return make_response(jsonify({"erro": "Produto não encontrado"}), 404)

            data = request.get_json()
            quantidade_comprada = data.get("quantidade")

            if not quantidade_comprada or quantidade_comprada <= 0:
                return make_response(jsonify({"erro": "Quantidade inválida"}), 400)

            if product.quantity < quantidade_comprada:
                return make_response(jsonify({"erro": "Estoque insuficiente"}), 400)


            product.quantity -= quantidade_comprada

            if product.quantity == 0:
                product.status = False

            venda = SoldProduct(
                product_id=product.id,
                user_id=product.user,  
                buyer_id=user_id,        
                quantity=quantidade_comprada,
                price_at_sale=product.price
            )

            db.session.add(venda)
            db.session.commit()

            return make_response(jsonify({
                "mensagem": "Compra realizada com sucesso!",
                "produto": product.to_dict(),
                "venda": venda.to_dict()
            }), 200)

        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)
        
    @staticmethod
    def toggle_product_status(product_id):
            try:
                product = Products.query.get(product_id)
                if not product:
                    return make_response(jsonify({"erro": "Produto não encontrado"}), 404)

                # inverter o status
                product.status = not product.status
                db.session.commit()

                status_str = "ativado" if product.status else "desativado"
                return make_response(jsonify({"mensagem": f"Produto {status_str} com sucesso!", "produto": product.to_dict()}), 200)

            except Exception as e:
                return make_response(jsonify({"erro": str(e)}), 500)