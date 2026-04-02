---
description: "Task list for Unifying testing documentation and test execution"
---

# Tasks: Unify testing documentation and test scripts coherency

**Input**: Design documents from `specs/002-unify-testing-docs/`
**Prerequisites**: plan.md, spec.md, research.md, contracts/test-cli.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure updates for proper pytest usage.

- [ ] T001 Update `backend/pyproject.toml` to include strict `[tool.pytest.ini_options]`, defining markers (`unit`, `integration`, `e2e`) and default arguments (like `asyncio_mode`).
- [ ] T002 [P] Create or update `backend/tests/conftest.py` with shared configurations for the pytest environment.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented. 

- [ ] T003 Refactor existing free-floating test scripts (`backend/test_full_pipeline.py`, etc.) into `backend/tests/` or prepare them for deprecation.
- [ ] T004 [P] Cleanup unstructured testing shells or powershell scripts that duplicate the test runner behavior.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - Centralized Testing Guide (Priority: P1) 🎯 MVP

**Goal**: Deliver a single, comprehensive `TESTING.md` file that effectively documents how to run and write tests across the repo.

**Independent Test**: Read `TESTING.md` and verify it contains clear copy-pasteable commands for all platforms (Windows, Linux, macOS) for unit, integration, and e2e testing.

### Implementation for User Story 1

- [ ] T005 [P] [US1] Create `TESTING.md` at the repository root covering the architecture, commands, and expected output.
- [ ] T006 [P] [US1] Remove redundant or outdated testing documentation from `README.md`.
- [ ] T007 [P] [US1] Remove redundant testing documentation from `backend/README.md`.
- [ ] T008 [US1] Cross-link `TESTING.md` in root `README.md` and `backend/README.md`.

**Checkpoint**: At this point, User Story 1 should be fully documented and centralized.

---

## Phase 4: User Story 2 - Coherent Test Execution (Priority: P1)

**Goal**: Standardize test script execution via a single entry point or standard pytest usage, replacing the multiple scattered scripts.

**Independent Test**: Execute `python backend/tests/run_tests.py --suite unit` or `pytest -m unit` and confirm only the relevant unit tests are triggered.

### Implementation for User Story 2

- [ ] T009 [P] [US2] Implement `backend/tests/run_tests.py` CLI script applying the contract defined in `specs/002-unify-testing-docs/contracts/test-cli.md`.
- [ ] T010 [US2] Apply `@pytest.mark.unit` to all appropriate test functions in `backend/tests/`.
- [ ] T011 [US2] Apply `@pytest.mark.integration` to all appropriate integration tests in `backend/tests/`.
- [ ] T012 [P] [US2] Apply `@pytest.mark.e2e` to end-to-end tests or full pipeline tests.
- [ ] T013 [US2] Update `backend/tests/test_agents.py` and `backend/tests/test_orchestrator.py` to ensure they run correctly within the new marker structure.

**Checkpoint**: At this point, running tests is centralized and categorized correctly.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect CI/CD and validation.

- [ ] T014 Update Github Actions workflows to invoke tests utilizing the new standard `pytest -m` commands or the `run_tests.py` wrapper.
- [ ] T015 Run validation scenarios mapped in `specs/002-unify-testing-docs/quickstart.md` to guarantee stability.

---

## Dependencies & Execution Order

### Phase Dependencies
- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup completion.
- **User Stories (Phase 3 & 4)**: Foundational phase MUST be complete before US2. US1 could technically start during Phase 2 since it is documentation.
- **Polish (Final Phase)**: Depends on US2 completion.

### Parallel Opportunities
- After Phase 1 & 2 are complete, US1 and US2 can be handled concurrently by different developers.
- Documentation cleanup tasks (T005-T007) inside US1 can run in parallel.
- Test marker assignments (T010-T012) inside US2 can be assigned and modified concurrently.

---

## Parallel Example: User Story 1

```bash
# Update multiple docs without overlap:
Task: T006 Remove redundant or outdated testing documentation from README.md
Task: T007 Remove redundant testing documentation from backend/README.md
```

## Implementation Strategy

### MVP First (User Story 1 + User Story 2 Setup)
1. Complete Setup and Foundational updates for Pytest configurations.
2. Complete US1 to define the target structure clearly in writing.
3. Complete US2 and map the codebase tests into unit/integration bounds.
4. Update CI/CD Actions to seal the pipeline guarantees.
