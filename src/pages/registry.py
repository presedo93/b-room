"""Simple registry to build Streamlit pages with injected context/services."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

import streamlit as st

from app import AppContext
from persistence.repositories import InstrumentRepository
from services.exchange_service import ExchangeService


@dataclass(slots=True)
class PageSpec:
    title: str
    icon: str
    factory: Callable[[AppContext], Callable[[], None]]


def build_default_services(ctx: AppContext) -> dict[str, object]:
    """Create default service instances used by pages."""
    repo = InstrumentRepository()
    exchange_service = ExchangeService.with_defaults(ctx.session_factory, repo)
    return {
        "exchange_service": exchange_service,
    }


def build_pages(ctx: AppContext, pages: Iterable[PageSpec]) -> list[st.Page]:
    """Turn PageSpec entries into Streamlit `st.Page` instances.

    Each page factory receives the AppContext and should return a zero-arg
    callable suitable for `st.Page`.
    """
    st_pages: list[st.Page] = []
    for spec in pages:
        render = spec.factory(ctx)
        st_pages.append(st.Page(render, title=spec.title, icon=spec.icon))
    return st_pages
