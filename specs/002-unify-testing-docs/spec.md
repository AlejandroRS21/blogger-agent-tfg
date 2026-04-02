# Feature Specification: Unify Testing Documentation and Scripts

**Feature Branch**: `002-unify-testing-docs`  
**Created**: 2026-04-02  
**Status**: Draft  
**Input**: User description: "Unify testing documentation, create test scripts coherency..."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Centralized Testing Guide (Priority: P1)

As a developer contributing to the project, I want a single, coherent testing guide so that I know exactly how to run unit, integration, and E2E tests without hunting across multiple READMEs.

**Why this priority**: Without central documentation, contributors lose time trying to understand which tests to run and how to configure them, leading to broken builds or untested code.

**Independent Test**: Can be fully tested by verifying a new contributor (or AI agent) can execute the full suite solely by following the instructions in the new unified documentation.

**Acceptance Scenarios**:

1. **Given** a fresh checkout of the repository, **When** I look for testing instructions, **Then** I find a clear, unified `TESTING.md` document detailing all test tiers.
2. **Given** the need to configure tests locally, **When** I read the guide, **Then** it clearly lists all required environment variables (e.g., API keys) and setup steps.

---

### User Story 2 - Coherent Test Execution (Priority: P2)

As a developer or CI pipeline operator, I want standard, predictable commands to run all tests or specific subsets (unit vs integration) so that test execution is coherent and unified.

**Why this priority**: Fragmented scripts (like `test_full_pipeline.py`, `run_tests.py`, etc.) create confusion over what constitutes a "passing build." Unifying execution standardizes the process.

**Independent Test**: Can be validated by executing a unified entry script or standardized commands (e.g., via `pytest` markers or a central shell script) that triggers exactly the requested test suite without ambiguity.

**Acceptance Scenarios**:

1. **Given** the need to run only unit tests, **When** I trigger the standard test command for units, **Then** only the fast unit tests run.
2. **Given** the need to run full pipeline integration tests, **When** I execute the integration test command, **Then** the end-to-end flow is tested coherently.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The repository MUST provide a single unified testing documentation file (`TESTING.md` or dedicated `project_docs/TESTING.md`) covering all test types.
- **FR-002**: The project MUST provide coherent, standardized execution paths or scripts for all tests, replacing or wrapping any currently fragmented scripts.
- **FR-003**: The test execution convention MUST support distinct execution subsets for unit tests versus end-to-end integration tests.
- **FR-004**: The documentation MUST describe the required tools and environment variables for local testing (e.g., LLM provider keys).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of existing standalone test scripts are either documented in the unified guide or consolidated into a unified runner.
- **SC-002**: A developer can discover and successfully execute the primary test suite locally within 2 minutes of reading the new documentation.
- **SC-003**: Elimination of undocumented or duplicate test execution scripts in the repository root or backend folder.

## Assumptions

- The test suite technology remains `pytest`; we are not migrating to a new testing framework, only improving the documentation and invocation coherency.
- The existing tests pass; this feature is focused on documentation and coherency, not necessarily fixing failing tests.
- Standard project variables (like `HF_TOKEN` or `OPENAI_API_KEY`) will suffice for integration test configuration if documented correctly.

### Edge Cases
- What happens if tests are run without API keys? (The guide should point to mock-mode execution or how to handle missing vars).
- What happens if a developer is on Windows vs Linux? (The execution paths should ideally cover both OS, or abstract it in the unified scripts).
