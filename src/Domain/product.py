PRODUCT_ATIVO = 'Ativo'
PRODUCT_INATIVO = 'Inativo'


class ProductDomain:
    """Representação de domínio de um produto pertencente a um seller."""

    def __init__(self, id, seller_id, name, price, quantity, status=PRODUCT_ATIVO, img=None):
        self.id = id
        self.seller_id = seller_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.status = status
        self.img = img

    def is_active(self):
        return self.status == PRODUCT_ATIVO

    def is_in_stock(self):
        return self.quantity > 0

    def to_dict(self):
        return {
            "id": self.id,
            "seller_id": self.seller_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "status": self.status,
            "img": self.img,
        }
