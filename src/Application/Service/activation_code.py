import random


def generate_activation_code():
    """
    Gera um código de ativação de 4 dígitos (0000 a 9999), sempre com 4 caracteres.

    Nos testes este gerador deve ser mockado para que o código seja
    determinístico — não se testa `random` de verdade.
    """
    return f'{random.randint(0, 9999):04d}'
