#!/usr/bin/env python3

"""
FastAPI Main Application Entry Point
AI Code Generator Backend
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import uvicorn

from backend.core.logging import Logger
from backend.config.settings import get_settings

from backend.db.base import Base
from backend.db.session import engine


# ============================================================
# ROUTERS
# ============================================================

from backend.api.routes.auth import router as auth_router
from backend.api.routes.projects import router as projects_router
from backend.api.routes.files import router as files_router
from backend.api.routes.versions import router as versions_router
from backend.api.routes.chat import router as chat_router
from backend.api.routes.deploy import router as deploy_router
from backend.api.routes.export import router as export_router


# ============================================================
# LOGGER & SETTINGS
# ============================================================

logger = Logger(__name__)

settings = get_settings()


# ============================================================
# DATABASE LIFESPAN
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info(
        "Application startup",
        environment=settings.environment,
        debug=settings.debug,
    )

    # Create database tables
    Base.metadata.create_all(bind=engine)

    yield

    logger.info("Application shutdown")


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="AI Code Generator API",
    description="AI-powered code generation backend",
    version="1.0.0",
    lifespan=lifespan,
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8080",

        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ============================================================
# ROUTER REGISTRATION
# ============================================================


app.include_router(
    auth_router,
    prefix="/api/auth",
    tags=["Authentication"]
)


app.include_router(
    projects_router,
    prefix="/api/projects",
    tags=["Projects"]
)


app.include_router(
    files_router,
    prefix="/api/files",
    tags=["Files"]
)


app.include_router(
    versions_router,
    prefix="/api/versions",
    tags=["Versions"]
)


app.include_router(
    chat_router,
    prefix="/api",
    tags=["Chat"]
)


app.include_router(
    deploy_router,
    prefix="/api/deploy",
    tags=["Deployment"]
)


app.include_router(
    export_router,
    prefix="/api/export",
    tags=["Export"]
)



# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health", tags=["Health"])
async def health_check():

    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.environment,
    }



# ============================================================
# ROOT API
# ============================================================

@app.get("/", tags=["Root"])
async def root():

    return {
        "message": "AI Code Generator API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }



# ============================================================
# GLOBAL ERROR HANDLER
# ============================================================

@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception
):

    logger.error(
        "Unhandled exception",
        error=str(exc),
        path=request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        },
    )



# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )