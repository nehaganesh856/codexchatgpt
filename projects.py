
from typing import Any, Dict, Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    BackgroundTasks,
)

from sqlalchemy.orm import Session


# ============================================================
# CORE IMPORTS
# ============================================================

from backend.core.validation import (
    GenerateAppRequest,
)

from backend.core.security import (
    get_current_user,
    SecurityService,
)

from backend.core.logging import (
    Logger,
)


# ============================================================
# AI AND FILE SERVICES
# ============================================================

from backend.services.ai import (
    AIService,
)

from backend.services.file import (
    FileService,
)


# ============================================================
# CONFIGURATION
# ============================================================

from backend.config.settings import (
    get_settings,
)


# ============================================================
# DATABASE
# ============================================================

from backend.db.session import (
    SessionLocal,
    get_db,
)

from backend.db.models.project import (
    Project,
    ProjectStatus,
)

from backend.db.repositories.project import (
    ProjectRepository,
)


# ============================================================
# INITIALIZATION
# ============================================================

logger = Logger(
    __name__
)

settings = get_settings()


# ============================================================
# ROUTER
# ============================================================

# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    tags=["Projects"],
)


# ============================================================
# DATABASE DEPENDENCY
# ============================================================

def get_db():
    """
    Create a database session for each request.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ============================================================
# PROJECT SERVICE
# ============================================================

class ProjectService:
    """
    Service responsible for project operations.

    Handles:
    - Project creation
    - Project retrieval
    - Project ownership verification
    - Project deletion
    """


    # ========================================================
    # CREATE PROJECT
    # ========================================================

    @staticmethod
    async def create_project(
        db: Session,
        user_id: int,
        name: str,
        description: str,
        idea: str,
        framework: str,
    ):
        """
        Create a new project.
        """

        # ----------------------------------------------------
        # Validate user ID
        # ----------------------------------------------------

        if not user_id:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user",
            )

        # ----------------------------------------------------
        # Validate project name
        # ----------------------------------------------------

        if not name:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project name is required",
            )

        # ----------------------------------------------------
        # Validate idea
        # ----------------------------------------------------

        if not idea:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project idea is required",
            )

        # ----------------------------------------------------
        # Validate framework
        # ----------------------------------------------------

        if not framework:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Framework is required",
            )

        # ----------------------------------------------------
        # Create project repository
        # ----------------------------------------------------

        repo = ProjectRepository(
            db
        )

        # ----------------------------------------------------
        # Create project data
        # ----------------------------------------------------

        project_data = {
            "user_id": user_id,
            "name": name,
            "description": description,
            "idea": idea,
            "framework": framework,
            "status": ProjectStatus.GENERATING,
        }

        # ----------------------------------------------------
        # Create project
        # ----------------------------------------------------

        project = await repo.create(
            project_data
        )

        logger.info(
            "Project created",
            project_id=project.id,
            user_id=user_id,
        )

        return project


    # ========================================================
    # GET PROJECT
    # ========================================================

    @staticmethod
    async def get_project(
        db: Session,
        user_id: int,
        project_id: int,
    ):
        """
        Get a project belonging to a user.
        """

        repo = ProjectRepository(
            db
        )

        project = await repo.get_by_id(
            project_id
        )

        # ----------------------------------------------------
        # Project does not exist
        # ----------------------------------------------------

        if not project:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        # ----------------------------------------------------
        # Verify project ownership
        # ----------------------------------------------------

        if project.user_id != user_id:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this project",
            )

        return project


    # ========================================================
    # DELETE PROJECT
    # ========================================================

    @staticmethod
    async def delete_project(
        db: Session,
        user_id: int,
        project_id: int,
    ):
        """
        Delete a project belonging to a user.
        """

        # ----------------------------------------------------
        # Verify project ownership
        # ----------------------------------------------------

        project = await ProjectService.get_project(
            db,
            user_id,
            project_id,
        )

        # ----------------------------------------------------
        # Delete project
        # ----------------------------------------------------

        repo = ProjectRepository(
            db
        )

        await repo.delete(
            project_id
        )

        logger.info(
            "Project deleted",
            project_id=project_id,
            user_id=user_id,
        )

        return True


# ============================================================
# BACKGROUND APPLICATION GENERATION
# ============================================================

async def generate_app_background(
    project_id: int,
):
    """
    Generate the complete application
    in the background.
    """

    db = SessionLocal()

    try:

        # ----------------------------------------------------
        # Create repository
        # ----------------------------------------------------

        repo = ProjectRepository(
            db
        )

        # ----------------------------------------------------
        # Get project
        # ----------------------------------------------------

        project = await repo.get_by_id(
            project_id
        )

        if not project:

            logger.error(
                "Project not found",
                project_id=project_id,
            )

            return

        # ----------------------------------------------------
        # Update status to generating
        # ----------------------------------------------------

        await repo.update(
            project_id,
            {
             "status": ProjectStatus.GENERATING,
            },
        )

        # ----------------------------------------------------
        # Initialize AI service
        # ----------------------------------------------------

        ai_service = AIService()

        # ----------------------------------------------------
        # STEP 1: Generate plan
        # ----------------------------------------------------

        logger.info(
            "Generating application plan",
            project_id=project_id,
        )

        plan = await ai_service.generate_plan(
            project.idea
        )

        # ----------------------------------------------------
        # STEP 2: Generate UI specification
        # ----------------------------------------------------

        logger.info(
            "Generating UI specification",
            project_id=project_id,
        )

        ui_spec = (
            await ai_service.generate_ui_spec(
                project.idea,
                plan,
                project.framework,
            )
        )

        # ----------------------------------------------------
        # STEP 3: Generate backend specification
        # ----------------------------------------------------

        logger.info(
            "Generating backend specification",
            project_id=project_id,
        )

        backend_spec = (
            await ai_service.generate_backend_spec(
                plan,
                ui_spec,
            )
        )

        # ----------------------------------------------------
        # STEP 4: Generate application files
        # ----------------------------------------------------

        logger.info(
            "Generating application files",
            project_id=project_id,
        )

        if project.framework.lower() == "react":

            files = (
                FileService.generate_react_files(
                    {
                        "plan": plan,
                        "ui_spec": ui_spec,
                        "backend_spec": backend_spec,
                    }
                )
            )

        else:

            files = (
                FileService.generate_fastapi_files(
                    {
                        "plan": plan,
                        "ui_spec": ui_spec,
                        "backend_spec": backend_spec,
                    }
                )
            )

        # ----------------------------------------------------
        # Calculate statistics
        # ----------------------------------------------------

        total_files = len(
            files
        )

        total_size = (
            FileService.calculate_total_size(
                files
            )
        )

        code_lines = (
            FileService.calculate_code_lines(
                files
            )
        )

        # ----------------------------------------------------
        # Update completed project
        # ----------------------------------------------------

        update_data = {
            "status": ProjectStatus.completed,
            "plan": plan,
            "ui_spec": ui_spec,
            "backend_spec": backend_spec,
            "files": files,
            "total_files": total_files,
            "total_size": total_size,
            "code_lines": code_lines,
        }

        await repo.update(
            project_id,
            update_data,
        )

        logger.info(
            "Application generation completed",
            project_id=project_id,
            total_files=total_files,
        )

    except Exception as e:

        logger.error(
            "Application generation failed",
            project_id=project_id,
            error=str(e),
        )

        # ----------------------------------------------------
        # Update project with error
        # ----------------------------------------------------

        try:

            repo = ProjectRepository(
                db
            )

            await repo.update(
                 project_id,
                 {
                    "status": ProjectStatus.ERROR,
                    "error_message": str(e),
                 },
            )

        except Exception as update_error:

            logger.error(
                "Failed to update project error",
                project_id=project_id,
                error=str(update_error),
            )

    finally:

        db.close()
@router.put("/{project_id}")
async def update_project(
    project_id: int,
    request: dict,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    repo = ProjectRepository(db)

    project = await repo.get_user_project(
        user_id=user_id,
        project_id=project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    updated = await repo.update(
        id=project_id,
        obj_in=request,
    )

    return {
    "success": True,
    "project": {
        "id": updated.id,
        "user_id": updated.user_id,
        "name": updated.name,
        "description": updated.description,
        "idea": updated.idea,
        "slug": updated.slug,
        "status": updated.status.value if hasattr(updated.status, "value") else updated.status,
        "framework": updated.framework.value if hasattr(updated.framework, "value") else updated.framework,
        "files": updated.files,
        "plan": updated.plan,
        "ui_spec": updated.ui_spec,
        "backend_spec": updated.backend_spec,
        "total_files": updated.total_files,
        "total_size": updated.total_size,
        "code_lines": updated.code_lines,
        "created_at": updated.created_at.isoformat() if updated.created_at else None,
        "updated_at": updated.updated_at.isoformat() if updated.updated_at else None,
    },
}

# ============================================================
# TEST ROUTE
# ============================================================

@router.get(
    "/test"
)
async def test_projects():

    return {
        "success": True,
        "message": "Projects route working",
    }


# ============================================================
# GENERATE APPLICATION
# ============================================================

@router.post("/")
async def generate_app(
    request: GenerateAppRequest,
    background_tasks: BackgroundTasks,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        project = await ProjectService.create_project(
            db=db,
            user_id=user_id,
            name=request.name[:50],
            description=request.description,
            idea=request.description,
            framework=request.framework.value,
)

        background_tasks.add_task(
            generate_app_background,
            project.id,
        )

        return {
            "success": True,
            "project_id": project.id,
            "status": "generating",
            "message": "Application generation started",
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# ============================================================
# GET SINGLE PROJECT
# ============================================================

@router.get(
    "/{project_id}"
)
async def get_project(
    project_id: int,
    user_id: int = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    ),
):
    """
    Get a single project.
    """

    try:

        project = (
            await ProjectService.get_project(
                db=db,
                user_id=user_id,
                project_id=project_id,
            )
        )

        return {
            "success": True,
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "idea": project.idea,
            "status": project.status,
            "framework": project.framework,
            "plan": project.plan,
            "ui_spec": project.ui_spec,
            "backend_spec": project.backend_spec,
            "files": project.files,
            "total_files": getattr(
                project,
                "total_files",
                0,
            ),
            "total_size": getattr(
                project,
                "total_size",
                0,
            ),
            "code_lines": getattr(
                project,
                "code_lines",
                0,
            ),
            "error_message": getattr(
                project,
                "error_message",
                None,
            ),
            "created_at": (
                project.created_at.isoformat()
                if project.created_at
                else None
            ),
            "updated_at": (
                project.updated_at.isoformat()
                if getattr(
                    project,
                    "updated_at",
                    None,
                )
                else None
            ),
        }

    except HTTPException:

        raise

    except Exception as e:

        logger.error(
            "Failed to get project",
            project_id=project_id,
            error=str(e),
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )


# ============================================================
# LIST PROJECTS
# ============================================================

@router.get(
    "/"
)
async def list_projects(
    skip: int = 0,
    limit: int = 50,
    user_id: int = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    ),
):
    """
    Get all projects belonging
    to the authenticated user.
    """

    try:

        if skip < 0:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="skip cannot be negative",
            )

        if limit < 1 or limit > 100:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="limit must be between 1 and 100",
            )

        repo = ProjectRepository(
            db
        )

        projects = (
            await repo.get_user_projects(
                user_id,
                skip,
                limit,
            )
        )

        return [
            {
                "id": project.id,
                "name": project.name,
                "status": project.status,
                "framework": project.framework,
                "created_at": (
                    project.created_at.isoformat()
                    if project.created_at
                    else None
                ),
            }
            for project in projects
        ]

    except HTTPException:

        raise

    except Exception as e:

        logger.error(
            "Failed to list projects",
            user_id=user_id,
            error=str(e),
        )

        raise HTTPException(
            status_code=(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
            detail="Failed to retrieve projects",
        )


# ============================================================
# DELETE PROJECT
# ============================================================

@router.delete(
    "/{project_id}"
)
async def delete_project(
    project_id: int,
    user_id: int = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    ),
):
    """
    Delete a project.
    """

    try:

        await ProjectService.delete_project(
            db=db,
            user_id=user_id,
            project_id=project_id,
        )

        return {
            "success": True,
            "status": "ok",
            "message": (
                "Project deleted successfully"
            ),
        }

    except HTTPException:

        raise

    except Exception as e:

        logger.error(
            "Failed to delete project",
            project_id=project_id,
            error=str(e),
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )


# ============================================================
# EXPORTS
# ============================================================

__all__ = [
    "router",
    "ProjectService",
    "get_db",
    "generate_app_background",
]

