"""Backtester page skeleton.

Stage 3 provides only the UI scaffolding; strategy execution is integrated in
Stage 4.
"""

from typing import Callable

import streamlit as st

from app import AppContext
from services.strategy_service import StrategyService


def make_backtester_page(_: AppContext) -> Callable[[], None]:
    svc = StrategyService.with_defaults()

    def render_backtester() -> None:
        st.title("Backtester")
        st.caption("Select a strategy and dataset; then run a backtest.")

        with st.expander("Configuration", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                strategy = st.selectbox(
                    "Strategy",
                    options=svc.available_strategies(),
                    index=0,
                )
            with c2:
                dataset = st.selectbox(
                    "Dataset",
                    options=["BTCUSDT 1h (sample)", "ETHUSDT 1h (sample)"],
                    index=0,
                )

        run = st.button("Run Backtest", type="primary")
        if run:
            prices = svc.load_sample_dataset(dataset)
            result = svc.run(strategy, prices)
            st.success(
                f"Ran {strategy} on {dataset}. Trades={len(result.trades)}, Total Return={result.total_return:.2%}"
            )
            with st.expander("Trades"):
                if result.trades:
                    st.table(
                        [
                            {
                                "entry_index": t.entry_index,
                                "exit_index": t.exit_index,
                                "entry_price": t.entry_price,
                                "exit_price": t.exit_price,
                                "pnl": round(t.pnl, 6),
                            }
                            for t in result.trades
                        ]
                    )
                else:
                    st.info("No trades executed.")

    # Ensure unique callable name for Streamlit page routing
    render_backtester.__name__ = "backtester_page"
    return render_backtester
