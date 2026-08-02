import os
from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


    # ==================================================
    # APPLICATION
    # ==================================================

    app_name: str = "AI App Generator"
    app_version: str = "2.0.0"

    environment: str = "development"
    debug: bool = True



    # ==================================================
    # SERVER
    # ==================================================

    host: str = "0.0.0.0"

    port: int = 8000

    workers: int = 1

    reload: bool = True



    # ==================================================
    # DATABASE
    # ==================================================

    database_url: str = "sqlite:///./database/app.db"

    database_echo: bool = False



    # ==================================================
    # REDIS
    # ==================================================

    redis_url: str = "redis://localhost:6379"

    redis_db: int = 0



    # ==================================================
    # AUTHENTICATION
    # ==================================================

    secret_key: str = Field(
        default="dev-secret-key-change-this",
        validation_alias="SECRET_KEY"
    )

    algorithm: str = "HS256"


    access_token_expire_minutes: int = 30

    refresh_token_expire_days: int = 7



    # ==================================================
    # AI API KEYS
    # ==================================================

    openai_api_key: str = Field(
        default="",
        validation_alias="OPENAI_API_KEY"
    )


    anthropic_api_key: str = Field(
        default="",
        validation_alias="ANTHROPIC_API_KEY"
    )


    openrouter_api_key: str = Field(
        default="",
        validation_alias="OPENROUTER_API_KEY"
    )


    gemini_api_key: str = Field(
        default="",
        validation_alias="GEMINI_API_KEY"
    )


    groq_api_key: str = Field(
        default="",
        validation_alias="GROQ_API_KEY"
    )



    github_token: str = Field(
        default="",
        validation_alias="GITHUB_TOKEN"
    )


    vercel_token: str = Field(
        default="",
        validation_alias="VERCEL_TOKEN"
    )



    # ==================================================
    # FRONTEND / BACKEND URL
    # ==================================================

    frontend_url: str = "http://localhost:5173"

    backend_url: str = "http://localhost:8000"



    # ==================================================
    # FILE UPLOAD
    # ==================================================

    upload_dir: str = "uploads"

    max_upload_size: int = 100 * 1024 * 1024



    # ==================================================
    # LOGGING
    # ==================================================

    log_level: str = "INFO"

    log_format: str = (
        "%(asctime)s - "
        "%(levelname)s - "
        "%(name)s - "
        "%(message)s"
    )


    log_file: str = "logs/app.log"



    # ==================================================
    # CORS
    # ==================================================

    cors_origins: List[str] = [
        "http://localhost:5173"
    ]


    cors_credentials: bool = True


    cors_methods: List[str] = [
        "*"
    ]


    cors_headers: List[str] = [
        "*"
    ]



    # ==================================================
    # RATE LIMITING
    # ==================================================

    rate_limit_enabled: bool = True

    rate_limit_requests: int = 100

    rate_limit_period: int = 60



    # ==================================================
    # AI SETTINGS
    # ==================================================

    ai_model_default: str = "gpt-4o-mini"

    ai_model_advanced: str = "gpt-4-turbo"


    ai_temperature: float = 0.7

    ai_max_tokens: int = 4000



    # ==================================================
    # CELERY
    # ==================================================

    celery_broker_url: str = (
        "redis://localhost:6379/1"
    )


    celery_result_backend: str = (
        "redis://localhost:6379/2"
    )



    # ==================================================
    # VALIDATORS
    # ==================================================

    @field_validator(
        "cors_origins",
        mode="before"
    )
    @classmethod
    def parse_cors_origins(cls, value):

        if isinstance(value, str):

            return [
                item.strip()
                for item in value.split(",")
                if item.strip()
            ]

        return value



    # ==================================================
    # ENVIRONMENT CHECKS
    # ==================================================

    @property
    def is_production(self) -> bool:

        return (
            self.environment.lower()
            == "production"
        )



    @property
    def is_development(self) -> bool:

        return (
            self.environment.lower()
            == "development"
        )





# ==================================================
# SETTINGS INSTANCE
# ==================================================

@lru_cache()
def get_settings() -> Settings:


    settings = Settings()



    # ------------------------------
    # Create upload directory
    # ------------------------------

    os.makedirs(
        settings.upload_dir,
        exist_ok=True
    )



    # ------------------------------
    # Create SQLite directory
    # ------------------------------

    if settings.database_url.startswith(
        "sqlite:///"
    ):

        db_path = (
            settings.database_url
            .replace(
                "sqlite:///",
                ""
            )
        )


        db_folder = os.path.dirname(
            db_path
        )


        if db_folder:

            os.makedirs(
                db_folder,
                exist_ok=True
            )



    # ------------------------------
    # Create log directory
    # ------------------------------

    if settings.log_file:

        log_folder = os.path.dirname(
            settings.log_file
        )


        if log_folder:

            os.makedirs(
                log_folder,
                exist_ok=True
            )



    return settings