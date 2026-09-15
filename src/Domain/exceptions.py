class DomainError(Exception):
    """Erro base do domínio. Carrega uma mensagem e um status HTTP sugerido."""
    status_code = 400

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class ValidationError(DomainError):
    """Dado de entrada inválido (formato, campo obrigatório ausente, etc)."""
    status_code = 400


class NotFoundError(DomainError):
    """Recurso não encontrado."""
    status_code = 404


class ConflictError(DomainError):
    """Violação de unicidade (e-mail, CNPJ ou celular já cadastrado)."""
    status_code = 409


class BusinessRuleError(DomainError):
    """Regra de negócio violada (ex: seller inativo tentando cadastrar produto)."""
    status_code = 422


class NotificationError(DomainError):
    """Falha ao enviar a mensagem pelo provedor externo."""
    status_code = 502
