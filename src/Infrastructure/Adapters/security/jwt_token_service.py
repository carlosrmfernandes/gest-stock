from datetime import datetime, timedelta, timezone

import jwt

from src.Application.Ports.token_service_port import TokenServicePort

ALGORITHM = "HS256"


class JwtTokenService(TokenServicePort):
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def create_token(self, user_id):
        payload = {
            "sub": str(user_id),
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        }
        return jwt.encode(payload, self.secret_key, algorithm=ALGORITHM)

    def validate_token(self, token):
        try:
            return jwt.decode(token, self.secret_key, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            return {"erro": "Token expirado"}
        except jwt.InvalidTokenError:
            return {"erro": "Token invalido"}
