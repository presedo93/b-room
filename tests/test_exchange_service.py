from collections.abc import Iterable
from typing import override
from sqlmodel import Session

from db import make_session_factory
from domain.models import Instrument as DomainInstrument
from adapters.exchanges.base import ExchangeInstrumentDTO, ExchangeClient
from services.exchange_service import ExchangeService

# Import persistence models before creating tables
from persistence.models import InstrumentTable


class StubRepo:
    def __init__(self) -> None:
        self._items: list[DomainInstrument] = []

    def upsert_many(self, _session: Session, items: Iterable[DomainInstrument]) -> None:
        # emulate deduplication by (exchange, name)
        existing = {(i.exchange, i.name) for i in self._items}
        for it in items:
            key = (it.exchange, it.name)
            if key in existing:
                # replace existing by updating fields
                for idx, cur in enumerate(self._items):
                    if (cur.exchange, cur.name) == key:
                        self._items[idx] = it
                        break
            else:
                self._items.append(it)
                existing.add(key)

    def list_by_exchange(
        self, _session: Session, exchange: str
    ) -> list[DomainInstrument]:
        return [i for i in self._items if i.exchange == exchange]


class StubClient(ExchangeClient):
    def __init__(self, items: list[ExchangeInstrumentDTO]) -> None:
        self._items = items

    @property
    @override
    def name(self) -> str:
        return "stub"

    @override
    def list_instruments(self, category: str) -> list[ExchangeInstrumentDTO]:
        return list(self._items)


def test_exchange_service_populate_and_list() -> None:
    assert InstrumentTable.__tablename__ == "instruments"

    session_factory = make_session_factory("sqlite:///:memory:")
    repo = StubRepo()
    items = [
        ExchangeInstrumentDTO("bybit", "BTCUSDT", "linear", "BTC", "USDT"),
        ExchangeInstrumentDTO("bybit", "ETHUSDT", "linear", "ETH", "USDT"),
    ]
    client = StubClient(items)

    svc = ExchangeService(
        session_factory=session_factory, repository=repo, clients={"bybit": client}
    )

    # Populate
    count = svc.populate_instruments("bybit", "linear")
    assert count == 2

    # List
    listed = svc.list_instruments("bybit")
    names = sorted(i.name for i in listed)
    assert names == ["BTCUSDT", "ETHUSDT"]
