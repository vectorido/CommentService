import logging
from typing import List, Dict
from datetime import datetime
from uuid import uuid4

from src.domain.exceptions import EntityNotFound, CommentNotFound, CommentValidationError

# Настройка логирования
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Временное in-memory хранилище комментариев
COMMENTS_DB: Dict[str, List[Dict]] = {}


class CreateCommentUseCase:
    async def execute(self, entity_type: str, entity_id: str, author_id: str, text: str) -> Dict:
        """
        Создать комментарий для сущности
        """
        if not text.strip():
            raise CommentValidationError("Comment text cannot be empty")

        comment_id = str(uuid4())
        now = datetime.utcnow().isoformat()

        comment = {
            "id": comment_id,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "author_id": author_id,
            "text": text,
            "created_at": now,
            "updated_at": now
        }

        key = f"{entity_type}:{entity_id}"
        if key not in COMMENTS_DB:
            COMMENTS_DB[key] = []

        COMMENTS_DB[key].append(comment)

        # Логирование
        logger.info(
            f"Comment created | id={comment_id} | entity={entity_type}:{entity_id} | author={author_id} | time={now}")

        return comment


class GetCommentsUseCase:
    async def execute(
            self,
            entity_type: str,
            entity_id: str,
            page: int = 1,
            limit: int = 10,
            sort: str = "desc"
    ) -> List[Dict]:
        """
        Получить список комментариев для сущности с постраничной навигацией и сортировкой
        """
        key = f"{entity_type}:{entity_id}"
        if key not in COMMENTS_DB:
            raise EntityNotFound(f"No comments found for entity {entity_type} with id {entity_id}")

        comments = COMMENTS_DB[key]

        reverse = True if sort == "desc" else False
        comments_sorted = sorted(comments, key=lambda c: c["created_at"], reverse=reverse)

        start = (page - 1) * limit
        end = start + limit
        return comments_sorted[start:end]


class UpdateCommentUseCase:
    async def execute(
            self,
            comment_id: str,
            entity_type: str,
            entity_id: str,
            new_text: str
    ) -> Dict:
        """
        Обновить текст комментария
        """
        if not new_text.strip():
            raise CommentValidationError("Comment text cannot be empty")

        key = f"{entity_type}:{entity_id}"
        if key not in COMMENTS_DB:
            raise EntityNotFound(f"No comments found for entity {entity_type} with id {entity_id}")

        comments = COMMENTS_DB[key]
        comment = next((c for c in comments if c["id"] == comment_id), None)
        if not comment:
            raise CommentNotFound(f"Comment with id {comment_id} not found")

        comment["text"] = new_text
        comment["updated_at"] = datetime.utcnow().isoformat()

        # Логирование
        logger.info(
            f"Comment updated | id={comment_id} | entity={entity_type}:{entity_id} | author={comment['author_id']} | time={comment['updated_at']}")

        return comment
