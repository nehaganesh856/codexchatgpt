
from typing import Any, Dict

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from fastapi.responses import Response
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.db.repositories.project import ProjectRepository


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/export",
    tags=["Export"],
)


# ============================================================
# DEPENDENCY
# ============================================================

def get_project_repository(
    db: Session = Depends(get_db),
) -> ProjectRepository:
    """
    Create a ProjectRepository using the active
    SQLAlchemy database session.
    """

    return ProjectRepository(db)


# ============================================================
# GET PROJECT EXPORT DATA
# ============================================================

@router.get(
    "/",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
)
async def export_project(
    project_id: int = Query(
        ...,
        description="Project ID",
    ),
    repository: ProjectRepository = Depends(
        get_project_repository
    ),
):
    """
    Export project information and generated files.

    Returns the complete project metadata and
    all files stored in the Project.files JSON field.
    """

    # --------------------------------------------------------
    # GET PROJECT
    # --------------------------------------------------------

    project = await repository.get_by_id(
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    # --------------------------------------------------------
    # GET FILES
    # --------------------------------------------------------

    files = project.files or {}

    if not isinstance(files, dict):
        files = {}

    # --------------------------------------------------------
    # RETURN EXPORT DATA
    # --------------------------------------------------------

    return {
        "project": {
            "id": project.id,
            "user_id": project.user_id,
            "name": project.name,
            "description": project.description,
            "idea": project.idea,
            "slug": project.slug,
            "status": (
                project.status.value
                if hasattr(project.status, "value")
                else project.status
            ),
            "framework": (
                project.framework.value
                if hasattr(project.framework, "value")
                else project.framework
            ),
            "template_type": project.template_type,
            "total_files": project.total_files,
            "total_size": project.total_size,
            "code_lines": project.code_lines,
            "is_public": project.is_public,
            "is_archived": project.is_archived,
            "tags": project.tags or [],
            "created_at": (
                project.created_at.isoformat()
                if project.created_at
                else None
            ),
            "updated_at": (
                project.updated_at.isoformat()
                if project.updated_at
                else None
            ),
            "completed_at": (
                project.completed_at.isoformat()
                if project.completed_at
                else None
            ),
        },
        "files": files,
        "file_count": len(files),
        "message": "Project exported successfully",
    }


# ============================================================
# EXPORT PROJECT FILES
# ============================================================

@router.get(
    "/files",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
)
async def export_project_files(
    project_id: int = Query(
        ...,
        description="Project ID",
    ),
    repository: ProjectRepository = Depends(
        get_project_repository
    ),
):
    """
    Export only the generated project files.
    """

    project = await repository.get_by_id(
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    files = project.files or {}

    if not isinstance(files, dict):
        files = {}

    return {
        "project_id": project.id,
        "project_name": project.name,
        "files": files,
        "file_count": len(files),
    }


# ============================================================
# GET SINGLE FILE FOR EXPORT
# ============================================================

@router.get(
    "/file",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
)
async def export_single_file(
    project_id: int = Query(
        ...,
        description="Project ID",
    ),
    file_name: str = Query(
        ...,
        description="File path or file name",
    ),
    repository: ProjectRepository = Depends(
        get_project_repository
    ),
):
    """
    Export a single file from a project.
    """

    project = await repository.get_by_id(
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    files = project.files or {}

    if not isinstance(files, dict):
        files = {}

    if file_name not in files:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File '{file_name}' not found",
        )

    return {
        "project_id": project.id,
        "project_name": project.name,
        "file_name": file_name,
        "content": files[file_name],
    }


# ============================================================
# DOWNLOAD SINGLE FILE
# ============================================================

@router.get(
    "/download",
    status_code=status.HTTP_200_OK,
)
async def download_file(
    project_id: int = Query(
        ...,
        description="Project ID",
    ),
    file_name: str = Query(
        ...,
        description="File name",
    ),
    repository: ProjectRepository = Depends(
        get_project_repository
    ),
):
    """
    Download a single project file.

    The file content is returned as a downloadable response.
    """

    project = await repository.get_by_id(
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    files = project.files or {}

    if not isinstance(files, dict):
        files = {}

    if file_name not in files:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File '{file_name}' not found",
        )

    content = files[file_name]

    if content is None:
        content = ""

    if not isinstance(content, str):
        content = str(content)

    # --------------------------------------------------------
    # SAFE DOWNLOAD FILE NAME
    # --------------------------------------------------------

    download_name = file_name.replace(
        "\\",
        "/",
    ).split("/")[-1]

    if not download_name:
        download_name = "download.txt"

    # --------------------------------------------------------
    # RETURN DOWNLOAD
    # --------------------------------------------------------

    return Response(
        content=content,
        media_type="text/plain",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{download_name}"'
            )
        },
    )

