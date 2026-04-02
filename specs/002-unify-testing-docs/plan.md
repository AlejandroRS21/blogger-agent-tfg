# Implementation Plan: Unify Testing Documentation and Scripts

**Branch**: `002-unify-testing-docs` | **Date**: 2026-04-02 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-unify-testing-docs/spec.md`

## Summary

Centralize testing documentation into a unified `TESTING.md` guide and consolidate fragmented test execution scripts into a coherent runner (`run_tests.sh` or `pytest` configuration), supporting targeted runs for unit and integration subsets.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: `pytest`, `pytest-asyncio`
**Storage**: N/A
**Testing**: `pytest`
**Target Platform**: Local development environments (Linux/Windows/macOS) and CI runners.
**Project Type**: AI Content Generation Pipeline (Python backend)
**Performance Goals**: N/A
**Constraints**: Documentation must be fully agnostic of specific OS bounds where possible, or document them clearly.
**Scale/Scope**: Entire project's test suite (unit and integration tests).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I (Python Pipeline Ownership)**: The tests primarily exercise the Python backend. Any test runner wrappers must respect the Python module boundaries and isolate testing configs. -> **PASS**
- **Principle III (Automated Verification First)**: This feature explicitly focuses on making automated verification coherent, improving its discoverability. -> **PASS**
- **Principle IV (Provenance, Privacy, and Safe Output)**: The testing docs must define safe execution without printing secrets. Mock execution modes must be documented. -> **PASS**

## Project Structure

### Documentation (this feature)

```text
specs/002-unify-testing-docs/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (N/A for docs)
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── test-cli.md      # Defines the wrapper/CLI test runner args
└── tasks.md             # Phase 2 output (generated via /speckit.tasks check)
```

### Source Code (repository root)

```text
.
├── backend/
│   ├── pyproject.toml       # Update pytest markers config
│   ├── pytest.ini           # Consolidate standard test vars (if needed)
│   ├── scripts/             # (New or consolidated)
│   │   └── run_tests.sh     # Unified execution runner
│   ├── TESTING.md           # The requested unified guide
│   ├── tests/               # Existing tests directory
│   └── (Remove or deprecate individual standalone scripts like test_full_pipeline.py by migrating them)
```

## Complexity Tracking

Not applicable (No Constitution Check violations or major technical debt additions planned for documentation).
