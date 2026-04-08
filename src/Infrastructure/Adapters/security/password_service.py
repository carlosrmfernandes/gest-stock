from werkzeug.security import check_password_hash, generate_password_hash

from src.Application.Ports.password_service_port import PasswordServicePort


class PasswordService(PasswordServicePort):
    def hash_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, stored_password, provided_password):
        stored_password = stored_password or ""

        if stored_password.startswith(("pbkdf2:", "scrypt:")):
            return check_password_hash(stored_password, provided_password)

        return stored_password == provided_password
