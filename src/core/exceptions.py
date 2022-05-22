from fastapi import HTTPException, status


class APIError(Exception):
    pass


class AlreadyExists(APIError):
    pass


class PasswordMismatch(APIError):
    pass


class AuthError(APIError):
    pass


class InvalidCredentials(AuthError):
    pass


class InvalidJWTUser(AuthError):
    pass


class InvalidUser(AuthError):
    pass


class InvalidRecipe(AuthError):
    pass
