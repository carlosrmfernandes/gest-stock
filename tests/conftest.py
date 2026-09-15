"""
Fixtures compartilhadas da prova P1.

São 5 fixtures, e elas cobrem tudo o que a prova precisa:

    seller_repository   mock do banco
    notifier            mock do envio de WhatsApp/SMS
    code_generator      mock do gerador de código (determinístico)
    seller_payload      um cadastro válido, pronto para usar
    active_seller       um seller "já existente", para simular duplicidade

Você NÃO precisa (e não deve) subir banco de dados nem acessar a internet
nos testes. Use os mocks abaixo.
"""
from unittest.mock import MagicMock

import pytest

from src.Domain.seller import STATUS_ATIVO
from src.Infrastructure.Model.seller import Seller


@pytest.fixture
def seller_repository():
    """
    Mock do SellerRepository.

    Padrão: o "banco" está vazio — nenhuma busca encontra nada — e o `save`
    devolve o próprio objeto que recebeu.

    Para simular que já existe alguém cadastrado:
        seller_repository.find_by_email.return_value = active_seller
    """
    repository = MagicMock()
    repository.find_by_email.return_value = None
    repository.find_by_cnpj.return_value = None
    repository.find_by_phone.return_value = None
    repository.save.side_effect = lambda seller: seller
    repository.update.side_effect = lambda seller: seller
    return repository


@pytest.fixture
def notifier():
    """
    Mock do ActivationNotifier (envio de WhatsApp/SMS pelo Twilio).

    Padrão: o envio funciona e devolve o id da mensagem.

    Para simular que o provedor caiu:
        notifier.send_activation_code.side_effect = NotificationError('fora do ar')
    """
    fake = MagicMock()
    fake.send_activation_code.return_value = 'SM-fake-sid'
    return fake


@pytest.fixture
def code_generator():
    """
    Mock do gerador de código de ativação: sempre retorna '1234'.

    Sem isso o código seria aleatório e o teste não teria o que assertar.
    """
    return MagicMock(return_value='1234')


@pytest.fixture
def seller_payload():
    """
    Payload VÁLIDO de cadastro de seller.

    Use direto:            service.create_seller(**seller_payload)
    Ou invalide um campo:  seller_payload['cnpj'] = '123'
    """
    return {
        'name': 'Mini Mercado X',
        'cnpj': '11.222.333/0001-81',
        'email': 'mercado@email.com',
        'phone': '+5511999999999',
        'password': '123456',
    }


@pytest.fixture
def active_seller():
    """
    Um seller que já está no banco.

    Serve para simular duplicidade de e-mail, CNPJ ou celular:
        seller_repository.find_by_cnpj.return_value = active_seller
    """
    return Seller(
        id=1,
        name='Mini Mercado X',
        cnpj='11222333000181',
        email='mercado@email.com',
        phone='+5511999999999',
        password='hash-fake',
        status=STATUS_ATIVO,
        activation_code=None,
    )
