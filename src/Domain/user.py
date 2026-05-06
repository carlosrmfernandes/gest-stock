class UserDomain:
    def __init__(self, id, nome, email, senha, cnpj, celular, codigoTwilio, status=False):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.cnpj = cnpj
        self.celular = celular
        self.status = status
        self.codigoTwilio = codigoTwilio

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "cnpj": self.cnpj,
            "celular": self.celular,
            "status": self.status,
            "codigoTwilio": self.codigoTwilio,
        }
