import streamlit as st

from sqlmodel import create_engine
from loguru import logger

from models.exchanges.bybit import ByBitInstrument, ByBitCategory

logger.add("xini.log", retention="2 days")
logger.info("Dashboard started")

engine = create_engine("sqlite:///xini.db")


def header_buttons():
    c1, _, c3 = st.columns(3)

    with c1:
        st.page_link(exc_page, label="exchanges", icon="🔀", use_container_width=True)

    with c3:
        st.page_link(bck_page, label="b-room", icon="🧠", use_container_width=True)


def backtester():
    st.title("Backtester")

    header_buttons()

    st.write("This is the page where the magic happens.")


def exchanges():
    st.title("Exchanges")
    header_buttons()

    st.write("This page shows data extracted from several crypto exchanges.")

    (tab1,) = st.tabs(["ByBit"])

    with tab1:
        with st.expander("Instruments"):
            instruments = ByBitInstrument.fetch(ByBitCategory.SPOT)
            st.table([i.model_dump() for i in instruments])


exc_page = st.Page(exchanges, icon="🔀")
bck_page = st.Page(backtester, icon="🧠")

if __name__ == "__main__":
    st.set_page_config(initial_sidebar_state="collapsed")

    st.navigation([exc_page, bck_page], position="hidden").run()
