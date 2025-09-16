"""ByBit exchange adapter wrapping existing DTOs and mapping to normalized
DTOs."""

from typing import override

from adapters.exchanges.base import ExchangeClient, ExchangeInstrumentDTO
from models.exchanges.bybit import ByBitInstrument, ByBitCategory


class ByBitClient(ExchangeClient):
    @property
    @override
    def name(self) -> str:  # pragma: no cover - trivial
        return "bybit"

    @override
    def list_instruments(self, category: str) -> list[ExchangeInstrumentDTO]:
        cat = ByBitCategory.from_str(category)
        data = ByBitInstrument.fetch(cat)
        return [
            ExchangeInstrumentDTO(
                exchange="bybit",
                name=item.symbol,
                kind=(item.category or cat.value),
                base=item.base_coin,
                quote=item.quote_coin,
            )
            for item in data
        ]
