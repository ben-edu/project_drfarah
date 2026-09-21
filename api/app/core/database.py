"""Database connection (SQLAlchemy 2.x).

Connections and sessions are closed correctly after each request.
No tables are created yet — models will be added in a later step.
"""

from collections.abc import Generator

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings

# Engine is created lazily so tests can override the URL first.
_engine: Engine | None = None
_SessionLocal: sessionmaker | None = None


def _get_engine() -> Engine:
    global _engine
    if _engine is None:
        s = get_settings()
        url = s.effective_database_url
        if url is None:
            url = "sqlite:///./drfarah.db"
        _engine = create_engine(
            url,
            pool_pre_ping=True,
            echo=(s.ENVIRONMENT == "dev"),
            connect_args={"check_same_thread": False} if url.startswith("sqlite") else {},
        )
    return _engine


def _get_session_local() -> sessionmaker:
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            bind=_get_engine(), autoflush=False, autocommit=False
        )
    return _SessionLocal


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = _get_session_local()()
    try:
        yield db
    finally:
        db.close()


def check_database_connection() -> bool:
    """Return True if the database is reachable and responsive."""
    try:
        engine = _get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


def reset_engine() -> None:
    """Reset the cached engine (used in tests to switch DB URL)."""
    global _engine, _SessionLocal
    if _engine is not None:
        _engine.dispose()
    _engine = None
    _SessionLocal = None
