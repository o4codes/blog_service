class NotFoundException(Exception):
    """
    Exception for when a resource is not found
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class DatabaseException(Exception):
    """
    Exception for when a database error occurs
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class ExistingDataException(Exception):
    """
    Exception for when a data already exists
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class BadRequest(Exception):
    """
    Exception for when a request is bad
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class UnauthorizedException(Exception):
    """
    Exception for when a user is not authorized
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message
