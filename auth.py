
from typing import Tuple

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from backend.core.validation import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    RefreshTokenRequest,
)

from backend.core.security import (
    SecurityService,
    get_current_user,
)

from backend.core.logging import Logger
from backend.config.settings import get_settings

from backend.db.session import SessionLocal, get_db
from backend.db.repositories.user import UserRepository


# ============================================================
# INITIALIZATION
# ============================================================

logger = Logger(__name__)
settings = get_settings()


# ============================================================
# AUTHENTICATION SERVICE
# ============================================================

class AuthService:
    """
    Authentication service.

    Handles:
    - User registration
    - User login
    - Password hashing
    - Password verification
    - JWT access token generation
    """

    # ========================================================
    # REGISTER USER
    # ========================================================

    @staticmethod
    async def register(
        db: Session,
        email: str,
        password: str,
        name: str,
    ) -> Tuple[object, str]:
        """
        Register a new user.

        Returns:
            user, access_token
        """

        # ----------------------------------------------------
        # Clean input
        # ----------------------------------------------------

        email = email.strip().lower()
        name = name.strip()

        # ----------------------------------------------------
        # Validate email
        # ----------------------------------------------------

        if not email:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is required",
            )

        # ----------------------------------------------------
        # Validate name
        # ----------------------------------------------------

        if not name:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Name is required",
            )

        # ----------------------------------------------------
        # Validate password
        # ----------------------------------------------------

        if not password:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password is required",
            )

        if len(password) < 6:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Password must contain "
                    "at least 6 characters"
                ),
            )

        # ----------------------------------------------------
        # Create repository
        # ----------------------------------------------------

        repo = UserRepository(db)

        # ----------------------------------------------------
        # Check existing user
        # ----------------------------------------------------

        existing_user = await repo.get_by_email(
            email
        )

        if existing_user:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "A user with this email "
                    "already exists"
                ),
            )

        # ----------------------------------------------------
        # Hash password
        # ----------------------------------------------------

        hashed_password = (
            SecurityService.hash_password(
                password
            )
        )

        # ----------------------------------------------------
        # Create user
        # ----------------------------------------------------

        user = await repo.create_user(
            email=email,
            name=name,
            hashed_password=hashed_password,
        )

        # ----------------------------------------------------
        # Get role
        # ----------------------------------------------------

        role = user.role

        if hasattr(
            role,
            "value",
        ):

            role = role.value

        # ----------------------------------------------------
        # Create access token
        # ----------------------------------------------------

        access_token = (
            SecurityService.create_access_token(
                {
                    "sub": str(user.id),
                    "email": user.email,
                    "role": role,
                }
            )
        )

        return user, access_token

    # ========================================================
    # LOGIN USER
    # ========================================================

    @staticmethod
    async def login(
        db: Session,
        email: str,
        password: str,
    ) -> Tuple[object, str]:
        """
        Authenticate an existing user.

        Returns:
            user, access_token
        """

        # ----------------------------------------------------
        # Clean email
        # ----------------------------------------------------

        email = email.strip().lower()

        # ----------------------------------------------------
        # Create repository
        # ----------------------------------------------------

        repo = UserRepository(db)

        # ----------------------------------------------------
        # Find user
        # ----------------------------------------------------

        user = await repo.get_by_email(
            email
        )

        if not user:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )

        # ----------------------------------------------------
        # Check active status
        # ----------------------------------------------------

        if not user.is_active:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        # ----------------------------------------------------
        # Verify password
        # ----------------------------------------------------

        password_valid = (
            SecurityService.verify_password(
                password,
                user.hashed_password,
            )
        )

        if not password_valid:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )

        # ----------------------------------------------------
        # Update last login
        # ----------------------------------------------------

        await repo.update_last_login(
            user.id
        )

        # ----------------------------------------------------
        # Get role
        # ----------------------------------------------------

        role = user.role

        if hasattr(
            role,
            "value",
        ):

            role = role.value

        # ----------------------------------------------------
        # Create access token
        # ----------------------------------------------------

        access_token = (
            SecurityService.create_access_token(
                {
                    "sub": str(user.id),
                    "email": user.email,
                    "role": role,
                }
            )
        )

        return user, access_token


# ============================================================
# FASTAPI ROUTER
# ============================================================

router = APIRouter(
    tags=["Authentication"],
)


# ============================================================
# DATABASE DEPENDENCY
# ============================================================

def get_db():
    """
    Create a database session for each request.
    """

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# ============================================================
# TEST AUTH ROUTE
# ============================================================

@router.get(
    "/test"
)
async def test():

    return {
        "success": True,
        "message": "Auth route working",
    }


