
from flask import request, jsonify, make_response
from flask_jwt_extended import get_jwt_identity
from src.Application.Service.venda_service import VendaService

class VendaController:
    @staticmethod
    def realizar_venda():
        seller_id = get_jwt_identity() 
        data = request.get_json()
        
        carrinho = data.get('carrinho') # Ex: [{"produto_id": 1, "quantidade": 2}]
        
        if not carrinho or len(carrinho) == 0:
            return make_response(jsonify({"erro": "O carrinho está vazio."}), 400)
            
        try:
            venda_realizada = VendaService.registrar_venda(seller_id, carrinho)
            return make_response(jsonify({
                "mensagem": "Venda concluída com sucesso!",
                "venda": venda_realizada.to_dict()
            }), 201)
            
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"erro": f"Erro interno: {str(e)}"}), 500)