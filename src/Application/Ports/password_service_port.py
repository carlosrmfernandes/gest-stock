from abc import ABC, abstractmethod


class PasswordServicePort(ABC):
    @abstractmethod
    def hash_password(self, password):
        raise NotImplementedError

    @abstractmethod
    def verify_password(self, stored_password, provided_password):
        raise NotImplementedError
