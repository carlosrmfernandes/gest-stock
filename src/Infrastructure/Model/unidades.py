from src.config.data_base import db

class Unidade(db.Model):
    __tablename__ = 'unidades'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    sigla = db.Column(db.String(10), nullable=False, unique=True)
    tipo = db.Column(db.String(30), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "sigla": self.sigla,
            "tipo": self.tipo
        }