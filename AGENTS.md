# Repository Guidelines

## Project Structure & Module Organization
- `src/main.py` boots the Streamlit UI; `src/app.py` and `src/db.py` expose shared factories.
- `src/pages/` hosts thin UI views; delegate logic to `src/services/` and domain layers.
- `src/services/`, `src/adapters/`, `src/persistence/`, `src/domain/`, and `src/strategies/` separate orchestration, I/O, storage, pure models, and trading logic.
- `tests/` mirrors service and strategy modules; add fixtures beside related tests.

## Build, Test, and Development Commands
- Install locally with `pip install -e .[test]` to pull runtime and tooling deps.
- Launch the app via `uv run streamlit run src/main.py` for an isolated environment.
- Validate code with `uv run ruff check src tests` and auto-format using `uv run ruff format`.
- Exercise the suite through `uv run pytest --cov=src --cov-report=term-missing -q` before every PR.

## Coding Style & Naming Conventions
- Follow standard Python: 4-space indents, type hints on public APIs, and guard main logic with functions.
- Keep modules and functions `snake_case`, classes `PascalCase`, and constants `UPPER_CASE`.
- Prefer dependency injection via services; avoid direct Streamlit or HTTP calls inside domain layers.
- Centralize logging with `loguru.logger` and keep user-facing copy in plain English.

## Testing Guidelines
- Write `pytest` unit tests in files named `test_*.py`; mirror the package under test.
- Use `respx` for HTTP client stubs and SQLModel sessions scoped per test to avoid cross-talk.
- Target ≥80% coverage on new code; include regression tests that reproduce any reported bug.
- Run `pytest -k` filters during development, but commit only when the full suite passes.

## Commit & Pull Request Guidelines
- Follow Conventional Commits (`type(scope): summary`), e.g., `feat(strategy): add rsi backtest`.
- Squash small fixes before review; ensure commit body links issues or documents trade-offs.
- PRs must describe behavior changes, list test commands, and attach UI screenshots when visuals shift.
- Confirm lint, tests, and Streamlit boot locally before requesting review.

## Security & Configuration Tips
- Never commit API keys or DB credentials; prefer local `.env` files loaded via environment variables.
- Reset or regenerate the sandbox SQLite files (`xini.db`) when sharing logs to avoid leaking sample data.
- Review dependency updates with `uv pip list --outdated` and address high-risk packages immediately.
