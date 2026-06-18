from src.config.data_base import db
from src.Infrastructure.Model.produtos import Produto

class ProductService:
    @staticmethod
    def criar_produto(dados, seller_id):
        novo_produto = Produto(
            nome=dados['nome'],
            preco=dados['preco'],
            estoque_quantidade=dados['estoque_quantidade'],
            estoque_unidade_id=dados['estoque_unidade_id'],
            conteudo_quantidade=dados.get('conteudo_quantidade'),
            conteudo_unidade_id=dados.get('conteudo_unidade_id'),
            imagem_path=dados.get('imagem_path'),
            seller_id=seller_id
        )
        db.session.add(novo_produto)
        db.session.commit()
        return novo_produto

    @staticmethod
    def listar_produtos_por_seller(seller_id):
        return Produto.query.filter_by(seller_id=seller_id).order_by(Produto.nome.asc()).all()
        
    @staticmethod
    def inativar_produto(produto_id, seller_id):
        produto = Produto.query.filter_by(id=produto_id, seller_id=seller_id).first()
        if produto:
            produto.status = False
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def atualizar_produto(produto_id, seller_id, dados):
        produto = Produto.query.filter_by(id=produto_id, seller_id=seller_id).first()
        if not produto:
            return None
        
        produto.nome = dados.get('nome', produto.nome)
        produto.preco = dados.get('preco', produto.preco)
        produto.estoque_quantidade = dados.get('estoque_quantidade', produto.estoque_quantidade)
        produto.estoque_unidade_id = dados.get('estoque_unidade_id', produto.estoque_unidade_id)
        
        if 'conteudo_quantidade' in dados:
            produto.conteudo_quantidade = dados['conteudo_quantidade']
        if 'conteudo_unidade_id' in dados:
            produto.conteudo_unidade_id = dados['conteudo_unidade_id']
            
        if dados.get('imagem_path'):
            produto.imagem_path = dados.get('imagem_path')

        db.session.commit()
        return produto