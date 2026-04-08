import secrets

from src.Domain.user import UserDomain


class UserUseCase:
    def __init__(self, user_repository, message_service, password_service, token_service):
        self.user_repository = user_repository
        self.message_service = message_service
        self.password_service = password_service
        self.token_service = token_service

    @staticmethod
    def _gerar_codigo(tamanho=4):
        maximo = 10**tamanho
        return f"{secrets.randbelow(maximo):0{tamanho}}"

    def criar_token(self, user_id: int):
        return self.token_service.create_token(user_id)

    def validar_token(self, token: str):
        return self.token_service.validate_token(token)

    def register_user(self, nome, cnpj, email, celular, senha):
        codigo = self._gerar_codigo()

        user = UserDomain(
            id=None,
            nome=nome,
            email=email,
            senha=self.password_service.hash_password(senha),
            cnpj=cnpj,
            celular=celular,
            codigoTwilio=codigo,
        )

        saved_user = self.user_repository.save(user)
        message_result = self.message_service.send_activation(celular, codigo)
        return saved_user, message_result

    def list_users(self):
        return [user.to_dict() for user in self.user_repository.list_all()]

    def send_test_activation(self, celular):
        codigo = self._gerar_codigo()
        return self.message_service.send_activation(celular, codigo)

    def validar_usuario(self, email, senha):
        usuario = self.user_repository.busca_por_email(email)

        if not usuario:
            return False

        return (
            usuario
            if self.password_service.verify_password(usuario.senha, senha)
            else False
        )

    def ativa_usuario_via_email(self, email, codigoAtivacao):
        return self.user_repository.ativa_usuario(email, codigoAtivacao)
