"""Exchange adapter base interfaces and DTOs."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(slots=True)
class ExchangeInstrumentDTO:
    """Normalized instrument representation returned by exchange adapters."""

    exchange: str
    name: str
    kind: str
    base: str
    quote: str


class ExchangeClient(ABC):
    """Protocol for exchange-specific clients that fetch instruments."""

    @property
    @abstractmethod
    def name(self) -> str:  # e.g., "bybit"
        ...

    @abstractmethod
    def list_instruments(self, category: str) -> list[ExchangeInstrumentDTO]:
        """Return instruments for the given category (e.g., 'linear')."""
        ...
