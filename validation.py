from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class ProjectStatus(str, Enum):
    DRAFT = "draft"
    GENERATING = "generating"
    COMPLETED = "completed"
    ERROR = "error"
    ARCHIVED = "archived"


class Framework(str, Enum):
    REACT = "react"
    NEXT = "next"
    VUE = "vue"
    SVELTE = "svelte"
    NODE = "node"
    FASTAPI = "fastapi"
    DJANGO = "django"
    EXPRESS = "express"


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("Invalid email")
        return value.lower()


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: int
    email: str
    expires_in: int


class RefreshTokenRequest(BaseModel):
    refresh_token: str

class GenerateAppRequest(BaseModel):
    name: str
    description: str
    framework: Framework = Framework.REACT


class ChatRequest(BaseModel):
    project_id: int
    message: str
    agent_type: Optional[str] = None


class FileUpdateRequest(BaseModel):
    path: str
    content: str


class VersionCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None


class DeployRequest(BaseModel):
    project_id: int
    target: str
    repository_name: Optional[str] = None
    environment: Optional[Dict[str, str]] = None


class ExportRequest(BaseModel):
    project_id: int
    format: str


class ResponseModel(BaseModel):
    status: str = "success"
    message: str = ""
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class PaginatedResponse(BaseModel):
    items: List[Dict[str, Any]]
    total: int
    page: int
    page_size: int
    total_pages: int