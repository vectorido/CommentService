from typing import Dict, Optional, List
from asyncpg import Pool

from src.domain.entities.comment import Comment


class PostgresCommentRepository:

    def __init__(self, pool: Pool):
        self.pool = pool

    async def create(self, comment: Dict) -> Dict:
        query = """
        INSERT INTO comments (id, entity_type, entity_id, author_id, text, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING *
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                comment["id"],
                comment["entity_type"],
                comment["entity_id"],
                comment["author_id"],
                comment["text"],
                comment["created_at"],
                comment["updated_at"],
            )
        return dict(row)

    async def get_by_id(self, comment_id: str) -> Optional[Comment]:
        query = """
        SELECT id, entity_type, entity_id, author_id, text, created_at, updated_at
        FROM comments
        WHERE id = $1
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, comment_id)
        return self._map_row_to_comment(row)

    async def get_by_entity(
            self,
            entity_type: str,
            entity_id: str
    ) -> List[Comment]:
        query = """
        SELECT id, entity_type, entity_id, author_id, text, created_at, updated_at
        FROM comments
        WHERE entity_type = $1 AND entity_id = $2
        ORDER BY created_at ASC
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, entity_type, entity_id)
        return [self._map_row_to_comment(row) for row in rows]

    async def update(self, comment: Comment) -> Comment:
        query = """
        UPDATE comments
        SET text = $1, updated_at = $2
        WHERE id = $3
        RETURNING *
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, comment.text, comment.updated_at, comment.id)
        return self._map_row_to_comment(row)

    @staticmethod
    def _map_row_to_comment(row) -> Optional[Comment]:
        if not row:
            return None
        return Comment(
            id=row['id'],
            entity_type=row['entity_type'],
            entity_id=row['entity_id'],
            author_id=row['author_id'],
            text=row['text'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
