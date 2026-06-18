from src.config.data_base import db
from datetime import datetime

class Venda(db.Model):
    __tablename__ = 'vendas'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    data_venda = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    valor_total = db.Column(db.Float, nullable=False, default=0.0)

    itens = db.relationship('VendaItem', backref='venda', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "seller_id": self.seller_id,
            "data_venda": self.data_venda.strftime('%Y-%m-%d %H:%M:%S'),
            "valor_total": self.valor_total,
            "itens": [item.to_dict() for item in self.itens]
        }