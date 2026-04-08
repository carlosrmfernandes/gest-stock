from abc import ABC, abstractmethod


class UserRepositoryPort(ABC):
    @abstractmethod
    def save(self, user_domain):
        raise NotImplementedError

    @abstractmethod
    def list_all(self):
        raise NotImplementedError

    @abstractmethod
    def busca_por_email(self, email):
        raise NotImplementedError

    @abstractmethod
    def ativa_usuario(self, email, codigo_ativacao):
        raise NotImplementedError
