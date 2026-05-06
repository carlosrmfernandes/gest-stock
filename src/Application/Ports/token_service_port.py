from abc import ABC, abstractmethod


class TokenServicePort(ABC):
    @abstractmethod
    def create_token(self, user_id):
        raise NotImplementedError

    @abstractmethod
    def validate_token(self, token):
        raise NotImplementedError
