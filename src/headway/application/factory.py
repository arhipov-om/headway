import uuid

from headway.domain.entitites import User


class UserFactory:

    @staticmethod
    def create(name: str) -> User:
        return User(
            id=uuid.uuid4(),
            name=name,
        )