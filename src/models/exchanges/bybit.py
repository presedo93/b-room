"""ByBit exchange data transfer objects and helpers.

This module contains pydantic models that mirror the ByBit API responses and
convenience helpers to fetch instrument lists from the public API.
"""

# Allow imports from third-party packages that may not be available in the
# linting environment.
# pylint: disable=import-error

from enum import Enum
from typing import Generic, TypeVar

from loguru import logger
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

import httpx

T = TypeVar("T")


class ByBitResponse(BaseModel, Generic[T]):
    """Top-level response wrapper returned by ByBit."""

    model_config = ConfigDict(
        alias_generator=to_camel, validate_by_name=True, validate_by_alias=True
    )

    result: "ByBitResult[T]"


class ByBitResult(BaseModel, Generic[T]):
    """Result container for ByBit API responses."""

    model_config = ConfigDict(
        alias_generator=to_camel, validate_by_name=True, validate_by_alias=True
    )

    category: "ByBitCategory"
    list: list[T]


class ByBitInstrument(BaseModel):
    """Pydantic model that represents a ByBit instrument record."""

    model_config = ConfigDict(
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
        result = ByBitResponse[ByBitInstrument].model_validate(response.json())
        _ = ByBitCategory.from_str(result.result.category)

        return [
            cls(
                symbol=d.symbol,
                base_coin=d.base_coin,
                quote_coin=d.quote_coin,
                category="spot",
            )
            for d in result.result.list
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