# ============================================================
# REGISTER ROUTE
# ============================================================

@router.post(
    "/register",
    response_model=TokenResponse,
)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):

    try:

        # ----------------------------------------------------
        # Register user
        # ----------------------------------------------------

        user, access_token = (
            await AuthService.register(
                db=db,
                email=request.email,
                password=request.password,
                name=request.name,
            )
        )

        # ----------------------------------------------------
        # Create refresh token
        # ----------------------------------------------------

        refresh_token = (
            SecurityService.create_refresh_token(
                {
                    "sub": str(user.id),
                }
            )
        )

        # ----------------------------------------------------
        # Return token response
        # ----------------------------------------------------

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
            email=user.email,
            expires_in=(
                settings.access_token_expire_minutes
                * 60
            ),
        )

    except HTTPException:

        raise

    except Exception as e:

        logger.error(
            "Registration failed",
            error=str(e),
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# ============================================================
# LOGIN ROUTE
# ============================================================

@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):

    try:

        # ----------------------------------------------------
        # Login user
        # ----------------------------------------------------

        user, access_token = (
            await AuthService.login(
                db=db,
                email=request.email,
                password=request.password,
            )
        )

        # ----------------------------------------------------
        # Create refresh token
        # ----------------------------------------------------

        refresh_token = (
            SecurityService.create_refresh_token(
                {
                    "sub": str(user.id),
                }
            )
        )

        # ----------------------------------------------------
        # Return token response
        # ----------------------------------------------------

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
            email=user.email,
            expires_in=(
                settings.access_token_expire_minutes
                * 60
            ),
        )

    except HTTPException:

        raise

    except Exception as e:

        logger.error(
            "Login failed",
            error=str(e),
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )


# ============================================================
# REFRESH TOKEN ROUTE
# ============================================================

@router.post(
    "/refresh",
    response_model=TokenResponse,
)
async def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):

    try:

        # ----------------------------------------------------
        # Decode token
        # ----------------------------------------------------

        payload = (
            SecurityService.decode_token(
                request.refresh_token
            )
        )

        # ----------------------------------------------------
        # Verify token type
        # ----------------------------------------------------

        if payload.get("type") != "refresh":

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        # ----------------------------------------------------
        # Get user ID
        # ----------------------------------------------------

        user_id = payload.get(
            "sub"
        )

        if user_id is None:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=(
                    "Invalid refresh "
                    "token claims"
                ),
            )

        # ----------------------------------------------------
        # Find user
        # ----------------------------------------------------

        repo = UserRepository(
            db
        )

        user = await repo.get_by_id(
            int(user_id)
        )

        if not user:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        # ----------------------------------------------------
        # Create new access token
        # ----------------------------------------------------

        access_token = (
            SecurityService.create_access_token(
                {
                    "sub": str(user.id),
                    "email": user.email,
                }
            )
        )

        # ----------------------------------------------------
        # Create new refresh token
        # ----------------------------------------------------

        new_refresh_token = (
            SecurityService.create_refresh_token(
                {
                    "sub": str(user.id),
                }
            )
        )

        # ----------------------------------------------------
        # Return response
        # ----------------------------------------------------

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            user_id=user.id,
            email=user.email,
            expires_in=(
                settings.access_token_expire_minutes
                * 60
            ),
        )

    except HTTPException:

        raise

    except Exception as e:

        logger.error(
            "Token refresh failed",
            error=str(e),
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(
                "Invalid or expired "
                "refresh token"
            ),
        )


# ============================================================
# CURRENT USER ROUTE
# ============================================================

@router.get(
    "/me"
)
async def get_me(
    user_id: int = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    ),
):

    try:

        # ----------------------------------------------------
        # Find user
        # ----------------------------------------------------

        repo = UserRepository(
            db
        )

        user = await repo.get_by_id(
            user_id
        )

        if not user:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        # ----------------------------------------------------
        # Convert role enum to string
        # ----------------------------------------------------

        role = user.role

        if hasattr(
            role,
            "value",
        ):

            role = role.value

        # ----------------------------------------------------
        # Return user data
        # ----------------------------------------------------

        return {
            "success": True,
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": role,
            "is_active": user.is_active,
            "email_verified": user.email_verified,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "last_login": user.last_login,
        }

    except HTTPException:

        raise

    except Exception as e:

        logger.error(
            "Failed to get current user",
            error=str(e),
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "Failed to retrieve "
                "user information"
            ),
        )


# ============================================================
# EXPORTS
# ============================================================

__all__ = [
    "router",
    "AuthService",
    "get_db",
]

