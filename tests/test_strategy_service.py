import os
import sys


# Ensure `src` on sys.path
CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from services.strategy_service import StrategyService


def test_strategy_service_runs_simple_ma_on_sample() -> None:
    svc = StrategyService.with_defaults()
    prices = svc.load_sample_dataset("BTCUSDT 1h (sample)")
    res = svc.run("Simple MA", prices)
    assert len(res.trades) == 4
    assert abs(res.total_return - (-0.0194117647)) < 1e-9

