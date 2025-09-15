"""SQLModel table definitions for persistence.

These mirror the existing database schema but are decoupled from adapters and
domain logic. Mapping between these and domain models is handled by
repositories.
"""

from __future__ import annotations

from typing import ClassVar

from sqlmodel import Field, SQLModel


class InstrumentTable(SQLModel, table=True):
    """Instrument table mirroring the current schema.

    Composite primary key: (exchange, name)
    """

    __tablename__ = "instrument"  # keep same name for continuity
    __table_args__: ClassVar[dict[str, bool]] = {"extend_existing": True}

    exchange: str = Field(primary_key=True)
    name: str = Field(primary_key=True)
    kind: str
    base: str
    quote: str

