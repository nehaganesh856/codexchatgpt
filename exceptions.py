from typing import Any, Dict, Optional


# ============================================================
# BASE APPLICATION EXCEPTION
# ============================================================

class AppException(Exception):
    """
    Base application exception.

    All custom application exceptions inherit from this class.
    """

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        error_code: str = "APP_ERROR",
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None,
    ):
        super().__init__(message)

        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        self.cause = cause

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": False,
            "status_code": self.status_code,
            "error": self.error_code,
            "message": self.message,
            "details": self.details,
        }

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"message={self.message!r}, "
            f"status_code={self.status_code}, "
            f"error_code={self.error_code!r})"
        )


# ============================================================
# VALIDATION
# ============================================================

class ValidationException(AppException):
    def __init__(
        self,
        message: str = "Validation failed",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=422,
            error_code="VALIDATION_ERROR",
            details=details,
        )


# ============================================================
# AUTHENTICATION
# ============================================================

class AuthenticationException(AppException):
    def __init__(
        self,
        message: str = "Authentication failed",
    ):
        super().__init__(
            message=message,
            status_code=401,
            error_code="AUTHENTICATION_ERROR",
        )


class InvalidTokenException(AuthenticationException):
    def __init__(
        self,
        message: str = "Invalid authentication token",
    ):
        super().__init__(message)
        self.error_code = "INVALID_TOKEN"


class TokenExpiredException(AuthenticationException):
    def __init__(
        self,
        message: str = "Authentication token has expired",
    ):
        super().__init__(message)
        self.error_code = "TOKEN_EXPIRED"


# ============================================================
# AUTHORIZATION
# ============================================================

class AuthorizationException(AppException):
    def __init__(
        self,
        message: str = "Permission denied",
    ):
        super().__init__(
            message=message,
            status_code=403,
            error_code="AUTHORIZATION_ERROR",
        )


# ============================================================
# NOT FOUND
# ============================================================

class NotFoundException(AppException):
    def __init__(
        self,
        message: str = "Resource not found",
    ):
        super().__init__(
            message=message,
            status_code=404,
            error_code="NOT_FOUND",
        )


class ResourceNotFoundException(NotFoundException):
    def __init__(
        self,
        resource: str,
        resource_id: Any,
    ):
        self.resource = resource
        self.resource_id = resource_id

        super().__init__(
            message=f"{resource} with ID '{resource_id}' not found"
        )

        self.error_code = "RESOURCE_NOT_FOUND"


# ============================================================
# CONFLICT
# ============================================================

class ConflictException(AppException):
    def __init__(
        self,
        message: str = "Resource conflict",
    ):
        super().__init__(
            message=message,
            status_code=409,
            error_code="CONFLICT",
        )


class DuplicateResourceException(ConflictException):
    def __init__(
        self,
        resource: str = "Resource",
        field: Optional[str] = None,
        value: Any = None,
    ):
        self.resource = resource
        self.field = field
        self.value = value

        if field is not None and value is not None:
            message = f"{resource} with {field} '{value}' already exists"
        else:
            message = f"{resource} already exists"

        super().__init__(message)

        self.error_code = "DUPLICATE_RESOURCE"


# ============================================================
# BAD REQUEST
# ============================================================

class BadRequestException(AppException):
    def __init__(
        self,
        message: str = "Bad request",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=400,
            error_code="BAD_REQUEST",
            details=details,
        )


# ============================================================
# RATE LIMIT
# ============================================================

class RateLimitException(AppException):
    def __init__(
        self,
        message: str = "Rate limit exceeded",
    ):
        super().__init__(
            message=message,
            status_code=429,
            error_code="RATE_LIMIT_EXCEEDED",
        )


# ============================================================
# SERVICE UNAVAILABLE
# ============================================================

class ServiceUnavailableException(AppException):
    def __init__(
        self,
        message: str = "Service temporarily unavailable",
    ):
        super().__init__(
            message=message,
            status_code=503,
            error_code="SERVICE_UNAVAILABLE",
        )


# ============================================================
# INTERNAL SERVER
# ============================================================

class InternalServerException(AppException):
    def __init__(
        self,
        message: str = "Internal server error",
        cause: Optional[Exception] = None,
    ):
        super().__init__(
            message=message,
            status_code=500,
            error_code="INTERNAL_SERVER_ERROR",
            cause=cause,
        )


# ============================================================
# EXPORTS
# ============================================================

__all__ = [
    "AppException",
    "ValidationException",
    "AuthenticationException",
    "InvalidTokenException",
    "TokenExpiredException",
    "AuthorizationException",
    "NotFoundException",
    "ResourceNotFoundException",
    "ConflictException",
    "DuplicateResourceException",
    "BadRequestException",
    "RateLimitException",
    "ServiceUnavailableException",
    "InternalServerException",
]