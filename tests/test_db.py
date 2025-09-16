from sqlmodel import select

from db import make_session_factory
from domain.models import Instrument as DomainInstrument
from persistence.models import InstrumentTable
from persistence.repositories import InstrumentRepository


def test_get_session_in_memory_can_create_tables() -> None:
    # Import persistence models before creating tables so metadata is populated
    assert InstrumentTable.__tablename__ == "instruments"

    # Create a session factory for an in-memory SQLite database
    session_factory = make_session_factory("sqlite:///:memory:")
    repo = InstrumentRepository()

    # Verify we can insert via repository and then read it back
    with session_factory() as s:
        inst = DomainInstrument(
            exchange="bybit", name="BTCUSDT", kind="linear", base="BTC", quote="USDT"
        )
        repo.upsert_many(s, [inst])
        s.commit()

    with session_factory() as s:
        items = s.exec(
            select(InstrumentTable).where(InstrumentTable.exchange == "bybit")
        ).all()

        assert len(items) == 1
        got = items[0]
        assert got.name == "BTCUSDT"
        assert got.base == "BTC"
        assert got.quote == "USDT"
