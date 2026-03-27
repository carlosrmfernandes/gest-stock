from src.config.data_base import db 
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    celular = db.Column(db.String(11), unique=True, nullable=False)
    status = db.Column(db.Boolean, default=False, nullable=False)

    activation_code = db.Column(db.String(4))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "cnpj": self.cnpj,
            "email": self.email,
            "celular": self.celular,
            "status": self.status
        }

