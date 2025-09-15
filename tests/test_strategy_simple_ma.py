import os
import sys


# Ensure `src` on sys.path
CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from strategies.example.simple_ma import SimpleMA


def test_simple_ma_strategy_trades_and_return() -> None:
    # Synthetic price series designed to create deterministic crosses
    prices = [100, 101, 102, 101, 103, 104, 103, 105, 104, 106]
    strat = SimpleMA(period=3)
    res = strat.backtest(prices)

    # Expect deterministic number of trades and return
    assert len(res.trades) == 4
    assert len(res.equity_curve) == len(prices)

    # Total return computed from trade sequence: approximately -1.94117647%
    assert abs(res.total_return - (-0.0194117647)) < 1e-9
