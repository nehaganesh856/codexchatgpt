from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Text,
    ForeignKey,
    Integer,
    Index,
)
from sqlalchemy.orm import relationship

from backend.db.base import Base


class FileVersion(Base):
    """
    Stores every version of every file in a project.
    """

    __tablename__ = "file_versions"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    version_id = Column(
        Integer,
        ForeignKey("versions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # File Information
    file_path = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)

    # Content
    content = Column(Text, nullable=False)
    size = Column(Integer, nullable=False)
    checksum = Column(String(64), nullable=False)

    # Timestamp
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )

    # Relationships
    project = relationship(
        "Project",
        back_populates="file_versions",
    )

    version = relationship(
        "Version",
        back_populates="file_versions",
    )

    __table_args__ = (
        Index(
            "idx_project_version_created",
            "project_id",
            "version_id",
            "created_at",
        ),
    )

    def __repr__(self):
        return (
            f"<FileVersion(id={self.id}, "
            f"file='{self.file_name}', "
            f"version={self.version_id})>"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "version_id": self.version_id,
            "file_path": self.file_path,
            "file_name": self.file_name,
            "file_type": self.file_type,
            "size": self.size,
            "checksum": self.checksum,
            "created_at": self.created_at.isoformat()
            if self.created_at
            else None,
        }

    def to_detailed_dict(self):
        data = self.to_dict()
        data["content"] = self.content
        return data