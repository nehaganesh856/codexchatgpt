from typing import Optional

from sqlalchemy.orm import Session

from backend.db.models.user import User


class UserRepository:
    """
    Repository for User database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        """
        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.
        """
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    async def create_user(
        self,
        *,
        email: str,
        name: str,
        hashed_password: str,
    ) -> User:
        """
        Create a new user.

        NOTE:
        hashed_password MUST already be hashed.
        DO NOT hash it again here.
        """

        user = User(
            email=email,
            name=name,
            hashed_password=hashed_password,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    async def update(self, user: User) -> User:
        """
        Update user.
        """
        self.db.commit()
        self.db.refresh(user)
        return user

    async def delete(self, user: User):
        """
        Delete user.
        """
        self.db.delete(user)
        self.db.commit()

    async def update_last_login(self, user_id: int):
        """
        Update last login timestamp using user ID.
        """
        from datetime import datetime

        user = (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if user:
            user.last_login = datetime.utcnow()

            self.db.commit()
            self.db.refresh(user)

        return user

    async def email_exists(self, email: str) -> bool:
        """
        Check whether an email already exists.
        """
        user = (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

        return user is not None