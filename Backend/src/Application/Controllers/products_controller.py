from flask import request, jsonify, make_response
from src.Application.Service.products_service import ProductsService
from src.Infrastructure.Model.products_model import Products
from src.config.data_base import db 

class ProductsController:
    @staticmethod
    def register_products():
        try:
            data = request.get_json()
            name = data.get('name')
            price = data.get('price')
            quantity = data.get('quantity')
            status = data.get('status')
            imagem = data.get('imagem')

            if not name or not price or not quantity:
                return make_response(jsonify({"erro": "Preencha todos os campos!"}), 400)

            products = ProductsService.create_user(name=name, price=price, quantity=quantity)

            return make_response(jsonify({
                "mensagem": "Produto salvo com sucesso!",
                "produtos": products.to_dict()
            }), 201)

        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 409)

        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)
        
    @staticmethod
    def get_products():
        try:
            products = Products.query.all()
            return make_response(jsonify([products.name for products in products]), 200)

        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def update_produts(products_id):
        try:
            products = Products.query.get(products_id)
            
            if not products:
                return make_response(jsonify({"erro": "Produto não encontrado"}), 404)

            data = request.get_json()
            products.name = data.get("name", products.name)
            products.price = data.get("price", products.price)
            products.quantity = data.get("quantity", products.quantity)
            products.status = data.get("status", products.status)
            
            if 'name' in data:
                products.name = data['name']

            db.session.commit()

            return make_response(jsonify({"mensagem": "Produto atualizado com sucesso!"}), 200)

        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def active_products():
        data = request.get_json()
        name = data.get('name')
        status = data.get('status')
        print(name)
        products = Products.query.filter_by(name=name).first()

        if products and products.status == False:
            products.status = True
            db.session.commit()
            return make_response(jsonify({"mensagem": "Produto ativado com sucesso!"}), 200)
        
        elif products.status == True:
            return make_response(jsonify({"ERRO": "ja atualizo porra"}), 400)

    @staticmethod
    def get_details_products():
        try:
            products = Products.query.all()
            return make_response(jsonify([products.to_dict() for products in products]), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

