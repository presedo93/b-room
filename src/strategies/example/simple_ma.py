"""Simple Moving Average crossover (price vs SMA) example strategy.

Enter long when price crosses above SMA(N). Exit to flat when price crosses
below SMA(N). No shorting, one position max.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import override

from strategies.base import Strategy, StrategyResult, Trade


def _sma(values: Sequence[float], window: int) -> list[float]:
    window = max(1, int(window))
    out: list[float] = []
    s = 0.0
    for i, v in enumerate(values):
        s += v
        if i >= window:
            s -= values[i - window]
        if i + 1 < window:
            out.append(float("nan"))
        else:
            out.append(s / window)
    return out


@dataclass(slots=True)
class SimpleMA(Strategy):
    period: int = 3

    @property
    @override
    def name(self) -> str:  # pragma: no cover - trivial
        return f"SimpleMA({self.period})"

    @override
    def backtest(self, prices: Sequence[float]) -> StrategyResult:
        ma = _sma(prices, self.period)
        in_position = False
        entry_idx = -1
        entry_price = 0.0
        trades: list[Trade] = []
        equity: list[float] = []
        equity_val = 1.0  # start at 1.0 for multiplicative returns

        prev_above: bool | None = None
        for i, price in enumerate(prices):
            m = ma[i]
            above = price > m if m == m else False  # nan check: m==m is False for nan

            if prev_above is not None:
                # Cross up: (was below or equal) -> now above
                if not prev_above and above and not in_position:
                    in_position = True
                    entry_idx = i
                    entry_price = price
                # Cross down: (was above) -> now not above
                elif prev_above and not above and in_position:
                    in_position = False
                    trade = Trade(
                        entry_index=entry_idx,
                        exit_index=i,
                        entry_price=entry_price,
                        exit_price=price,
                    )
                    trades.append(trade)
                    equity_val *= 1.0 + trade.pnl
            prev_above = above
            equity.append(equity_val)

        # If we end in position, close at last price
        if in_position and entry_idx >= 0:
            price = float(prices[-1])
            trade = Trade(
                entry_index=entry_idx,
                exit_index=len(prices) - 1,
                entry_price=entry_price,
                exit_price=price,
            )
            trades.append(trade)
            equity_val *= 1.0 + trade.pnl
            equity[-1] = equity_val

        total_return = equity_val - 1.0
        return StrategyResult(
            trades=trades, total_return=total_return, equity_curve=equity
        )
