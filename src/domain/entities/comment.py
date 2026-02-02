# src/domain/entities/comment.py
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Comment:
    id: str
    entity_type: str
    entity_id: str
    author_id: str
    text: str
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        # Валидация текста при создании
        self._validate_text(self.text)

    def update_text(self, new_text: str):
        """
        Обновляет текст комментария и время обновления
        """
        self._validate_text(new_text)
        self.text = new_text
        self.updated_at = datetime.utcnow()

    @staticmethod
    def _validate_text(text: str):
        if not text.strip():
            raise ValueError("Comment text cannot be empty")
