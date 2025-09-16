from services.strategy_service import StrategyService


def test_strategy_service_runs_simple_ma_on_sample() -> None:
    svc = StrategyService.with_defaults()
    prices = svc.load_sample_dataset("BTCUSDT 1h (sample)")
    res = svc.run("Simple MA", prices)
    assert len(res.trades) == 4
    assert abs(res.total_return - (-0.0194117647)) < 1e-9
