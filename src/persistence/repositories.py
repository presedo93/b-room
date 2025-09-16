"""Repository implementations for persistence layer.

Provides an InstrumentRepository to read/write instruments while mapping to
domain models.
"""

from collections.abc import Iterable
from sqlalchemy.dialects.sqlite import insert
from sqlmodel import Session, select

from domain.models import Instrument as DomainInstrument
from persistence.models import InstrumentTable


class InstrumentRepository:
    """Repository for Instrument entities."""

    def upsert_many(self, session: Session, items: Iterable[DomainInstrument]) -> None:
        """Upsert a batch of instruments.

        Uses SQLite ON CONFLICT on (exchange, name) to update existing rows.
        """
        for it in items:
            stmt = (
                insert(InstrumentTable)
                .values(
                    exchange=it.exchange,
                    name=it.name,
                    kind=it.kind,
                    base=it.base,
                    quote=it.quote,
                )
                .on_conflict_do_update(
                    index_elements=["exchange", "name"],
                    set_={"kind": it.kind, "base": it.base, "quote": it.quote},
                )
            )
            session.connection().execute(stmt)

    def list_by_exchange(
        self, session: Session, exchange: str
    ) -> list[DomainInstrument]:
        """List all instruments for an exchange as domain models."""
        rows = session.exec(
            select(InstrumentTable).where(InstrumentTable.exchange == exchange)
        ).all()
        return [self._to_domain(r) for r in rows]

    def get(
        self, session: Session, exchange: str, name: str
    ) -> DomainInstrument | None:
        """Get a single instrument by exchange and name."""
        row = session.exec(
            select(InstrumentTable).where(
                (InstrumentTable.exchange == exchange) & (InstrumentTable.name == name)
            )
        ).first()
        return None if row is None else self._to_domain(row)

    @staticmethod
    def _to_domain(row: InstrumentTable) -> DomainInstrument:
        return DomainInstrument(
            exchange=row.exchange,
            name=row.name,
            kind=row.kind,
            base=row.base,
            quote=row.quote,
        )
