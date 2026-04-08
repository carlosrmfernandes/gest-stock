from functools import wraps

from flask import current_app, jsonify, make_response, request

from src.Application.UseCases.user_use_case import UserUseCase
from src.Infrastructure.Adapters.messaging.twilio_message_service import TwilioMessageService
from src.Infrastructure.Adapters.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)
from src.Infrastructure.Adapters.security.jwt_token_service import JwtTokenService
from src.Infrastructure.Adapters.security.password_service import PasswordService


def _build_user_use_case():
    return UserUseCase(
        user_repository=SqlAlchemyUserRepository(),
        message_service=TwilioMessageService(),
        password_service=PasswordService(),
        token_service=JwtTokenService(current_app.config["JWT_SECRET_KEY"]),
    )


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        authorization = request.headers.get("Authorization", "")

        if not authorization.startswith("Bearer "):
            return make_response(jsonify({"erro": "Token ausente ou mal formatado."}), 401)

        token = authorization.split(" ", 1)[1].strip()
        payload = _build_user_use_case().validar_token(token)

        if isinstance(payload, dict) and payload.get("erro"):
            return make_response(jsonify(payload), 401)

        return func(*args, **kwargs)

    return wrapper


class UserController:
    @staticmethod
    def register_user():
        data = request.get_json() or {}

        nome = data.get("nome")
        cnpj = data.get("cnpj")
        email = data.get("email")
        celular = data.get("celular")
        senha = data.get("senha")

        if not nome or not email or not senha or not celular or not cnpj:
            return make_response(jsonify({"erro": "Um campo nao foi preenchido."}), 400)

        if len(cnpj) < 14:
            return make_response(jsonify("CNPJ invalido. Sao necessarios pelo menos 14 digitos."), 401)

        if len(celular) < 11:
            return make_response(jsonify("Numero de celular invalido. Use um numero valido e funcional."), 401)

        try:
            user, twilio_result = _build_user_use_case().register_user(
                nome=nome,
                cnpj=cnpj,
                email=email,
                celular=celular,
                senha=senha,
            )
        except Exception as exc:
            return make_response(
                jsonify(
                    {
                        "erro": "Falha no cadastro ou no envio do WhatsApp.",
                        "detalhe": str(exc),
                    }
                ),
                502,
            )

        return make_response(
            jsonify(
                {
                    "mensagem": "Usuario salvo com sucesso. Verifique o WhatsApp.",
                    "usuarios cadastrados": user.to_dict(),
                    "whatsapp": twilio_result,
                }
            ),
            200,
        )

    @staticmethod
    def testarNumero():
        try:
            result = _build_user_use_case().send_test_activation("5511958942521")
            return make_response(jsonify(result), 200)
        except Exception as exc:
            return make_response(jsonify({"erro": str(exc)}), 500)

    @staticmethod
    @token_required
    def verUsuarios():
        return make_response(jsonify({"usuarios": _build_user_use_case().list_users()}), 200)

    @staticmethod
    def ativar_usuario():
        data = request.get_json() or {}

        email = data.get("email")
        codigoAtivacao = data.get("codigoAtivacao")

        if not email or not codigoAtivacao:
            return make_response(jsonify({"erro": "Um campo nao foi preenchido."}), 400)

        usuario = _build_user_use_case().ativa_usuario_via_email(email, codigoAtivacao)

        if usuario:
            return "Usuario ativo com sucesso!", 200
        return "Erro ao ativar usuario, verifique o email ou o codigo de ativacao.", 400

    @staticmethod
    def login_user():
        data = request.get_json() or {}

        email = data.get("email")
        senha = data.get("senha")

        if not email or not senha:
            return make_response(jsonify({"erro": "Um campo nao foi preenchido."}), 400)

        usuario = _build_user_use_case().validar_usuario(email, senha)

        if not usuario:
            return {"erro": "Login invalido"}, 400

        token = _build_user_use_case().criar_token(user_id=usuario.id)

        return {
            "access_token": token,
            "token_type": "bearer",
        }, 200
