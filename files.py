
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.db.repositories.project import ProjectRepository


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/files",
    tags=["Files"],
)


# ============================================================
# DEPENDENCIES
# ============================================================

def get_project_repository(
    db: Session = Depends(get_db),
) -> ProjectRepository:
    """
    Create a ProjectRepository using the current database session.
    """
    return ProjectRepository(db)


# ============================================================
# LIST PROJECT FILES
# ============================================================

@router.get(
    "/",
    response_model=List[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
)
async def list_files(
    project_id: int = Query(
        ...,
        description="Project ID",
    ),
    repository: ProjectRepository = Depends(
        get_project_repository
    ),
):
    """
    Get all files belonging to a project.
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
        return []

    return [
        {
            "name": file_name,
            "content": file_content,
        }
        for file_name, file_content in files.items()
    ]


# ============================================================
# GET SINGLE FILE
# ============================================================

@router.get(
    "/{file_name:path}",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
)
async def get_file(
    file_name: str,
    project_id: int = Query(
        ...,
        description="Project ID",
    ),
    repository: ProjectRepository = Depends(
        get_project_repository
    ),
):
    """
    Get a specific file from a project.
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

    if file_name not in files:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File '{file_name}' not found",
        )

    return {
        "name": file_name,
        "content": files[file_name],
    }


# ============================================================
# CREATE OR UPDATE FILE
# ============================================================

@router.post(
    "/",
    response_model=Dict[str, Any],
    status_code=status.HTTP_201_CREATED,
)
async def create_file(
    project_id: int = Query(
        ...,
        description="Project ID",
    ),
    file_name: str = Query(
        ...,
        description="File name",
    ),
    content: str = Query(
        "",
        description="File content",
    ),
    repository: ProjectRepository = Depends(
        get_project_repository
    ),
):
    """
    Create a new file or update an existing file.
    """

    project = await repository.get_by_id(
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    files = dict(
        project.files or {}
    )

    files[file_name] = content

    await repository.update(
        project_id,
        {
            "files": files,
            "total_files": len(files),
        },
    )

    return {
        "message": "File saved successfully",
        "name": file_name,
        "content": content,
    }


# ============================================================
# DELETE FILE
# ============================================================

@router.delete(
    "/{file_name:path}",
    status_code=status.HTTP_200_OK,
)
async def delete_file(
    file_name: str,
    project_id: int = Query(
        ...,
        description="Project ID",
    ),
    repository: ProjectRepository = Depends(
        get_project_repository
    ),
):
    """
    Delete a file from a project.
    """

    project = await repository.get_by_id(
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    files = dict(
        project.files or {}
    )

    if file_name not in files:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File '{file_name}' not found",
        )

    del files[file_name]

    await repository.update(
        project_id,
        {
            "files": files,
            "total_files": len(files),
        },
    )

    return {
        "message": "File deleted successfully",
        "name": file_name,
    }

