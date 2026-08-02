
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from backend.config.settings import get_settings
from backend.core.exceptions import (
    InvalidTokenException,
    TokenExpiredException,
)
from backend.core.logging import Logger


# ============================================================
# INITIALIZATION
# ============================================================

logger = Logger(__name__)
settings = get_settings()


# ============================================================
# PASSWORD SECURITY
# ============================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


# ============================================================
# HTTP BEARER AUTHENTICATION
# ============================================================

security = HTTPBearer()


# ============================================================
# SECURITY SERVICE
# ============================================================

class SecurityService:
    """
    Handle authentication, password hashing,
    JWT access tokens, and refresh tokens.
    """

    # --------------------------------------------------------
    # PASSWORD HASHING
    # --------------------------------------------------------

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a plain-text password using bcrypt.
        """
        return pwd_context.hash(password)

    # --------------------------------------------------------
    # PASSWORD VERIFICATION
    # --------------------------------------------------------

    @staticmethod
    def verify_password(
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        """
        Verify a plain-text password against
        a previously hashed password.
        """
        return pwd_context.verify(
            plain_password,
            hashed_password,
        )

    # --------------------------------------------------------
    # CREATE ACCESS TOKEN
    # --------------------------------------------------------

    @staticmethod
    def create_access_token(
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        """
        Create a JWT access token.
        """

        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=settings.access_token_expire_minutes
            )

        to_encode.update(
            {
                "exp": expire,
                "type": "access",
            }
        )

        encoded_jwt = jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=settings.algorithm,
        )

        return encoded_jwt

    # --------------------------------------------------------
    # CREATE REFRESH TOKEN
    # --------------------------------------------------------

    @staticmethod
    def create_refresh_token(
        data: Dict[str, Any],
    ) -> str:
        """
        Create a JWT refresh token.
        """

        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.refresh_token_expire_days
        )

        to_encode.update(
            {
                "exp": expire,
                "type": "refresh",
            }
        )

        encoded_jwt = jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=settings.algorithm,
        )

        return encoded_jwt

    # --------------------------------------------------------
    # DECODE TOKEN
    # --------------------------------------------------------

    @staticmethod
    def decode_token(
        token: str,
    ) -> Dict[str, Any]:
        """
        Decode and validate a JWT token.
        """

        try:
            payload = jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.algorithm],
            )

            return payload

        except jwt.ExpiredSignatureError:
            logger.error(
                "Token expired",
                token=token[:10],
            )

            raise TokenExpiredException()

        except jwt.InvalidTokenError as e:
            logger.error(
                "Invalid token",
                error=str(e),
            )

            raise InvalidTokenException()


# ============================================================
# GET CURRENT USER
# ============================================================

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    FastAPI dependency to get the currently authenticated user.

    The JWT token is received through:
        Authorization: Bearer <token>
    """

    token = credentials.credentials

    try:
        # Decode JWT token
        payload = SecurityService.decode_token(token)

        # Get user ID from "sub" claim
        user_id = payload.get("sub")

        if user_id is None:
            raise InvalidTokenException(
                "Invalid token claims"
            )

        # Convert user ID to integer
        return int(user_id)

    except (
        InvalidTokenException,
        TokenExpiredException,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    except Exception as e:
        logger.error(
            "Authentication failed",
            error=str(e),
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )


# ============================================================
# GET CURRENT ADMIN
# ============================================================

async def get_current_admin(
    user_id: int = Depends(get_current_user),
):
    """
    FastAPI dependency to verify that the current user
    has administrator privileges.
    """

    # Import here to avoid circular import problems
    from db.repositories.user import UserRepository

    user = await UserRepository.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not found",
        )

    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return user
# ============================================================
# MODULE-LEVEL HELPER FUNCTIONS
# ============================================================

def hash_password(password: str) -> str:
    """
    Hash a plain-text password.
    """
    return SecurityService.hash_password(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plain-text password against its hash.
    """
    return SecurityService.verify_password(
        plain_password,
        hashed_password,
    )


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create a JWT access token.
    """
    return SecurityService.create_access_token(
        data,
        expires_delta,
    )


def create_refresh_token(
    data: Dict[str, Any],
) -> str:
    """
    Create a JWT refresh token.
    """
    return SecurityService.create_refresh_token(data)


def decode_token(
    token: str,
) -> Dict[str, Any]:
    """
    Decode and validate a JWT token.
    """
    return SecurityService.decode_token(token)