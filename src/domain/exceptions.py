class DomainException(Exception):
    pass


class EntityNotFound(DomainException):
    pass


class EntityAlreadyExists(DomainException):
    pass


class ValidationError(DomainException):
    pass

