"""Strategy interfaces and result types."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(slots=True)
class Trade:
    entry_index: int
    exit_index: int
    entry_price: float
    exit_price: float

    @property
    def pnl(self) -> float:
        # Simple return for a long trade
        if self.entry_price == 0:
            return 0.0
        return (self.exit_price - self.entry_price) / self.entry_price


@dataclass(slots=True)
class StrategyResult:
    trades: list[Trade]
    total_return: float
    equity_curve: list[float]


class Strategy(ABC):
    """Base interface for strategies."""

    @property
    @abstractmethod
    def name(self) -> str: ...

    def configure(self, **_params: object) -> None:  # pragma: no cover - default no-op
        """Optional configuration hook."""
        return None

    @abstractmethod
    def backtest(self, prices: Sequence[float]) -> StrategyResult:
        """Run the strategy on a sequence of close prices."""
        ...
