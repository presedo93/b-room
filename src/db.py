"""Database engine and session factory utilities.

This module centralizes creation of SQLAlchemy/SQLModel engines and provides a
session factory that can be reused across the app. It supports in-memory SQLite
with a static pool so that tables persist for the lifetime of the engine.
"""

from __future__ import annotations

from typing import Callable

from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine


# Default database URL for the application. File-based SQLite to persist data.
DEFAULT_DB_URL = "sqlite:///xini.db"


def _make_engine(database_url: str, *, echo: bool = False) -> Engine:
    """Create a SQLAlchemy engine for the given URL.

    Special handling for SQLite in-memory databases to ensure a single shared
    connection via StaticPool so that tables persist across sessions.
    """
    kwargs: dict[str, object] = {"echo": echo}

    if database_url.startswith("sqlite") and ":memory:" in database_url:
        kwargs.update(
            {
                "connect_args": {"check_same_thread": False},
                "poolclass": StaticPool,
            }
        )

    return create_engine(database_url, **kwargs)  # type: ignore[arg-type]


def make_session_factory(
    database_url: str = DEFAULT_DB_URL, *, echo: bool = False, create_tables: bool = True
) -> Callable[[], Session]:
    """Return a zero-arg callable that creates a `Session` bound to a stable engine.

    When `database_url` is an in-memory SQLite URL, a StaticPool is used so that
    every session shares the same connection and sees the same ephemeral DB.

    If `create_tables` is True, `SQLModel.metadata.create_all(engine)` is called.
    Ensure your models are imported before invoking this so their tables are
    registered in the metadata.
    """
    engine = _make_engine(database_url, echo=echo)
    if create_tables:
        SQLModel.metadata.create_all(engine)

    def _factory() -> Session:
        return Session(engine)

    return _factory


def get_session(database_url: str = DEFAULT_DB_URL, *, echo: bool = False) -> Session:
    """Convenience function to create a one-off `Session` for the given URL.

    Prefer `make_session_factory` for long-lived apps so connections are reused.
    """
    engine = _make_engine(database_url, echo=echo)
    return Session(engine)

