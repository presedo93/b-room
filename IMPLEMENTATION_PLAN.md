# Implementation Plan — Refactor for Pages, Exchanges, and Strategies

Created: 2025-09-14

Purpose
-------

This document defines a staged, incremental plan to refactor the project so it cleanly supports:

- Multiple Streamlit pages
- Multiple exchange adapters (ByBit, others)
- Pluggable trading strategies (for backtesting and live testing later)

Goals
-----

- Separate responsibilities into: domain models, persistence (repositories), exchange adapters, services (orchestrators), UI pages, and strategies.
- Make components small, testable and independently replaceable.
- Migrate incrementally: new modules added alongside current code until behavior is verified.

Status legend
-------------

- Not Started
- In Progress
- Completed
- Cancelled

Stages
------

## Stage 0: Preparation

**Goal**: Create the plan (this file) and prepare an application & DB session factory to be used by new modules.
**Estimate**: 1–2h
**Success Criteria**:

- IMPLEMENTATION_PLAN.md exists (this file).
- A db/session factory (src/db.py) and a lightweight app context factory (src/app.py) are available.

Tasks:

- 0.1 Create IMPLEMENTATION_PLAN.md — Completed (2025-09-14)
- 0.2 Create `src/db.py` (engine + session factory) — Completed (2025-09-15)
- 0.3 Create `src/app.py` (AppContext / factory for wiring repos, services) — Completed (2025-09-15)

Tests:

- Unit test for `get_session()` using a transient sqlite:///:memory: database that can create tables. — Completed (2025-09-15)

## Stage 1: Domain & Persistence

**Goal**: Extract pure domain models and implement a repository layer for Instruments.
**Estimate**: 4–6h
**Success Criteria**:

- `src/domain/models.py` created with a pure domain Instrument type.
- `src/persistence/models.py` contains SQLModel table(s) mirroring the current DB schema.
- `src/persistence/repositories.py` implements `InstrumentRepository` with `upsert_many`, `list_by_exchange`, and `get`.
- Unit tests for repository using in-memory SQLite.

Tasks:

- 1.1 Create `src/domain/models.py` (Instrument domain model) — Completed (2025-09-15)
- 1.2 Create `src/persistence/models.py` (SQLModel table definitions) — Completed (2025-09-15)
- 1.3 Implement `src/persistence/repositories.py` (InstrumentRepository) — Completed (2025-09-15)
- 1.4 Add tests for repo behaviors (upsert, list, get) using sqlite:///:memory: — Completed (2025-09-15)

Tests:

- Repository unit tests should use the session factory from `src/db.py`.

## Stage 2: Exchange Adapters & Service

**Goal**: Add an ExchangeClient interface and implement a ByBit adapter that returns domain DTOs. Implement ExchangeService that orchestrates fetch + persist.
**Estimate**: 4–8h
**Success Criteria**:

- `src/adapters/exchanges/base.py` defines `ExchangeClient` and `ExchangeInstrumentDTO`.
- `src/adapters/exchanges/bybit.py` implements the client and maps HTTP responses to `ExchangeInstrumentDTO`.
- `src/services/exchange_service.py` implements `populate_instruments(exchange, category)` and `list_instruments(exchange)` methods.
- Tests for adapter mapping (use `respx` to mock httpx) and for ExchangeService (mock repository).

Tasks:

- 2.1 Create `src/adapters/exchanges/base.py` — Completed (2025-09-15)
- 2.2 Create `src/adapters/exchanges/bybit.py` (wrap existing logic) — Completed (2025-09-15)
- 2.3 Implement `src/services/exchange_service.py` — Completed (2025-09-15)
- 2.4 Add tests for adapters (httpx/respx) and the service — Completed (2025-09-15)

Notes:

- Standardize on synchronous I/O for now (httpx sync) to keep pages simple. If you later move to async, do so across all adapters.

## Stage 3: Pages & Registry

**Goal**: Move Streamlit pages to call services only and register pages dynamically.
**Estimate**: 3–6h
**Success Criteria**:

- `src/pages/registry.py` provides a simple way to register pages and build the `st.navigation` list.
- `src/pages/exchanges.py` uses `ExchangeService.populate_instruments` and `ExchangeService.list_instruments`.
- `src/pages/backtester.py` provides the UI for selecting a strategy and dataset (strategy execution will be integrated in Stage 4).
- `main.py` simplified to create AppContext and run the registry-built pages. Keep old page implementations until migration is validated.

Tasks:

