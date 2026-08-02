
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.config.settings import get_settings

from pathlib import Path
# ============================================================
# SETTINGS
# ============================================================

settings = get_settings()

DATABASE_URL = settings.database_url


# ============================================================
# DATABASE CONNECTION OPTIONS
# ============================================================

connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False
    }


# ============================================================
# DATABASE ENGINE
# ============================================================

engine = create_engine(
    DATABASE_URL,
    echo=settings.database_echo,
    future=True,
    connect_args=connect_args,
)


print("=" * 60)
print("DATABASE_URL =", DATABASE_URL)

if DATABASE_URL.startswith("sqlite:///"):
    db_path = DATABASE_URL.replace("sqlite:///", "")
    print("ABSOLUTE PATH =", Path(db_path).resolve())

print("=" * 60)


# ============================================================
# DATABASE SESSION
# ============================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


# ============================================================
# FASTAPI DATABASE DEPENDENCY
# ============================================================

def get_db():
    """
    Provide a database session for FastAPI requests.

    The session is automatically closed after
    the request is completed.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

