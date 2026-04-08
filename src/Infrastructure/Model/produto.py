from src.config.data_base import db 
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    qtd = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, default=True, nullable=False)
    imagem = db.Column(db.String(255), nullable=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "qtd": self.qtd,
            "imagem": self.imagem,
            "User": self.user,
        }
        

