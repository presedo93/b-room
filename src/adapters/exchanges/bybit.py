"""ByBit exchange adapter wrapping existing DTOs and mapping to normalized DTOs."""

from __future__ import annotations

from adapters.exchanges.base import ExchangeClient, ExchangeInstrumentDTO
from models.exchanges.bybit import ByBitInstrument, ByBitCategory


class ByBitClient(ExchangeClient):
    @property
    def name(self) -> str:  # pragma: no cover - trivial
        return "bybit"

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
