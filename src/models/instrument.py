from enum import Enum
from sqlmodel import Field, SQLModel, Session
from sqlalchemy.dialects.sqlite import insert

from models.exchanges.bybit import ByBitInstrument


class Instrument(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    exchange: str = Field(primary_key=True)
    name: str = Field(primary_key=True)
    kind: str
    base: str
    quote: str

    @classmethod
    def from_bybit(cls, data: "ByBitInstrument") -> "Instrument":
        """Create an Instrument from a ByBit API response."""
        return Instrument(
            name=data.symbol,
            exchange="bybit",
            kind=Kind(data.category).value,
            base=data.base_coin,
            quote=data.quote_coin,
        )

    def upsert(self, session: Session):
        """Upsert the instrument into the database."""
        stmt = (
            insert(Instrument)
            .values(**self)
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
    SPOT = "spot"
    LINEAR = "linear"
    INVERSE = "inverse"
    OPTION = "option"

    @classmethod
    def from_str(cls, category: str) -> "Kind":
        """Convert a string to a Kind enum."""
        return cls(category.lower())
