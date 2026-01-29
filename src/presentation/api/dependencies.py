from src.application.use_cases.user_use_cases import (
    CreateUserUseCase,
    GetUserUseCase,
    GetAllUsersUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase,
)
from src.infrastructure.database.connection import db_connection
from src.infrastructure.repositories.postgres_user_repository import PostgresUserRepository


def get_user_repository():
    return PostgresUserRepository(db_connection)


def get_create_user_use_case():
    return CreateUserUseCase(get_user_repository())


def get_get_user_use_case():
    return GetUserUseCase(get_user_repository())


def get_get_all_users_use_case():
    return GetAllUsersUseCase(get_user_repository())


def get_update_user_use_case():
    return UpdateUserUseCase(get_user_repository())


def get_delete_user_use_case():
    return DeleteUserUseCase(get_user_repository())

