from src.config.data_base import db
from src.Domain.seller import SellerDomain, STATUS_INATIVO


class Seller(db.Model):
    __tablename__ = 'sellers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False, default=STATUS_INATIVO)
    activation_code = db.Column(db.String(4), nullable=True)

    def to_domain(self):
        return SellerDomain(
            id=self.id,
            name=self.name,
            cnpj=self.cnpj,
            email=self.email,
            phone=self.phone,
            status=self.status,
            activation_code=self.activation_code,
        )
