from typing import List, Optional

from src.domain.entities.user import User
from src.domain.exceptions import EntityAlreadyExists, EntityNotFound, ValidationError
from src.domain.repositories.user_repository import UserRepository


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, email: str, name: str) -> User:
        if not email or not name:
            raise ValidationError("Email and name are required")
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise EntityAlreadyExists(f"User with email {email} already exists")

        user = User(id=None, email=email, name=name)
        return await self.user_repository.create(user)


class GetUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: int) -> User:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise EntityNotFound(f"User with id {user_id} not found")
        return user


class GetAllUsersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, limit: int = 100, offset: int = 0) -> List[User]:
        return await self.user_repository.get_all(limit=limit, offset=offset)


class UpdateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: int, email: Optional[str] = None, name: Optional[str] = None) -> User:
        existing_user = await self.user_repository.get_by_id(user_id)
        if not existing_user:
            raise EntityNotFound(f"User with id {user_id} not found")

        if email:
            existing_user.email = email
        if name:
            existing_user.name = name

        updated_user = await self.user_repository.update(existing_user)
        if not updated_user:
            raise EntityNotFound(f"User with id {user_id} not found")
        return updated_user


class DeleteUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: int) -> bool:
        result = await self.user_repository.delete(user_id)
        if not result:
            raise EntityNotFound(f"User with id {user_id} not found")
        return result

