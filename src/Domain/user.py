class UserDomain:
    def __init__(self, id, name, cnpj, email, celular, password, status="Inativo"):
        self.id = id
        self.name = name
        self.cnpj = cnpj
        self.email = email  
        self.celular = celular
        self.password = password
        self.status = status
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "cnpj": self.cnpj,
            "email": self.email,
            "celular": self.celular,
            "password": self.password,
            "status": self.status
        }
