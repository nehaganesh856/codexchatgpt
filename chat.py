
from datetime import datetime
import json
from typing import Set

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from sqlalchemy.orm import Session

from backend.core.validation import ChatRequest
from backend.core.security import get_current_user
from backend.core.logging import Logger

from backend.services.project import ProjectService
from backend.services.ai import AIService

from backend.db.session import get_db


# ============================================================
# LOGGER
# ============================================================

logger = Logger(__name__)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/api",
    tags=["chat"],
)


# ============================================================
# CONNECTION MANAGER
# ============================================================

class ConnectionManager:
    """
    Manages active WebSocket connections.
    """

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(
        self,
        websocket: WebSocket,
    ):
        """
        Accept and register a WebSocket connection.
        """

        await websocket.accept()

        self.active_connections.add(
            websocket
        )

        logger.info(
            "WebSocket connected",
            active_connections=len(
                self.active_connections
            ),
        )

    async def disconnect(
        self,
        websocket: WebSocket,
    ):
        """
        Remove a WebSocket connection.
        """

        self.active_connections.discard(
            websocket
        )

        logger.info(
            "WebSocket disconnected",
            active_connections=len(
                self.active_connections
            ),
        )

    async def broadcast(
        self,
        message: dict,
    ):
        """
        Send a message to all active WebSocket clients.
        """

        disconnected_connections = []

        for connection in list(
            self.active_connections
        ):
            try:
                await connection.send_json(
                    {
                        "type": "message",
                        "data": message,
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                )

            except Exception as e:
                logger.error(
                    "Broadcast error",
                    error=str(e),
                )

                disconnected_connections.append(
                    connection
                )

        # Remove broken connections
        for connection in disconnected_connections:
            await self.disconnect(
                connection
            )


# ============================================================
# GLOBAL CONNECTION MANAGER
# ============================================================

manager = ConnectionManager()


# ============================================================
# HTTP CHAT ENDPOINT
# ============================================================

@router.post(
    "/chat",
)
async def chat(
    request: ChatRequest,
    user_id: int = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    ),
):
    """
    Chat endpoint for modifying an existing project
    using AI.

    The request should contain:
    - project_id
    - message
    """

    try:
        # ----------------------------------------------------
        # GET PROJECT
        # ----------------------------------------------------

        project = await ProjectService.get_project(
            db,
            user_id,
            request.project_id,
        )

        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        # ----------------------------------------------------
        # INITIALIZE AI SERVICE
        # ----------------------------------------------------

        ai_service = AIService()

        # ----------------------------------------------------
        # SEND PROJECT DATA TO AI
        # ----------------------------------------------------

        response = await ai_service.chat_modify_project(
            {
                "plan": project.plan,
                "ui_spec": project.ui_spec,
                "backend_spec": project.backend_spec,
            },
            request.message,
        )

        # ----------------------------------------------------
        # LOG SUCCESS
        # ----------------------------------------------------

        logger.info(
            "Chat response generated",
            project_id=request.project_id,
            user_id=user_id,
        )

        # ----------------------------------------------------
        # RETURN RESPONSE
        # ----------------------------------------------------

        return {
            "response": response,
            "project_id": request.project_id,
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(
            "Chat failed",
            error=str(e),
            project_id=request.project_id,
            user_id=user_id,
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# ============================================================
# WEBSOCKET CHAT ENDPOINT
# ============================================================

@router.websocket(
    "/ws/chat/{project_id}"
)
async def websocket_chat(
    websocket: WebSocket,
    project_id: int,
):
    """
    WebSocket endpoint for real-time project chat.
    """

    await manager.connect(
        websocket
    )

    try:
        while True:

            # ------------------------------------------------
            # RECEIVE MESSAGE
            # ------------------------------------------------

            data = await websocket.receive_text()

            # ------------------------------------------------
            # PARSE JSON
            # ------------------------------------------------

            try:
                message_data = json.loads(
                    data
                )

            except json.JSONDecodeError:
                await websocket.send_json(
                    {
                        "type": "error",
                        "message": "Invalid JSON message",
                    }
                )

                continue

            # ------------------------------------------------
            # ADD PROJECT ID
            # ------------------------------------------------

            message = {
                "project_id": project_id,
                "data": message_data,
                "timestamp": datetime.utcnow().isoformat(),
            }

            # ------------------------------------------------
            # BROADCAST MESSAGE
            # ------------------------------------------------

            await manager.broadcast(
                message
            )

    except WebSocketDisconnect:

        logger.info(
            "WebSocket client disconnected",
            project_id=project_id,
        )

        await manager.disconnect(
            websocket
        )

    except Exception as e:

        logger.error(
            "WebSocket error",
            error=str(e),
            project_id=project_id,
        )

        await manager.disconnect(
            websocket
        )

