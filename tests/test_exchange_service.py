import os
import sys
from typing import Iterable


# Ensure `src` on sys.path
CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from sqlmodel import Session

from db import make_session_factory
from domain.models import Instrument as DomainInstrument
from adapters.exchanges.base import ExchangeInstrumentDTO, ExchangeClient
from services.exchange_service import ExchangeService

# Import persistence models before creating tables
from persistence.models import InstrumentTable  # noqa: F401


class StubRepo:
    def __init__(self) -> None:
        self._items: list[DomainInstrument] = []

    def upsert_many(self, session: Session, items: Iterable[DomainInstrument]) -> None:  # noqa: ARG002 - session unused
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

    def list_by_exchange(self, session: Session, exchange: str) -> list[DomainInstrument]:  # noqa: ARG002 - session unused
        return [i for i in self._items if i.exchange == exchange]


class StubClient(ExchangeClient):
    def __init__(self, items: list[ExchangeInstrumentDTO]) -> None:
        self._items = items

    @property
    def name(self) -> str:
        return "stub"

    def list_instruments(self, category: str) -> list[ExchangeInstrumentDTO]:  # noqa: ARG002 - category unused
        return list(self._items)


def test_exchange_service_populate_and_list() -> None:
    session_factory = make_session_factory("sqlite:///:memory:")
    repo = StubRepo()
    items = [
        ExchangeInstrumentDTO("bybit", "BTCUSDT", "linear", "BTC", "USDT"),
        ExchangeInstrumentDTO("bybit", "ETHUSDT", "linear", "ETH", "USDT"),
    ]
    client = StubClient(items)

    svc = ExchangeService(session_factory=session_factory, repository=repo, clients={"bybit": client})

    # Populate
    count = svc.populate_instruments("bybit", "linear")
    assert count == 2

    # List
    listed = svc.list_instruments("bybit")
    names = sorted(i.name for i in listed)
    assert names == ["BTCUSDT", "ETHUSDT"]

