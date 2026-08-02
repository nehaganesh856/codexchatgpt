
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.db.models.project import Project
from backend.db.repositories.base import BaseRepository


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/versions",
    tags=["Versions"],
)


# ============================================================
# DEPENDENCIES
# ============================================================

def get_project_repository(
    db: Session = Depends(get_db),
) -> BaseRepository[Project]:
    """
    Create a project repository using the current database session.
    """
    return BaseRepository(
        db,
        Project,
    )


# ============================================================
# GET PROJECT VERSIONS
# ============================================================

@router.get(
    "/",
    response_model=List[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
)
async def list_versions(
    project_id: int = Query(
        ...,
        description="Project ID",
    ),
    repository: BaseRepository[Project] = Depends(
        get_project_repository
    ),
):
    """
    Get all versions belonging to a project.

    Note:
    This route expects the Project model to have a
    relationship named 'versions'.
    """

    project = await repository.get_by_id(
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    versions = project.versions or []

    result = []

    for version in versions:
        version_data = {
            "id": getattr(
                version,
                "id",
                None,
            ),
            "project_id": getattr(
                version,
                "project_id",
                project_id,
            ),
        }

        # Add common version fields if they exist
        if hasattr(version, "version"):
            version_data["version"] = version.version

        if hasattr(version, "name"):
            version_data["name"] = version.name

        if hasattr(version, "description"):
            version_data["description"] = version.description

        if hasattr(version, "files"):
            version_data["files"] = version.files

        if hasattr(version, "created_at"):
            version_data["created_at"] = version.created_at

        result.append(
            version_data
        )

    return result


# ============================================================
# GET SINGLE VERSION
# ============================================================

@router.get(
    "/{version_id}",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
)
async def get_version(
    version_id: int,
    project_id: int = Query(
        ...,
        description="Project ID",
    ),
    repository: BaseRepository[Project] = Depends(
        get_project_repository
    ),
):
    """
    Get a specific version belonging to a project.
    """

    project = await repository.get_by_id(
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    version = next(
        (
            item
            for item in (project.versions or [])
            if getattr(
                item,
                "id",
                None,
            ) == version_id
        ),
        None,
    )

    if version is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Version not found",
        )

    result = {
        "id": getattr(
            version,
            "id",
            None,
        ),
        "project_id": getattr(
            version,
            "project_id",
            project_id,
        ),
    }

    if hasattr(version, "version"):
        result["version"] = version.version

    if hasattr(version, "name"):
        result["name"] = version.name

    if hasattr(version, "description"):
        result["description"] = version.description

    if hasattr(version, "files"):
        result["files"] = version.files

    if hasattr(version, "created_at"):
        result["created_at"] = version.created_at

    return result


# ============================================================
# DELETE VERSION
# ============================================================

@router.delete(
    "/{version_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_version(
    version_id: int,
    project_id: int = Query(
        ...,
        description="Project ID",
    ),
    repository: BaseRepository[Project] = Depends(
        get_project_repository
    ),
):
    """
    Delete a version from a project.
    """

    project = await repository.get_by_id(
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    version = next(
        (
            item
            for item in (project.versions or [])
            if getattr(
                item,
                "id",
                None,
            ) == version_id
        ),
        None,
    )

    if version is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Version not found",
        )

    # Remove version from relationship
    project.versions.remove(
        version
    )

    # Commit changes
    repository.session.commit()

    return {
        "message": "Version deleted successfully",
        "version_id": version_id,
    }

