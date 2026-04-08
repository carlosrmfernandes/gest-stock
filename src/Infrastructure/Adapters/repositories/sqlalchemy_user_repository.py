from src.Application.Ports.user_repository_port import UserRepositoryPort
from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import and_, db


class SqlAlchemyUserRepository(UserRepositoryPort):
    @staticmethod
    def _to_domain(user):
        return UserDomain(
            id=user.id,
            nome=user.nome,
            email=user.email,
            senha=user.senha,
            cnpj=user.cnpj,
            celular=user.celular,
            status=user.status,
            codigoTwilio=user.codigoTwilio,
        )

    def save(self, user_domain):
        user = User(
            nome=user_domain.nome,
            cnpj=user_domain.cnpj,
            email=user_domain.email,
            celular=user_domain.celular,
            senha=user_domain.senha,
            status=user_domain.status,
            codigoTwilio=user_domain.codigoTwilio,
        )
        db.session.add(user)
        db.session.commit()
        return self._to_domain(user)

    def list_all(self):
        return [self._to_domain(user) for user in User.query.all()]

    def busca_por_email(self, email):
        user = db.session.query(User).where(User.email == email).first()
        return self._to_domain(user) if user else None

    def ativa_usuario(self, email, codigo_ativacao):
        usuario = db.session.query(User).where(
            and_(
                User.email == email,
                User.codigoTwilio == codigo_ativacao,
            )
        ).first()

        if usuario:
            usuario.status = True
            db.session.add(usuario)
            db.session.commit()
            return True
        return False
