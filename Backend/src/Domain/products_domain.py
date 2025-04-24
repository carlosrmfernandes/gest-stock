class ProductsDomain:
    def __init__(self, name, price, quantity, status=False, imagem=None):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.status = status
        self.imagem = None
    
    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "status": self.status,
            "imagem": self.imagem
        }
