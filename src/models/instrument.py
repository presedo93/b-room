from enum import Enum
from sqlmodel import SQLModel


# class Instrument(SQLModel, table=True):
#     name: str
#     kind: "Kind"
#     base: str
#     quote: str
#
#     def from_bybit(self, data: "ByBitInstrument") -> "Instrument":
#         """Create an Instrument from a ByBit API response."""
#         return Instrument(
#             name=data.symbol,
#             kind=Kind(data.kind),
#             base=data.base_currency,
#             quote=data.quote_currency,
#         )


# class Kind(str, Enum):
#     SPOT = "spot"
#     LINEAR = "linear"
#     INVERSE = "inverse"
#     OPTION = "option"
