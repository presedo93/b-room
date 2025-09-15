"""Exchanges page using the ExchangeService."""

from __future__ import annotations

from dataclasses import asdict
from typing import Callable

import streamlit as st

from app import AppContext
from services.exchange_service import ExchangeService


def make_exchanges_page(ctx: AppContext) -> Callable[[], None]:
    services = _get_services(ctx)
    svc: ExchangeService = services["exchange_service"]

    def render_exchanges() -> None:
        st.title("Exchanges")
        st.write("This page shows data extracted from several crypto exchanges.")

        (tab1,) = st.tabs(["ByBit"])
        with tab1:
            with st.expander("Instruments"):
                container = st.container(border=True)
                (c1, c2) = container.columns([0.8, 0.2], vertical_alignment="center")

                c1.write("Do you want to populate the database with ByBit instruments?")
                if c2.button("Populate", type="primary", use_container_width=True):
                    count = svc.populate_instruments("bybit", "linear")
                    st.success(f"Fetched {count} ByBit instruments.") if count else st.warning("No ByBit instruments found.")

                instruments = svc.list_instruments("bybit")
                rows = [asdict(i) for i in instruments[:5]]
                if rows:
                    st.table(rows)
                else:
                    st.info("No instruments in the database yet.")

    # Ensure unique callable name for Streamlit page routing
    render_exchanges.__name__ = "exchanges_page"
    return render_exchanges


def _get_services(ctx: AppContext) -> dict[str, object]:
    # Lazily build default services; in future stages, allow injection/override.
    from pages.registry import build_default_services  # local import to avoid cycles

    return build_default_services(ctx)
