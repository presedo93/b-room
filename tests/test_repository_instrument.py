from db import make_session_factory

# Import persistence models BEFORE creating tables so metadata is populated
from persistence.models import InstrumentTable
from domain.models import Instrument as DomainInstrument
from persistence.repositories import InstrumentRepository
from sqlmodel import select


def test_upsert_and_list_and_get() -> None:
    assert InstrumentTable.__tablename__ == "instruments"

    # Create in-memory session factory with tables
    session_factory = make_session_factory("sqlite:///:memory:")
    repo = InstrumentRepository()

    items = [
        DomainInstrument("bybit", "BTCUSDT", "linear", "BTC", "USDT"),
        DomainInstrument("bybit", "ETHUSDT", "linear", "ETH", "USDT"),
        DomainInstrument("bybit", "BTCUSDT", "linear", "BTC", "USDT"),  # duplicate
    ]

    # Upsert
    with session_factory() as s:
        repo.upsert_many(s, items)
        s.commit()

        # Raw count from table should be 2 (deduped by upsert)
        cnt = s.exec(
            select(InstrumentTable).where(InstrumentTable.exchange == "bybit")
        ).all()
        assert len(cnt) == 2

    # List
    with session_factory() as s:
        listed = repo.list_by_exchange(s, "bybit")
    names = sorted(i.name for i in listed)
    assert names == ["BTCUSDT", "ETHUSDT"]

    # Get existing
    with session_factory() as s:
        btc = repo.get(s, "bybit", "BTCUSDT")
        assert btc is not None
        assert btc.base == "BTC"
        assert btc.quote == "USDT"

    # Get missing
    with session_factory() as s:
        missing = repo.get(s, "bybit", "DOGEUSDT")
        assert missing is None
