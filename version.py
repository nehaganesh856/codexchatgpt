from typing import List, Optional
from sqlalchemy.orm import Session

from backend.db.models.version import Version
from backend.db.repositories.base import BaseRepository

class VersionRepository(BaseRepository[Version]):
    """Version repository"""
    
    def __init__(self, session: Session):
        super().__init__(session, Version)
    
    async def get_project_versions(self, project_id: int) -> List[Version]:
        """Get all versions of a project"""
        return self.session.query(Version).filter(
            Version.project_id == project_id
        ).order_by(Version.version_number.desc()).all()
    
    async def get_latest_version(self, project_id: int) -> Optional[Version]:
        """Get latest version of a project"""
        return self.session.query(Version).filter(
            Version.project_id == project_id
        ).order_by(Version.version_number.desc()).first()
    
    async def get_next_version_number(self, project_id: int) -> int:
        """Get next version number"""
        latest = await self.get_latest_version(project_id)
        return (latest.version_number + 1) if latest else 1