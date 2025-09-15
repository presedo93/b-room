"""Pure domain models.

This module defines dataclasses representing core domain entities, independent
from persistence or external adapter DTOs.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Instrument:
    """Domain representation of a tradable instrument."""

    exchange: str
    name: str
    kind: str
    base: str
    quote: str

