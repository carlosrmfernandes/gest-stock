from src.Infrastructure.Model.user import User
from src.config.data_base import db 

class UserService:
    @staticmethod
    def create_user(name, email, password):
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            raise ValueError("O email já está cadastrado.")

        user = User(
            name=name,
            email=email,
            password=password
        )

        db.session.add(user)
        db.session.commit()
        return user