- 3.1 Create `src/pages/registry.py` — Completed (2025-09-15)
- 3.2 Create `src/pages/exchanges.py` that uses the ExchangeService — Completed (2025-09-15)
- 3.3 Create `src/pages/backtester.py` and wire it into the registry — Completed (2025-09-15)
- 3.4 Update `main.py` to use the page registry (non-destructive switch) — Completed (2025-09-15)
- 3.5 Add tests for page logic where possible (test service interactions rather than Streamlit UI) — Not Started

Notes:

- Keep pages thin: UI only. Business logic must live in services so it is unit-testable.

## Stage 4: Strategies & Backtester

**Goal**: Introduce a pluggable Strategy interface, a simple example strategy, and integrate it with the Backtester page.
**Estimate**: 4–8h
**Success Criteria**:

- `src/strategies/base.py` defines `Strategy` ABC with `backtest(historical_data)` and lifecycle hooks.
- `src/strategies/example/simple_ma.py` implements a simple moving-average strategy with deterministic outputs for tests.
- `src/services/strategy_service.py` can run strategies on datasets and return a result summary.
- Backtester page can select a strategy and run a backtest using historical data provided by a service or fixture.

Tasks:

- 4.1 Create `src/strategies/base.py` — Completed (2025-09-15)
- 4.2 Implement an example strategy `src/strategies/example/simple_ma.py` — Completed (2025-09-15)
- 4.3 Implement `src/services/strategy_service.py` to run strategies — Completed (2025-09-15)
- 4.4 Integrate strategy selection and execution in `src/pages/backtester.py` — Completed (2025-09-15)
- 4.5 Add unit tests for strategies using synthetic/historical data — Completed (2025-09-15)

Notes:

- Focus on deterministic behavior for strategy unit tests; separate performance considerations from correctness.

## Stage 5: Polish, Tests, and CI

**Goal**: Ensure test coverage, linters, and CI integration. Remove or archive old code after migration.
**Estimate**: 2–4h
**Success Criteria**:

- Tests covering adapters, repositories, services, and strategies exist and pass.
- Add/adjust CI workflow(s) if necessary to run tests and linters.
- Update README and remove redundant/old modules.

Tasks:

- 5.1 Add/extend tests across modules and ensure >80% coverage for core logic — Completed (2025-09-15)
- 5.2 Update CI (GitHub Actions) to run pytest and linting — Completed (2025-09-15)
- 5.3 Remove or archive old, replaced modules and update documentation — Completed (2025-09-15)

Migration & Safety Guidelines
-----------------------------

- Implement new modules alongside existing code. Do not delete or replace the original implementations until tests and manual validation pass.
- Use feature branches for each Stage (e.g., `feature/refactor-stage-1-domain-persistence`).
- Prefer small, incremental PRs that include tests.
- If a pre-commit hook modifies files during commit, amend the commit to include those changes (see repo rules).

Testing recommendations
-----------------------

- Use `sqlite:///:memory:` for repository tests. Create/drop tables in setup/teardown per test to keep tests isolated.
- Use `respx` to mock external `httpx` calls in adapter tests.
- Mock repositories in service tests to focus on orchestration behavior.
- Keep Streamlit UI logic untested at the UI rendering level; instead, test the underlying service business logic.

Conventions
-----------

- Follow existing project style: `black`/`ruff`/`mypy` where configured in pyproject.toml.
- Type hints on public functions and methods.
- Keep functions small and single-responsibility; test them.

ADR (short)
-----------

ADR-001: Introduce Adapter + Repository + Service architecture for exchanges and pages.

- Status: Proposed
- Reason: Current code couples UI, persistence, and exchange DTOs making it hard to add new exchanges/pages/strategies.
- Decision: Add ExchangeClient ABC, InstrumentRepository, Services, and keep UI pages thin.

Risks & Mitigations
-------------------

- Risk: Large refactor breaks behavior or slows progress. Mitigation: incremental migration and automated tests.
- Risk: Duplication during migration. Mitigation: delete old code only after tests and manual verification.

Immediate next steps (short-term)
---------------------------------

1. I can create `src/db.py` and `src/app.py` (session factory + AppContext) and a simple test for the session factory.
2. After that we can start Stage 1 (domain + persistence) by extracting a domain Instrument model and implementing the repository with tests.

How to update this plan
-----------------------

- Edit this file and update task statuses as you (or I) complete them.
- Prefer short notes when marking a task Completed (date and a 1-line summary of what changed).

If you'd like, I can start by implementing the immediate next step (create `src/db.py` and `src/app.py`) and add the unit test for the session factory. Should I proceed?
