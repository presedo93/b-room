"""ByBit exchange data transfer objects and helpers.

This module contains pydantic models that mirror the ByBit API responses and
convenience helpers to fetch instrument lists from the public API.
"""

from __future__ import annotations

# Allow imports from third-party packages that may not be available in the
# linting environment.
# pylint: disable=import-error

from enum import Enum
from typing import Generic, TypeVar, ClassVar, cast

from loguru import logger
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

import httpx

T = TypeVar("T")


class ByBitResponse(BaseModel, Generic[T]):
    """Top-level response wrapper returned by ByBit."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        alias_generator=to_camel, validate_by_name=True, validate_by_alias=True
    )

    result: "ByBitResult[T]"


class ByBitResult(BaseModel, Generic[T]):
    """Result container for ByBit API responses."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        alias_generator=to_camel, validate_by_name=True, validate_by_alias=True
    )

    category: "ByBitCategory"
    instruments: list[T] = Field(alias="list")


class ByBitInstrument(BaseModel):
    """Pydantic model that represents a ByBit instrument record."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        alias_generator=to_camel, validate_by_name=True, validate_by_alias=True
    )

    symbol: str
    category: str | None = None
    base_coin: str
    quote_coin: str

    @classmethod
    def fetch(cls, category: "ByBitCategory") -> list["ByBitInstrument"]:
        """Fetch instruments from ByBit API for the requested category.

        Returns a list of ByBitInstrument DTOs built from the API response.
        """
        logger.info(f"ByBit instruments fetch started for {category}")

        endpoint = "https://api.bybit.com/v5/market/instruments-info"
        params = {"category": category.value}

        response = httpx.get(endpoint, params=params)
        response.raise_for_status()

        logger.trace(f"ByBit instruments fetch response: {response.text}")
        # model_validate may be untyped at the stub level; cast to the expected
        # pydantic model so the type checker doesn't propagate Any.
        result = cast(
            ByBitResponse["ByBitInstrument"],
            ByBitResponse["ByBitInstrument"].model_validate(response.json()),
        )

        # Determine a sensible category string. The API may return the category
        # either as a plain string or it may already be parsed into a ByBitCategory
        # enum by pydantic. Handle both cases and prefer a per-instrument
        # category when available.
        top_cat_raw = result.result.category
        top_category = (
            top_cat_raw.value if hasattr(top_cat_raw, "value") else str(top_cat_raw)
        )

        def _item_category(item: "ByBitInstrument") -> str:
            item_cat_raw = getattr(item, "category", None)
            if item_cat_raw is None:
                return top_category
            return (
                item_cat_raw.value
                if hasattr(item_cat_raw, "value")
                else str(item_cat_raw)
            )

        return [
            cls(
                symbol=d.symbol,
                base_coin=d.base_coin,
                quote_coin=d.quote_coin,
                category=_item_category(d),
            )
            for d in result.result.instruments
        ]


class ByBitCategory(str, Enum):
    """Enumeration of ByBit API categories."""

    SPOT = "spot"
    LINEAR = "linear"
    INVERSE = "inverse"
    OPTION = "option"

    @classmethod
    def from_str(cls, category: str) -> "ByBitCategory":
        """Convert a string to a ByBitCategory enum in a case-insensitive way."""
        return cls(category.lower())
