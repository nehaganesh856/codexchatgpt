
from typing import Any, Dict, Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.db.repositories.project import ProjectRepository


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/deploy",
    tags=["Deployment"],
)


# ============================================================
# DEPENDENCY
# ============================================================

def get_project_repository(
    db: Session = Depends(get_db),
) -> ProjectRepository:
    """
    Create a ProjectRepository using the active database session.
    """

    return ProjectRepository(db)


# ============================================================
# GET DEPLOYMENT STATUS
# ============================================================

@router.get(
    "/status",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
)
async def get_deployment_status(
    project_id: int = Query(
        ...,
        description="Project ID",
    ),
    repository: ProjectRepository = Depends(
        get_project_repository
    ),
):
    """
    Get the current deployment status of a project.
    """

    project = await repository.get_by_id(
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return {
        "project_id": project.id,
        "project_name": project.name,
        "status": project.status.value
        if hasattr(project.status, "value")
        else project.status,
        "is_public": project.is_public,
        "is_archived": project.is_archived,
        "message": "Deployment status retrieved successfully",
    }


# ============================================================
# DEPLOY PROJECT
# ============================================================

@router.post(
    "/",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
)
async def deploy_project(
    project_id: int = Query(
        ...,
        description="Project ID",
    ),
    repository: ProjectRepository = Depends(
        get_project_repository
    ),
):
    """
    Deploy a project.

    This endpoint currently performs the deployment preparation
    and marks the project as public.

    Actual cloud deployment can be connected later.
    """

    project = await repository.get_by_id(
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    # --------------------------------------------------------
    # Validate project files
    # --------------------------------------------------------

    files = project.files or {}

    if not isinstance(files, dict) or len(files) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project has no files to deploy",
        )

    # --------------------------------------------------------
    # Update deployment state
    # --------------------------------------------------------

    updated_project = await repository.update(
        project_id,
        {
            "is_public": True,
        },
    )

    return {
        "message": "Project deployment prepared successfully",
        "project_id": updated_project.id,
        "project_name": updated_project.name,
        "is_public": updated_project.is_public,
        "file_count": len(files),
        "deployment_status": "ready",
    }


# ============================================================
# UNDEPLOY PROJECT
# ============================================================

@router.post(
    "/undeploy",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
)
async def undeploy_project(
    project_id: int = Query(
        ...,
        description="Project ID",
    ),
    repository: ProjectRepository = Depends(
        get_project_repository
    ),
):
    """
    Remove a project from public deployment.
    """

    project = await repository.get_by_id(
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    updated_project = await repository.update(
        project_id,
        {
            "is_public": False,
        },
    )

    return {
        "message": "Project undeployed successfully",
        "project_id": updated_project.id,
        "project_name": updated_project.name,
        "is_public": updated_project.is_public,
        "deployment_status": "offline",
    }


# ============================================================
# PUBLISH PROJECT
# ============================================================

@router.post(
    "/publish",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
)
async def publish_project(
    project_id: int = Query(
        ...,
        description="Project ID",
    ),
    repository: ProjectRepository = Depends(
        get_project_repository
    ),
):
    """
    Publish a project.

    Publishing makes the project publicly accessible.
    """

    project = await repository.get_by_id(
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    updated_project = await repository.update(
        project_id,
        {
            "is_public": True,
            "is_archived": False,
        },
    )

    return {
        "message": "Project published successfully",
        "project_id": updated_project.id,
        "project_name": updated_project.name,
        "is_public": updated_project.is_public,
    }


# ============================================================
# UNPUBLISH PROJECT
# ============================================================

@router.post(
    "/unpublish",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
)
async def unpublish_project(
    project_id: int = Query(
        ...,
        description="Project ID",
    ),
    repository: ProjectRepository = Depends(
        get_project_repository
    ),
):
    """
    Unpublish a project.

    The project remains in the database but is no longer public.
    """

    project = await repository.get_by_id(
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    updated_project = await repository.update(
        project_id,
        {
            "is_public": False,
        },
    )

    return {
        "message": "Project unpublished successfully",
        "project_id": updated_project.id,
        "project_name": updated_project.name,
        "is_public": updated_project.is_public,
    }
