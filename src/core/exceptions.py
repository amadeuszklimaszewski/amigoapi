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


auth_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials."
)
invalid_jwt_user_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="No user matches given token."
)
