---
description: "Task list for generating and evaluating 50 posts for format rigidity and style mimicry"
---

# Tasks: Analyze Style Mimicry vs Format Rigidity

**Input**: Design documents from `specs/003-analyze-style-mimicry/`
**Prerequisites**: plan.md, spec.md, research.md, contracts/analyzer-cli.md, data-model.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the static dataset required for reproducibility and dependencies.

- [X] T001 Update `backend/requirements.txt` / `pyproject.toml` to explicitly include `tenacity` for exponential backoff functionality.
- [ ] T002 [P] Create `backend/inputs/50_ai_bigdata_topics.json` and manually populate it with 50 distinct breaking news topics related to AI and Big Data.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Ensure the testing suite supports the LLM-as-a-judge tests safely without uncontrolled API spending.

- [ ] T003 Create a `pytest` LLM response mock fixture in `backend/tests/conftest.py` to intercept calls to OpenAI/Anthropic SDKs during unit testing.

**Checkpoint**: Core dependencies configured, topics locked, and secure testing mock available.

---

## Phase 3: User Story 1 - Batch Generation of AI/Big Data Posts (Priority: P1)

**Goal**: Automatically trigger and sequentially generate 50 standalone posts using the system pipeline without crashing.

**Independent Test**: Trigger the batch generation script and verify 50 generated posts are written to `docs/posts/`.

### Implementation for User Story 1

- [ ] T004 [US1] Create `BatchGenerationTask` state logic in `backend/batch_generate.py` that reads the input topics and initializes tracking via `backend/batch_status.json`.
- [X] T005 [US1] Implement exponential backoff (`tenacity`) wrapping the existing pipeline call (`daggr` / workflow orchestrator) inside `backend/batch_generate.py`.
- [X] T006 [US1] Integrate state persistence to update `backend/batch_status.json` on each post success/failure to support resumption from the last index.
- [X] T007 [US1] Add CLI interface in `backend/batch_generate.py` parsing `--input` and `--output` paths as defined in the CLI contract.
- [X] T008 [US1] Write unit tests in `backend/tests/test_batch_generate.py` verifying state recovery from a mocked `batch_status.json`.

**Checkpoint**: You can run `python backend/batch_generate.py` completely independently to generate corpus content.

---

## Phase 4: User Story 2 - Style Mimicry vs. Template Rigidity Analysis (Priority: P1)

**Goal**: Analyze 50 generated textual outputs using deterministic HTML/Markdown structure extraction and LLM qualitative scoring against the author's stylistic rulebook.

**Independent Test**: Execute `structural_analyzer.py` on a folder of texts and verify it outputs `COHERENCE_REPORT.md` returning valid format variances and mimicry scores (>0.7 and >0.8).

### Implementation for User Story 2

- [X] T009 [P] [US2] Implement `PostStructureMetrics` extraction logic inside `backend/structural_analyzer.py` utilizing `beautifulsoup4` or a markdown parser to tally headers, paragraphs, and list counts.
- [X] T010 [P] [US2] Create variance calculation logic in `backend/structural_analyzer.py` to yield a standard-deviation based structural variance score.
- [X] T011 [US2] Implement LLM-as-a-judge evaluation via `backend/style_judge.py` using `backend/javipas_style_profile.json` as the target rubric to score voice and tone.
- [X] T012 [US2] Tie `structural_analyzer.py` and `style_judge.py` execution together and map the consolidated outcomes to the `MimicryEvaluationReport` schema.
- [X] T013 [US2] Write the `COHERENCE_REPORT.md` markdown exporter utilizing the collected metrics and qualitative LLM observations.
- [ ] T014 [US2] Add CLI interface to `backend/structural_analyzer.py` honoring `--target` and `--report` arguments.
- [ ] T015 [US2] Write unit tests in `backend/tests/test_structural_analyzer.py` mocking deterministic string structures.
- [ ] T016 [US2] Write unit tests in `backend/tests/test_style_judge.py` testing prompt structure via the mock LLM fixtures created in Phase 2.

**Checkpoint**: Both generation and subsequent analysis frameworks run coherently.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Full-loop assessment and quality validation.

- [ ] T017 Run the complete generation pipeline mapping outlined in `specs/003-analyze-style-mimicry/quickstart.md` and commit the resulting `COHERENCE_REPORT.md`.
- [ ] T018 Verify no static LLM keys or sensitive variables were dumped into `docs/posts/` or the report file.

---

## Dependencies & Execution Order

### Phase Dependencies
- **Setup & Foundational (Phases 1-2)**: Can begin instantly. Foundational mocks MUST be in place before US2's LLM components.
- **User Story 1 & 2 (Phases 3-4)**: US2 has NO code dependency on US1 (Analyzer logic can be written entirely concurrently using dummy mock `.md` files). 
- **Polish (Phase 5)**: Requires actual `docs/posts/` generated efficiently by US1 logic and parsed by US2.

### Parallel Opportunities
- Teams can implement `batch_generate.py` (US1) AND `structural_analyzer.py` (US2) concurrently.
- Creating the `50_ai_bigdata_topics.json` (T002) can be done in parallel with `tenacity` pip installations (T001).
- Building the structural extraction heuristics (T009) can be decoupled and worked in parallel to the judge script (T011).

---

## Parallel Example: User Story 2

```bash
# Parallelizing structural extraction mapping away from qualitative style rating:
Task: T009 [P] [US2] Implement PostStructureMetrics extraction logic...
Task: T010 [P] [US2] Create variance calculation logic...
```
---

## Tech Debt Tasks (Generated by /speckit.cleanup)

**Generated**: 2026-04-02
**Source**: Post-implementation cleanup of 003-analyze-style-mimicry
**Priority**: Address before next feature iteration

### Detected Issues

- [X] TD001 [P] Refactor `backend/style_judge.py` to move `anthropic.Anthropic()` initialization inside `evaluate_style` or use lazy initialization to prevent import crashes and improve mockability.
- [X] TD002 [P] Add an explicit `timeout` parameter to `client.messages.create` in `backend/style_judge.py` to comply with the project Constitution regarding network-bound operations.
- [X] TD003 [P] Add a `try/except` block targeting file I/O operations inside `backend/structural_analyzer.py`'s `process_batch` method to seamlessly handle corrupt or inaccessible JSON files without crashing the loop.
- [X] TD004 Extract the hardcoded `JAVIPAS_URLS` list in `backend/batch_generate.py` into a configuration file, environment variable, or CLI argument.
