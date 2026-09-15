"""
Fixtures compartilhadas da prova P1.

Você NÃO precisa (e não deve) subir banco de dados para os testes de unidade.
Use os mocks/fixtures abaixo.
"""
from unittest.mock import MagicMock

import pytest

from src.Domain.product import PRODUCT_ATIVO
from src.Domain.seller import STATUS_ATIVO, STATUS_INATIVO
from src.Infrastructure.Model.product import Product
from src.Infrastructure.Model.seller import Seller


@pytest.fixture
def seller_repository():
    """Mock do SellerRepository. Por padrão, nada existe no 'banco'."""
    repository = MagicMock()
    repository.find_by_email.return_value = None
    repository.find_by_cnpj.return_value = None
    repository.find_by_phone.return_value = None
    repository.find_by_id.return_value = None
    repository.save.side_effect = lambda seller: seller
    repository.update.side_effect = lambda seller: seller
    return repository


@pytest.fixture
def product_repository():
    """Mock do ProductRepository."""
    repository = MagicMock()
    repository.find_by_id.return_value = None
    repository.find_by_seller.return_value = []
    repository.find_by_name_and_seller.return_value = None
    repository.save.side_effect = lambda product: product
    return repository


@pytest.fixture
def notifier():
    """Mock do ActivationNotifier (envio de WhatsApp/SMS)."""
    fake = MagicMock()
    fake.send_activation_code.return_value = 'SM-fake-sid'
    return fake


@pytest.fixture
def code_generator():
    """Gerador de código determinístico: sempre retorna '1234'."""
    return MagicMock(return_value='1234')


@pytest.fixture
def seller_payload():
    """Payload válido de cadastro de seller."""
    return {
        'name': 'Mini Mercado X',
        'cnpj': '11.222.333/0001-81',
        'email': 'mercado@email.com',
        'phone': '+5511999999999',
        'password': '123456',
    }


@pytest.fixture
def inactive_seller():
    """Seller já cadastrado, status Inativo, com código de ativação '1234'."""
    return Seller(
        id=1,
        name='Mini Mercado X',
        cnpj='11222333000181',
        email='mercado@email.com',
        phone='+5511999999999',
        password='hash-fake',
        status=STATUS_INATIVO,
        activation_code='1234',
    )


@pytest.fixture
def active_seller():
    """Seller já ativado."""
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


@pytest.fixture
def product():
    """Produto de exemplo pertencente ao seller 1."""
    return Product(
        id=1,
        seller_id=1,
        name='Arroz',
        price=10.50,
        quantity=100,
        status=PRODUCT_ATIVO,
        img='http://img/arroz.png',
    )
