from src.config.data_base import db 
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    celular = db.Column(db.String(13), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, default=False, nullable=False)
    codigoTwilio = db.Column(db.String(4), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,   
            "cnpj": self.cnpj,
            "celular": self.celular,
            "status": self.status,
            "codigoTwilio": self.codigoTwilio
        }
