from src.config.data_base import db
from src.Infrastructure.Model.seller import Seller


class SellerRepository:
    """
    Isola o acesso ao banco. Nos testes de unidade esta classe deve ser
    substituída por um mock — nenhum teste unitário deve tocar o banco real.
    """

    def save(self, seller):
        db.session.add(seller)
        db.session.commit()
        return seller

    def update(self, seller):
        db.session.commit()
        return seller

    def find_by_id(self, seller_id):
        return db.session.get(Seller, seller_id)

    def find_by_email(self, email):
        return Seller.query.filter_by(email=email).first()

    def find_by_cnpj(self, cnpj):
        return Seller.query.filter_by(cnpj=cnpj).first()

    def find_by_phone(self, phone):
        return Seller.query.filter_by(phone=phone).first()
