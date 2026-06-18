from src.config.data_base import db
from src.Infrastructure.Model.vendas import Venda
from src.Infrastructure.Model.vendas_itens import VendaItem
from src.Infrastructure.Model.produtos import Produto

class VendaService:
    @staticmethod
    def registrar_venda(seller_id, carrinho):
        """
        carrinho: lista de dicionários ex: [{"produto_id": 1, "quantidade": 2.5}, ...]
        """
        nova_venda = Venda(seller_id=seller_id, valor_total=0.0)
        db.session.add(nova_venda)
        db.session.flush()

        valor_total_venda = 0.0

        for item in carrinho:
            produto = Produto.query.filter_by(id=item['produto_id'], seller_id=seller_id).first()
            
            if not produto:
                raise ValueError(f"Produto ID {item['produto_id']} não encontrado ou não pertence a você.")

            # RN1: Bloqueio de Inativos
            if not produto.status:
                raise ValueError(f"O produto '{produto.nome}' está inativo e não pode ser vendido.")

            # RN2: Validação de Estoque
            if item['quantidade'] > produto.estoque_quantidade:
                raise ValueError(f"Estoque insuficiente para '{produto.nome}'. Disponível: {produto.estoque_quantidade}.")

            subtotal = produto.preco * item['quantidade']
            valor_total_venda += subtotal

            # Cria o registro do item vendido
            novo_item = VendaItem(
                venda_id=nova_venda.id,
                produto_id=produto.id,
                quantidade=item['quantidade'],
                preco_unitario=produto.preco,
                subtotal=subtotal
            )
            db.session.add(novo_item)

            # RN3: Baixa Automática no Estoque
            produto.estoque_quantidade -= item['quantidade']

        nova_venda.valor_total = round(valor_total_venda, 2)
        db.session.commit()
        
        return nova_venda