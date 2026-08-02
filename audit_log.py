from datetime import datetime
import enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship

from backend.db.base import Base


class AuditAction(str, enum.Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    DEPLOY = "deploy"
    DOWNLOAD = "download"
    SHARE = "share"
    LOGIN = "login"
    LOGOUT = "logout"


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    action = Column(
        SQLEnum(AuditAction),
        nullable=False,
    )

    resource_type = Column(
        String(50),
        nullable=False,
    )

    resource_id = Column(
        Integer,
        nullable=True,
    )

    description = Column(
        Text,
        nullable=True,
    )

    ip_address = Column(
        String(45),
        nullable=True,
    )

    user_agent = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # Relationships

    user = relationship(
        "User",
        back_populates="audit_logs",
    )

    project = relationship(
        "Project",
        back_populates="audit_logs",
    )

    def __repr__(self):
        return (
            f"<AuditLog(id={self.id}, "
            f"action={self.action.value}, "
            f"user={self.user_id})>"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "project_id": self.project_id,
            "action": self.action.value,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "description": self.description,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "created_at": self.created_at.isoformat()
            if self.created_at
            else None,
        }