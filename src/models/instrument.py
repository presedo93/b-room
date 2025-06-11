from dataclasses import dataclass
from enum import Enum
from typing import Literal

from sqlmodel import SQLModel


class Instrument(SQLModel, table=True):
    name: str
    kind: "Kind"
    base: str
    quote: str
    fees: dict[Literal["taker", "maker"], float]
    size: float

    def from_bybit(self, data: "ByBitInstrument") -> "Instrument":
        """Create an Instrument from a ByBit API response."""
        return Instrument(
            name=data.instrument_name,
            kind=Kind(data.kind),
            base=data.base_currency,
            quote=data.quote_currency,
            fees={
                "taker": data.taker_commission,
                "maker": data.maker_commission,
            },
            size=data.tick_size,
        )


class Kind(str, Enum):
    SPOT = "spot"
    PERP = "perp"
    FUTURE = "future"
    OPTION = "option"


@dataclass
class ByBitInstrument:
    instrument_name: str
    kind: str
    base_currency: str
    quote_currency: str
    taker_commission: float
    maker_commission: float
    tick_size: float

    @classmethod
    def fetch(cls, _category: str = "linear") -> list["ByBitInstrument"]:
        """Fetch instruments from ByBit API."""
        # This is a placeholder for the actual API call.
        # In practice, you would use an HTTP client to fetch data from ByBit's API.
        return [
            cls(
                instrument_name="BTCUSDT",
                kind="linear",
                base_currency="BTC",
                quote_currency="USDT",
                taker_commission=0.001,
                maker_commission=0.0005,
                tick_size=0.01,
            )
        ]
