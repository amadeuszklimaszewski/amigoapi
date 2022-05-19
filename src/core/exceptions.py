class APIError(Exception):
    pass


class AlreadyExists(APIError):
    pass


class PasswordMismatch(APIError):
    pass
