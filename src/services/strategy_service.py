"""Service to run strategies on datasets and return summaries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from strategies.base import Strategy, StrategyResult
from strategies.example.simple_ma import SimpleMA


def _default_strategies() -> dict[str, Strategy]:
    return {"Simple MA": SimpleMA(period=3)}


@dataclass(slots=True)
class StrategyService:
    strategies: Mapping[str, Strategy]

    @classmethod
    def with_defaults(cls) -> "StrategyService":
        return cls(strategies=_default_strategies())

    def available_strategies(self) -> list[str]:
        return list(self.strategies.keys())

    def run(self, strategy_name: str, prices: Sequence[float]) -> StrategyResult:
        try:
            strategy = self.strategies[strategy_name]
        except KeyError as exc:  # pragma: no cover - defensive
            raise ValueError(f"Unknown strategy: {strategy_name}") from exc
        return strategy.backtest(prices)

    def load_sample_dataset(self, name: str) -> list[float]:
        """Return a synthetic dataset for demos and tests."""
        if name == "BTCUSDT 1h (sample)":
            return [100, 101, 102, 101, 103, 104, 103, 105, 104, 106]
        if name == "ETHUSDT 1h (sample)":
            return [50, 49, 50, 51, 50, 52, 53, 52, 54, 55]
        # default deterministic sequence
        return [1, 1.1, 1.2, 1.15, 1.25]

