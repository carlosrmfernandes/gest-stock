class ProductDomain:
    def __init__(self, id, nome, preco, qtd, status=False, image=None, user=None):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.qtd = qtd
        self.status = status
        self.user = user
        self.image = image


    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "qtd": self.qtd,
            "status": self.status,
            "image": self.image,
            "User": self.user,
        }
