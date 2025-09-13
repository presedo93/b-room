"""Database model for trading instruments.

This module defines the Instrument SQLModel and the Kind enum used to
categorize instruments. Helper constructors and an upsert helper are
provided to integrate with exchange-specific DTOs.
"""

# Allow imports from third-party packages that may not be available in the
# linting environment.
# pylint: disable=import-error

from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel, Session
from sqlalchemy.dialects.sqlite import insert

if TYPE_CHECKING:
    from models.exchanges.bybit import ByBitInstrument


class Instrument(SQLModel, table=True):
    """Represents a trading instrument stored in the database."""

    __table_args__ = {"extend_existing": True}

    exchange: str = Field(primary_key=True)
    name: str = Field(primary_key=True)
    kind: str
    base: str
    quote: str

    @classmethod
    def from_bybit(cls, data: "ByBitInstrument") -> "Instrument":
        """Create an Instrument from a ByBitInstrument DTO.

        The ByBit data may provide a category or leave it empty; default to
        'spot' when missing.
        """
        return Instrument(
            name=data.symbol,
            exchange="bybit",
            kind=Kind.from_str(data.category or "spot").value,
            base=data.base_coin,
            quote=data.quote_coin,
        )

    def upsert(self, session: Session) -> None:
        """Insert or update this Instrument into the database.

        Uses SQLite's ON CONFLICT clause to perform an upsert based on the
        (exchange, name) composite primary key.
        """
        stmt = (
            insert(Instrument)
            .values(**self.model_dump())
            .on_conflict_do_update(
                index_elements=["exchange", "name"],
                set_={
                    "kind": self.kind,
                    "base": self.base,
                    "quote": self.quote,
                },
            )
        )

        session.connection().execute(stmt)


class Kind(str, Enum):
    """Enumeration of instrument categories/kinds."""

    SPOT = "spot"
    LINEAR = "linear"
    INVERSE = "inverse"
    OPTION = "option"

    @classmethod
    def from_str(cls, category: str) -> "Kind":
        """Convert a string to a Kind enum.

        The input is lower-cased to make the conversion case-insensitive.
        """
        return cls(category.lower())
