import streamlit as st

from sqlmodel import create_engine
from loguru import logger

from dashboard.exchanges import page as exc_page
from dashboard.backtester import page as bck_page

logger.add("xini.log", retention="2 days")
logger.info("Dashboard started")

engine = create_engine("sqlite:///xini.db")

if __name__ == "__main__":
    st.set_page_config(initial_sidebar_state="collapsed")

    pg = st.navigation(
        [
            st.Page(exc_page, title="exchanges", icon="🥇", url_path="exchanges/"),
            st.Page(bck_page, title="backtester", icon="🥈"),
        ],
    )

    pg.run()
