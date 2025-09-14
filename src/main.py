"""Streamlit app for the b-room dashboard.

This module defines the Streamlit pages, database setup and helper
functions to fetch and populate ByBit instruments.
"""

from typing import cast

import streamlit as st
from sqlmodel import SQLModel, Session, create_engine, select
from sqlalchemy.engine import Engine
from loguru import logger

from models.exchanges.bybit import ByBitInstrument, ByBitCategory
from models.instrument import Instrument

logger.level("DEBUG")
logger.add("xini.log", retention="2 days")
logger.info("Dashboard started")

engine: Engine = create_engine("sqlite:///xini.db")
SQLModel.metadata.create_all(engine)


def header_buttons() -> None:
    """Render the header page links."""
    c1, _, c3 = st.columns(3)

    with c1:
        st.page_link(exc_page, label="exchanges", icon="🔀", use_container_width=True)

    with c3:
        st.page_link(bck_page, label="b-room", icon="🧠", use_container_width=True)


def backtester() -> None:
    """Render the Backtester page."""
    st.title("Backtester")

    header_buttons()

    st.write("This is the page where the magic happens.")


def exchanges() -> None:
    """Render the Exchanges page."""
    st.title("Exchanges")
    header_buttons()

    st.write("This page shows data extracted from several crypto exchanges.")

    (tab1,) = st.tabs(["ByBit"])

    with tab1:
        with st.expander("Instruments"):
            container = st.container(border=True)
            (c1, c2) = container.columns([0.8, 0.2], vertical_alignment="center")

            c1.write("Do you want to populate the database with ByBit instruments?")
            c2.button(
                "Populate",
                type="primary",
                on_click=populate_bybit_instruments,
                use_container_width=True,
            )

            instruments = get_bybit_instruments()
            # Cast the dumped model to a concrete mapping type to avoid Any
            # propagation from pydantic's model_dump() stub in the type checker.
            table_rows = [
                cast(dict[str, object], i.model_dump()) for i in instruments[:5]
            ]
            st.table(table_rows)


@st.cache_data(ttl=60 * 60 * 24, show_spinner=False)
def get_bybit_instruments() -> list[Instrument]:
    """Fetch ByBit instruments from the database."""
    with Session(engine) as session:
        statement = select(Instrument).where(Instrument.exchange == "bybit")
        instruments = cast(list[Instrument], session.exec(statement).all())
    return instruments


def populate_bybit_instruments() -> None:
    """Populate the database with ByBit instruments."""
    logger.info("Populating ByBit instruments...")
    instruments = ByBitInstrument.fetch(ByBitCategory.LINEAR)

    with Session(engine) as session:
        for instrument in instruments:
            Instrument.from_bybit(instrument).upsert(session)
        session.commit()

    st.cache_data.clear()
    if instruments:
        logger.info(f"Fetched {len(instruments)} ByBit instruments.")
        st.success(f"Fetched {len(instruments)} ByBit instruments.")
    else:
        logger.warning("No ByBit instruments found.")
        st.warning("No ByBit instruments found.")


exc_page = st.Page(exchanges, icon="🔀")
bck_page = st.Page(backtester, icon="🧠")

if __name__ == "__main__":
    st.set_page_config(initial_sidebar_state="collapsed")
    st.navigation([exc_page, bck_page], position="hidden").run()
