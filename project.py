
from typing import List, Optional

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from backend.db.models.project import Project
from backend.db.repositories.base import BaseRepository
import backend.db.repositories.base as base_module

print(base_module.__file__)

class ProjectRepository(BaseRepository[Project]):
    """
    Repository for managing Project database operations.
    """

    def __init__(self, session: Session):
        """
        Initialize the ProjectRepository.

        Args:
            session: SQLAlchemy database session.
        """
        super().__init__(session, Project)

    async def get_user_projects(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Project]:
        """
        Get all projects belonging to a specific user.

        Args:
            user_id: ID of the project owner.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List of projects belonging to the user.
        """
        return (
            self.session.query(Project)
            .filter(Project.user_id == user_id)
            .order_by(Project.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    async def get_by_slug(
        self,
        slug: str,
    ) -> Optional[Project]:
        """
        Get a project by its unique slug.

        Args:
            slug: Project slug.

        Returns:
            Project object if found, otherwise None.
        """
        return (
            self.session.query(Project)
            .filter(Project.slug == slug)
            .first()
        )

    async def get_user_project(
        self,
        user_id: int,
        project_id: int,
    ) -> Optional[Project]:
        """
        Get a specific project belonging to a specific user.

        Args:
            user_id: ID of the project owner.
            project_id: ID of the project.

        Returns:
            Project object if found, otherwise None.
        """
        return (
            self.session.query(Project)
            .filter(
                and_(
                    Project.id == project_id,
                    Project.user_id == user_id,
                )
            )
            .first()
        )

    async def count_user_projects(
        self,
        user_id: int,
    ) -> int:
        """
        Count the number of projects belonging to a user.

        Args:
            user_id: ID of the project owner.

        Returns:
            Number of projects.
        """
        return (
            self.session.query(Project)
            .filter(Project.user_id == user_id)
            .count()
        )

    async def search_projects(
        self,
        user_id: int,
        query: str,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Project]:
        """
        Search projects belonging to a user.

        Searches in:
        - Project name
        - Project description

        Args:
            user_id: ID of the project owner.
            query: Search text.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List of matching projects.
        """
        search_query = f"%{query}%"

        return (
            self.session.query(Project)
            .filter(
                and_(
                    Project.user_id == user_id,
                    or_(
                        Project.name.ilike(search_query),
                        Project.description.ilike(search_query),
                    ),
                )
            )
            .order_by(Project.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
