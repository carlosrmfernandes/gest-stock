from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db 

class UserService:
    @staticmethod
    def create_user(name, email, password):        
        user = User(name=name, email=email, password=password)        
        db.session.add(user)
        db.session.commit()       
        return UserDomain(user.id, user.name, user.email, user.password)
