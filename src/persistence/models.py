"""SQLModel table definitions for persistence.

These mirror the existing database schema but are decoupled from adapters and
domain logic. Mapping between these and domain models is handled by
repositories.
"""

from typing import Annotated

from sqlmodel import Field, SQLModel


class InstrumentTable(SQLModel, table=True):
    """Instrument table mirroring the current schema.

    Composite primary key: (exchange, name)
    """

    __tablename__: str = "instruments"  # pyright: ignore[reportIncompatibleVariableOverride]

    exchange: Annotated[str, Field(primary_key=True)]
    name: Annotated[str, Field(primary_key=True)]
    kind: Annotated[str, Field(description="Instrument category, e.g. linear")]
    base: Annotated[str, Field(description="Base asset symbol")]
    quote: Annotated[str, Field(description="Quote asset symbol")]
