# Research: Unify Testing Documentation

## 1. How to run tests consistently (Linux vs Windows)
**Decision**: Use `pytest` natively with CLI markers (`-m integration`, `-m unit`) or a simple agnostic `run_tests.py` runner script instead of bash/powershell duopoly.
**Rationale**: Python acts as its own runner and is inherently cross-platform. Writing wrappers in bash excludes Windows contributors without WSL, while writing them in Python supports all users out of the box.
**Alternatives considered**: Managing `run_tests.ps1` and `run_tests.sh` (like the setup scripts do), but this doubles maintenance. `Makefile` - requires `make` installation on Windows.

## 2. API Key Dependencies for End-to-End Tests
**Decision**: The unified document will specify required `.env` paths and recommend a mock test configuration (where applicable, e.g., setting `USE_MOCK=true` or passing `HF_TOKEN="dummy" pytest -m unit`).
**Rationale**: Aligns explicitly with Principle IV (Safety/Privacy/Mocking). The tests should never fail just because of external API unavailability on CI if we are only testing unit logic.
**Alternatives considered**: Requiring real API keys for all test runs (rejected as it degrades developer onboarding time).
