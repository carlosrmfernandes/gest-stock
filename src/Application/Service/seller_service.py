from werkzeug.security import generate_password_hash

from src.Application.Service.activation_code import generate_activation_code
from src.Domain.exceptions import (
    BusinessRuleError,
    ConflictError,
    NotFoundError,
    ValidationError,
)
from src.Domain.seller import STATUS_ATIVO, STATUS_INATIVO
from src.Domain.validators import (
    is_valid_cnpj,
    is_valid_email,
    is_valid_password,
    is_valid_phone,
    normalize_cnpj,
    normalize_phone,
)
from src.Infrastructure.http.whats_app import ActivationNotifier
from src.Infrastructure.Model.seller import Seller
from src.Infrastructure.Repository.seller_repository import SellerRepository


class SellerService:
    """
    Regras de negócio do mini mercado (seller).

    As dependências (repositório, notificador e gerador de código) entram pelo
    construtor justamente para que os testes possam injetar mocks.
    """

    def __init__(self, repository=None, notifier=None, code_generator=None):
        self.repository = repository or SellerRepository()
        self.notifier = notifier or ActivationNotifier()
        self.code_generator = code_generator or generate_activation_code

    def create_seller(self, name, cnpj, email, phone, password):
        """
        Cadastra um seller com status Inativo e envia o código de ativação
        de 4 dígitos por WhatsApp/SMS.

        Regras:
          - todos os campos são obrigatórios;
          - CNPJ, e-mail e celular precisam ser válidos e a senha ter 6+ caracteres;
          - CNPJ, e-mail e celular são únicos;
          - a senha nunca é armazenada em texto puro;
          - o seller nasce Inativo, com um código de ativação gerado;
          - se o envio da mensagem falhar, o erro sobe (NotificationError).
        """
        if not name or not str(name).strip():
            raise ValidationError('Nome é obrigatório')

        if not is_valid_cnpj(cnpj):
            raise ValidationError('CNPJ inválido')

        if not is_valid_email(email):
            raise ValidationError('E-mail inválido')

        if not is_valid_phone(phone):
            raise ValidationError('Celular inválido')

        if not is_valid_password(password):
            raise ValidationError('Senha deve ter no mínimo 6 caracteres')

        clean_cnpj = normalize_cnpj(cnpj)
        clean_phone = normalize_phone(phone)
        clean_email = email.strip().lower()

        if self.repository.find_by_email(clean_email):
            raise ConflictError('E-mail já cadastrado')

        if self.repository.find_by_cnpj(clean_cnpj):
            raise ConflictError('CNPJ já cadastrado')

        if self.repository.find_by_phone(clean_phone):
            raise ConflictError('Celular já cadastrado')

        code = self.code_generator()

        seller = Seller(
            name=str(name).strip(),
            cnpj=clean_cnpj,
            email=clean_email,
            phone=clean_phone,
            password=generate_password_hash(password),
            status=STATUS_INATIVO,
            activation_code=code,
        )

        self.repository.save(seller)

        self.notifier.send_activation_code(clean_phone, code)

        return seller.to_domain()

    def activate_seller(self, phone, code):
        """
        Ativa o seller a partir do celular + código recebido na mensagem.

        Regras:
          - celular e código são obrigatórios;
          - celular não cadastrado -> NotFoundError;
          - seller já ativo -> BusinessRuleError;
          - código diferente do gerado -> ValidationError;
          - ao ativar, o status vira Ativo e o código é descartado.
        """
        if not phone or not code:
            raise ValidationError('Celular e código são obrigatórios')

        clean_phone = normalize_phone(phone)
        seller = self.repository.find_by_phone(clean_phone)

        if seller is None:
            raise NotFoundError('Seller não encontrado')

        if seller.status == STATUS_ATIVO:
            raise BusinessRuleError('Seller já está ativo')

        if not seller.to_domain().matches_code(code):
            raise ValidationError('Código de ativação inválido')

        seller.status = STATUS_ATIVO
        seller.activation_code = None
        self.repository.update(seller)

        return seller.to_domain()
