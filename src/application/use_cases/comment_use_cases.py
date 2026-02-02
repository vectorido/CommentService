import logging
from datetime import datetime
from uuid import uuid4
from typing import List

from src.domain.entities.comment import Comment
from src.domain.exceptions import EntityNotFound, CommentNotFound, CommentValidationError
from src.infrastructure.repositories.postgres_comment_repository import PostgresCommentRepository

# Настройка логирования
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class CreateCommentUseCase:
    def __init__(self, repo: PostgresCommentRepository):
        self.repo = repo

    async def execute(self, entity_type: str, entity_id: str, author_id: str, text: str) -> Comment:
        """
        Создать комментарий для сущности
        """
        if not text.strip():
            raise CommentValidationError("Comment text cannot be empty")

        now = datetime.now()
        comment = Comment(
            id=str(uuid4()),
            entity_type=entity_type,
            entity_id=entity_id,
            author_id=author_id,
            text=text,
            created_at=now,
            updated_at=now
        )

        saved_comment = await self.repo.create(comment)

        # Логирование
        logger.info(
            f"Comment created | id={comment.id} | entity={entity_type}:{entity_id} | author={author_id} | time={now.isoformat()}"
        )

        return saved_comment


class GetCommentsUseCase:
    def __init__(self, repo: PostgresCommentRepository):
        self.repo = repo

    async def execute(
            self,
            entity_type: str,
            entity_id: str,
            page: int = 1,
            limit: int = 10,
            sort: str = "desc"
    ) -> List[Comment]:
        """
        Получить список комментариев для сущности с постраничной навигацией и сортировкой
        """
        comments = await self.repo.get_by_entity(entity_type, entity_id)
        if not comments:
            raise EntityNotFound(f"No comments found for entity {entity_type} with id {entity_id}")

        reverse = True if sort == "desc" else False
        comments_sorted = sorted(comments, key=lambda c: c.created_at, reverse=reverse)

        start = (page - 1) * limit
        end = start + limit
        return comments_sorted[start:end]


class UpdateCommentUseCase:
    def __init__(self, repo: PostgresCommentRepository):
        self.repo = repo

    async def execute(
            self,
            comment_id: str,
            entity_type: str,
            entity_id: str,
            new_text: str
    ) -> Comment:
        """
        Обновить текст комментария
        """
        if not new_text.strip():
            raise CommentValidationError("Comment text cannot be empty")

        comment = await self.repo.get_by_id(comment_id)
        if not comment:
            raise CommentNotFound(f"Comment with id {comment_id} not found")

        # Метод update_text теперь в сущности
        comment.update_text(new_text)

        updated_comment = await self.repo.update(comment)

        # Логирование
        logger.info(
            f"Comment updated | id={comment.id} | entity={entity_type}:{entity_id} | author={comment.author_id} | time={comment.updated_at.isoformat()}"
        )

        return updated_comment
