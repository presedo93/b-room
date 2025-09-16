"""SQLModel table definitions for persistence.

These mirror the existing database schema but are decoupled from adapters and
domain logic. Mapping between these and domain models is handled by
repositories.
"""

from __future__ import annotations

from typing import Annotated, ClassVar

from sqlmodel import Field, SQLModel


class InstrumentTable(SQLModel, table=True):
    """Instrument table mirroring the current schema.

    Composite primary key: (exchange, name)
    """

    __tablename__ = "instrument"  # keep same name for continuity
    __table_args__: ClassVar[dict[str, bool]] = {"extend_existing": True}

    exchange: Annotated[str, Field(primary_key=True)]
    name: Annotated[str, Field(primary_key=True)]
    kind: Annotated[str, Field(description="Instrument category, e.g. linear")]
    base: Annotated[str, Field(description="Base asset symbol")]
    quote: Annotated[str, Field(description="Quote asset symbol")]
