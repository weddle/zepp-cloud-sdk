class ApiError(Exception):
    pass


class AuthError(ApiError):
    pass


class RateLimitError(ApiError):
    pass


class DecodeError(ApiError):
    pass
