class APIException(Exception):
    pass


class AlreadyExistsException(APIException):
    pass


class DoesNotExistException(APIException):
    pass


class PasswordMismatchException(APIException):
    pass


class AuthException(APIException):
    pass


class InvalidCredentialsException(AuthException):
    pass


class InvalidJWTUserException(AuthException):
    pass


class InvalidUserException(AuthException):
    pass


class InvalidRecipeException(AuthException):
    pass
