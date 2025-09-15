# b-room

Streamlit app and library for exploring exchange instruments and backtesting
simple trading strategies.

## Quick Start

Prerequisites: Python 3.13.

Install dependencies (editable, with test extras):

```bash
pip install -e .[test]
```

Run the app:

```bash
uv run streamlit run src/main.py
```

Run tests with coverage:

```bash
pytest --cov=src --cov-report=term-missing -q
```

## Architecture

- `src/pages/*`: Thin Streamlit pages. Use services only.
- `src/services/*`: Orchestration/business logic (exchanges, strategies).
- `src/adapters/exchanges/*`: Exchange clients that normalize external data.
- `src/persistence/*`: SQLModel tables and repositories.
- `src/domain/*`: Pure domain models, independent of persistence/adapters.
- `src/strategies/*`: Strategy interfaces and example implementations.
- `src/app.py`, `src/db.py`: App and DB session factories.
