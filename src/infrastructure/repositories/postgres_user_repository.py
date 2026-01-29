from typing import List, Optional

from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.database.connection import DatabaseConnection


class PostgresUserRepository(UserRepository):
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def _map_row_to_user(self, row) -> User:
        if not row:
            return None
        return User(
            id=row['id'],
            email=row['email'],
            name=row['name'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
    
    async def create(self, user: User) -> User:
        row = await self.db.fetchrow(
            """
            insert into users (email, name)
            values ($1, $2)
            returning id, email, name, created_at, updated_at
            """,
            user.email, user.name
        )
        return self._map_row_to_user(row)
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        row = await self.db.fetchrow(
            """
            select id, email, name, created_at, updated_at
            from users
            where id = $1
            """,
            user_id
        )
        return self._map_row_to_user(row)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        row = await self.db.fetchrow(
            """
            select id, email, name, created_at, updated_at
            from users
            where email = $1
            """,
            email.lower()
        )
        return self._map_row_to_user(row)
    
    async def get_all(self, limit: int = 100, offset: int = 0) -> List[User]:
        rows = await self.db.fetch(
            """
            select id, email, name, created_at, updated_at
            from users
            order by id
            limit $1 offset $2
            """,
            limit, offset
        )
        return [self._map_row_to_user(row) for row in rows]
    
    async def update(self, user: User) -> Optional[User]:
        row = await self.db.fetchrow(
            """
            update users
            set email = $1, name = $2, updated_at = current_timestamp
            where id = $3
            returning id, email, name, created_at, updated_at
            """,
            user.email, user.name, user.id
        )
        return self._map_row_to_user(row)
    
    async def delete(self, user_id: int) -> bool:
        result = await self.db.execute(
            """
            delete from users
            where id = $1
            """,
            user_id
        )
        return result == "DELETE 1"

