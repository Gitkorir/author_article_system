class DatabaseError(Exception):
    """Base exception for database operations"""
    pass

class RecordNotFound(DatabaseError):
    """Raised when a record isn't found"""
    pass

class ConstraintViolation(DatabaseError):
    """Raised when a database constraint is violated"""
    pass