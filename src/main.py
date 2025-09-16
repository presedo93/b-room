"""Streamlit app entrypoint for the b-room dashboard.

Stage 3 migration: wire pages through a registry and services. Old page
implementations remain in this file for now but are not used by default.
"""

import streamlit as st
from loguru import logger

from app import create_app_context
from pages.registry import PageSpec, build_pages
from pages.exchanges import make_exchanges_page
from pages.backtester import make_backtester_page


logger.level("DEBUG")
logger.add("room.log", retention="2 days")
logger.info("Dashboard started")


def _build_navigation_pages():
    ctx = create_app_context()

    specs = [
        PageSpec(title="Exchanges", icon="🔀", factory=make_exchanges_page),
        PageSpec(title="Backtester", icon="🧠", factory=make_backtester_page),
    ]
    return build_pages(ctx, specs)


if __name__ == "__main__":
    st.set_page_config(initial_sidebar_state="collapsed")
    pages = _build_navigation_pages()
    st.navigation(pages, position="hidden").run()
