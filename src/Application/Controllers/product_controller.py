from flask import request, jsonify, make_response, current_app
from flask_jwt_extended import get_jwt_identity
from src.Application.Service.product_service import ProductService
import os
import random
from werkzeug.utils import secure_filename

class ProductController:
    @staticmethod
    def criar_produto():
        seller_id = get_jwt_identity()
        
        nome = request.form.get('nome')
        preco = request.form.get('preco')
        estoque_quantidade = request.form.get('estoque_quantidade')
        estoque_unidade_id = request.form.get('estoque_unidade_id')
        conteudo_quantidade = request.form.get('conteudo_quantidade')
        conteudo_unidade_id = request.form.get('conteudo_unidade_id')
        
        imagem = request.files.get('imagem')

        try:
            if not nome or not preco or not estoque_quantidade or not estoque_unidade_id or not imagem:
                return make_response(jsonify({"erro": "Todos os campos obrigatórios e a imagem devem ser informados."}), 400)

            upload_folder = os.path.join(current_app.static_folder, 'uploads')
            
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            prefixo = str(random.randint(1000, 9999))
            filename = secure_filename(f"seller_{seller_id}_{prefixo}_{imagem.filename}")
            filepath = os.path.join(upload_folder, filename)
            
            imagem.save(filepath)
            
            imagem_url = f"/static/uploads/{filename}"

            dados = {
                "nome": nome,
                "preco": float(preco),
                "estoque_quantidade": float(estoque_quantidade),
                "estoque_unidade_id": int(estoque_unidade_id),
                "conteudo_quantidade": float(conteudo_quantidade) if conteudo_quantidade else None,
                "conteudo_unidade_id": int(conteudo_unidade_id) if conteudo_unidade_id else None,
                "imagem_path": imagem_url
            }

            produto = ProductService.criar_produto(dados, seller_id)
            return make_response(jsonify({
                "mensagem": "Produto cadastrado com sucesso!",
                "produto": produto.to_dict()
            }), 201)
        except Exception as e:
            return make_response(jsonify({"erro": f"Erro ao cadastrar produto: {str(e)}"}), 500)

    @staticmethod
    def listar_produtos():
        seller_id = get_jwt_identity()
        try:
            produtos = ProductService.listar_produtos_por_seller(seller_id)
            return make_response(jsonify([p.to_dict() for p in produtos]), 200)
        except Exception as e:
            return make_response(jsonify({"erro": f"Erro ao listar produtos: {str(e)}"}), 500)

    @staticmethod
    def inativar_produto(produto_id):
        seller_id = get_jwt_identity()
        try:
            sucesso = ProductService.inativar_produto(produto_id, seller_id)
            if sucesso:
                return make_response(jsonify({"mensagem": "Produto inativado com sucesso!"}), 200)
            return make_response(jsonify({"erro": "Produto não encontrado ou não pertence a você."}), 404)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)
        
    @staticmethod
    def atualizar_produto(produto_id):
        seller_id = get_jwt_identity()
        
        nome = request.form.get('nome')
        preco = request.form.get('preco')
        estoque_quantidade = request.form.get('estoque_quantidade')
        estoque_unidade_id = request.form.get('estoque_unidade_id')
        conteudo_quantidade = request.form.get('conteudo_quantidade')
        conteudo_unidade_id = request.form.get('conteudo_unidade_id')
        
        imagem = request.files.get('imagem')

        dados = {}
        if nome: dados['nome'] = nome
        if preco: dados['preco'] = float(preco)
        if estoque_quantidade: dados['estoque_quantidade'] = float(estoque_quantidade)
        if estoque_unidade_id: dados['estoque_unidade_id'] = int(estoque_unidade_id)
        
        dados['conteudo_quantidade'] = float(conteudo_quantidade) if conteudo_quantidade and conteudo_quantidade.strip() != '' else None
        dados['conteudo_unidade_id'] = int(conteudo_unidade_id) if conteudo_unidade_id and conteudo_unidade_id.strip() != '' else None

        if imagem and imagem.filename != '':
            upload_folder = os.path.join(current_app.static_folder, 'uploads')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            
            import random
            from werkzeug.utils import secure_filename
            prefixo = str(random.randint(1000, 9999))
            filename = secure_filename(f"seller_{seller_id}_{prefixo}_{imagem.filename}")
            filepath = os.path.join(upload_folder, filename)
            imagem.save(filepath)
            dados['imagem_path'] = f"/static/uploads/{filename}"

        try:
            produto = ProductService.atualizar_produto(produto_id, seller_id, dados)
            if not produto:
                return make_response(jsonify({"erro": "Produto não encontrado."}), 404)
            
            return make_response(jsonify({
                "mensagem": "Produto atualizado com sucesso!",
                "produto": produto.to_dict()
            }), 200)
        except Exception as e:
            return make_response(jsonify({"erro": f"Erro ao atualizar produto: {str(e)}"}), 500)