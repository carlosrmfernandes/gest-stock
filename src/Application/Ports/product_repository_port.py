from abc import ABC, abstractmethod


class ProductRepositoryPort(ABC):
    @abstractmethod
    def save(self, product_domain):
        raise NotImplementedError

    @abstractmethod
    def list_all(self):
        raise NotImplementedError

    @abstractmethod
    def ativa_product(self, nome, user):
        raise NotImplementedError

    @abstractmethod
    def desativar_product(self, nome, user):
        raise NotImplementedError
    
    @abstractmethod
    def update(self, nome, user):
        raise NotImplementedError
