from abc import ABC, abstractmethod


class MessageServicePort(ABC):
    @abstractmethod
    def send_activation(self, celular, codigo):
        raise NotImplementedError
