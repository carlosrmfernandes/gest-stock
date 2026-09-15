import pytest

from src.Application.Service.seller_service import SellerService
from src.Domain.exceptions import ConflictError, ValidationError, NotificationError


def test_create_seller_retorna_seller_inativo(
    seller_repository, notifier, code_generator, seller_payload
):
    """Cadastro válido deve retornar um seller com status Inativo."""
    service = SellerService(
        repository=seller_repository,
        notifier=notifier,
        code_generator=code_generator,
    )
    seller = service.create_seller(**seller_payload)
    assert seller.status == "Inativo"


def test_create_seller_salva_uma_vez(
    seller_repository, notifier, code_generator, seller_payload
):
    """Cadastro válido deve salvar o seller exatamente uma vez."""
    service = SellerService(seller_repository, notifier, code_generator)
    service.create_seller(**seller_payload)
    seller_repository.save.assert_called_once()


def test_create_seller_nao_salva_senha_em_texto_puro(
    seller_repository, notifier, code_generator, seller_payload
):
    """A senha salva deve ser diferente da senha original."""
    service = SellerService(seller_repository, notifier, code_generator)
    service.create_seller(**seller_payload)

    seller_salvo = seller_repository.save.call_args[0][0]

    assert seller_salvo.password != "123456"


def test_create_seller_normaliza_cnpj_e_email(
    seller_repository, notifier, code_generator, seller_payload
):
    """O CNPJ deve ser salvo sem máscara e o e-mail em letras minúsculas."""
    service = SellerService(seller_repository, notifier, code_generator)
    service.create_seller(**seller_payload)

    seller_salvo = seller_repository.save.call_args[0][0]

    assert seller_salvo.cnpj == "11222333000181"
    assert seller_salvo.email == seller_payload["email"].lower()


def test_create_seller_envia_codigo_de_ativacao(
    seller_repository, notifier, code_generator, seller_payload
):
    """Após salvar, o código gerado deve ser enviado ao celular informado."""
    service = SellerService(seller_repository, notifier, code_generator)
    service.create_seller(**seller_payload)

    notifier.send_activation_code.assert_called_once_with(
        "+5511999999999",
        "1234",
    )


@pytest.mark.parametrize(
    "campo, valor_invalido",
    [
        ("name", ""),
        ("cnpj", "11.222.333/0001-99"),
        ("email", "email-sem-arroba"),
        ("phone", "11999999999"),
        ("password", "12345"),
    ],
)
def test_create_seller_dados_invalidos_nao_salva_nem_envia_mensagem(
    seller_repository,
    notifier,
    code_generator,
    seller_payload,
    campo,
    valor_invalido,
):
    """Dados inválidos devem gerar ValidationError antes de salvar ou enviar mensagem."""
    payload = seller_payload.copy()
    payload[campo] = valor_invalido

    service = SellerService(seller_repository, notifier, code_generator)

    with pytest.raises(ValidationError):
        service.create_seller(**payload)

    seller_repository.save.assert_not_called()
    notifier.send_activation_code.assert_not_called()


def test_create_seller_com_email_duplicado_nao_salva_nem_envia(
    seller_repository, notifier, code_generator, seller_payload, active_seller
):
    """Se o e-mail já existe, nada deve ser salvo e nenhuma mensagem deve ser enviada."""
    seller_repository.find_by_email.return_value = active_seller

    service = SellerService(seller_repository, notifier, code_generator)

    with pytest.raises(ConflictError):
        service.create_seller(**seller_payload)

    seller_repository.save.assert_not_called()
    notifier.send_activation_code.assert_not_called()


def test_create_seller_com_cnpj_duplicado_nao_salva_nem_envia(
    seller_repository, notifier, code_generator, seller_payload, active_seller
):
    """Se o CNPJ já existe, nada deve ser salvo e nenhuma mensagem deve ser enviada."""
    seller_repository.find_by_cnpj.return_value = active_seller

    service = SellerService(seller_repository, notifier, code_generator)

    with pytest.raises(ConflictError):
        service.create_seller(**seller_payload)

    seller_repository.save.assert_not_called()
    notifier.send_activation_code.assert_not_called()


def test_create_seller_com_celular_duplicado_nao_salva_nem_envia(
    seller_repository, notifier, code_generator, seller_payload, active_seller
):
    """Se o celular já existe, nada deve ser salvo e nenhuma mensagem deve ser enviada."""
    seller_repository.find_by_phone.return_value = active_seller

    service = SellerService(seller_repository, notifier, code_generator)

    with pytest.raises(ConflictError):
        service.create_seller(**seller_payload)

    seller_repository.save.assert_not_called()
    notifier.send_activation_code.assert_not_called()


def test_create_seller_se_notificacao_falhar_erro_sobe_e_seller_ja_foi_salvo(
    seller_repository, notifier, code_generator, seller_payload
):
    """Se o provedor falhar, NotificationError deve subir depois que o seller foi salvo."""
    notifier.send_activation_code.side_effect = NotificationError(
        "provedor fora do ar"
    )

    service = SellerService(seller_repository, notifier, code_generator)

    with pytest.raises(NotificationError):
        service.create_seller(**seller_payload)

    seller_repository.save.assert_called_once()