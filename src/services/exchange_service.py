"""Service layer to orchestrate exchange imports and queries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping

from sqlmodel import Session

from domain.models import Instrument as DomainInstrument
from persistence.repositories import InstrumentRepository
from adapters.exchanges.base import ExchangeClient, ExchangeInstrumentDTO
from adapters.exchanges.bybit import ByBitClient


def _default_clients() -> dict[str, ExchangeClient]:
    return {"bybit": ByBitClient()}


@dataclass(slots=True)
class ExchangeService:
    session_factory: Callable[[], Session]
    repository: InstrumentRepository
    clients: Mapping[str, ExchangeClient]

    @classmethod
    def with_defaults(
        cls, session_factory: Callable[[], Session], repository: InstrumentRepository
    ) -> "ExchangeService":
        return cls(session_factory=session_factory, repository=repository, clients=_default_clients())

    def populate_instruments(self, exchange: str, category: str) -> int:
        """Fetch instruments from an exchange and persist them via repository.

        Returns the number of instruments processed.
        """
        client = self._get_client(exchange)
        items = client.list_instruments(category)
        domain_items = [self._dto_to_domain(d) for d in items]
        with self.session_factory() as s:
            self.repository.upsert_many(s, domain_items)
            s.commit()
        return len(items)

    def list_instruments(self, exchange: str) -> list[DomainInstrument]:
        """List instruments for an exchange from the repository."""
        with self.session_factory() as s:
            return self.repository.list_by_exchange(s, exchange)

    def _get_client(self, exchange: str) -> ExchangeClient:
        try:
            return self.clients[exchange]
        except KeyError as exc:  # pragma: no cover - defensive
            raise ValueError(f"Unknown exchange: {exchange}") from exc

    @staticmethod
    def _dto_to_domain(d: ExchangeInstrumentDTO) -> DomainInstrument:
        return DomainInstrument(exchange=d.exchange, name=d.name, kind=d.kind, base=d.base, quote=d.quote)
