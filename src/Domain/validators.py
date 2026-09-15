import re

EMAIL_REGEX = re.compile(r'^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$')
PHONE_REGEX = re.compile(r'^\+55\d{10,11}$')


def normalize_cnpj(cnpj):
    """Remove pontuação do CNPJ, deixando apenas dígitos."""
    if cnpj is None:
        return ''
    return re.sub(r'\D', '', str(cnpj))


def is_valid_cnpj(cnpj):
    """
    Valida um CNPJ pelos dois dígitos verificadores.
    Aceita com ou sem máscara (00.000.000/0001-00 ou 00000000000100).
    """
    digits = normalize_cnpj(cnpj)

    if len(digits) != 14:
        return False

    if digits == digits[0] * 14:
        return False

    def check_digit(base, weights):
        total = sum(int(d) * w for d, w in zip(base, weights))
        rest = total % 11
        return '0' if rest < 2 else str(11 - rest)

    first = check_digit(digits[:12], [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    second = check_digit(digits[:13], [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])

    return digits[12] == first and digits[13] == second


def is_valid_email(email):
    """Valida o formato do e-mail."""
    if not email or not isinstance(email, str):
        return False
    return bool(EMAIL_REGEX.match(email.strip()))


def normalize_phone(phone):
    """Remove espaços, parênteses, hífens e pontos do celular."""
    if phone is None:
        return ''
    return re.sub(r'[\s()\-.]', '', str(phone))


def is_valid_phone(phone):
    """
    Valida o celular no formato internacional brasileiro: +55 seguido de DDD e número.
    Ex: +5511999999999
    """
    return bool(PHONE_REGEX.match(normalize_phone(phone)))


def is_valid_password(password):
    """A senha precisa ter no mínimo 6 caracteres."""
    return isinstance(password, str) and len(password) >= 6
