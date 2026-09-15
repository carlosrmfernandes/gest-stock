STATUS_ATIVO = 'Ativo'
STATUS_INATIVO = 'Inativo'


class SellerDomain:
    """
    Representação de domínio de um mini mercado (seller).
    Não conhece banco de dados nem Flask.
    """

    def __init__(self, id, name, cnpj, email, phone, status=STATUS_INATIVO, activation_code=None):
        self.id = id
        self.name = name
        self.cnpj = cnpj
        self.email = email
        self.phone = phone
        self.status = status
        self.activation_code = activation_code

    def is_active(self):
        return self.status == STATUS_ATIVO

    def matches_code(self, code):
        """Compara o código informado com o código de ativação gerado."""
        if not self.activation_code or code is None:
            return False
        return str(code).strip() == str(self.activation_code)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "cnpj": self.cnpj,
            "email": self.email,
            "phone": self.phone,
            "status": self.status,
        }
