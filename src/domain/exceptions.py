class DomainException(Exception):
    """Base domain exceptions for comments"""
    pass


class EntityNotFound(DomainException):
    def __init__(self, entity_type: str, entity_id: str):
        super().__init__(f'Сущность не найдена: {entity_type}:{entity_id}')
        self.entity_type = entity_type
        self.entity_id = entity_id


class CommentNotFound(DomainException):
    """Comment not found"""

    def __init__(self, comment_id):
        self.comment_id = comment_id
        super().__init__(f'Комментарий не найден: {comment_id}')


class EntityAlreadyExists(DomainException):
    pass


class ValidationError(DomainException):
    pass


class CommentValidationError(DomainException):
    pass
