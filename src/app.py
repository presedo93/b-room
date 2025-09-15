"""Lightweight application context and factory.

Provides a minimal AppContext that holds a session factory. Additional fields
for repositories and services can be added incrementally in later stages.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from sqlmodel import Session

from db import DEFAULT_DB_URL, make_session_factory


@dataclass(slots=True)
class AppContext:
    """Application-level dependencies container.

    Currently only exposes a database session factory.
    """

    session_factory: Callable[[], Session]


def create_app_context(database_url: str = DEFAULT_DB_URL) -> AppContext:
    """Construct an `AppContext` for the given database URL."""
    return AppContext(session_factory=make_session_factory(database_url))
