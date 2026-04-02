# Implementation Plan: Analyze Style Mimicry vs Format Rigidity

**Branch**: `003-analyze-style-mimicry` | **Date**: 2026-04-02 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/003-analyze-style-mimicry/spec.md`

## Summary

Generate 50 break-news blogs on AI and Big Data to assess the generation agent's mimicry and structure. This will involve implementing a batch generation mechanism (`batch_generate.py`) using a static list of topics, and an evaluation layer (`structural_analyzer.py` and `style_judge.py`) combining deterministic HTML/Markdown structural variance checks and LLM-as-a-judge for validating the target author (Javipas) style imprint.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: `daggr`, `pytest`, OpenAI/Anthropic SDK, `beautifulsoup4`
**Storage**: Local JSON and Markdown/HTML files in `docs/posts/`
**Testing**: `pytest`
**Target Platform**: Local command-line execution and LLM execution.
**Project Type**: AI Content Generation Pipeline
**Performance Goals**: Support batch scheduling of 50 remote LLM invocations with strict exponential backoff (e.g., `tenacity`) and a `batch_status.json` file for checkpointing resilience.
**Constraints**: Must isolate LLM evaluation rules to `javipas_style_profile.json` boundaries.
**Scale/Scope**: 50 complete articles generated and 50 LLM evaluation calls in one pipeline run.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I (Python Pipeline Ownership)**: The batch runner and evaluation analyzer will be purely Python logic separated into focused scripts (`batch_generate.py`, `structural_analyzer.py`). -> **PASS**
- **Principle II (Reproducible Content Generation)**: The 50 topics are being baked into a static JSON input file to guarantee reproducible tests. Outputs and evaluation metrics are written strictly to text and markdown. State is checkpointed sequentially in `batch_status.json`. -> **PASS**
- **Principle III (Automated Verification First)**: New metric computation functions will be covered by `pytest`. Tests for `style_judge.py` must utilize mock LLM fixtures to avoid brittle remote execution. -> **PASS**
- **Principle IV (Provenance, Privacy, and Safe Output)**: The LLMs involved will operate securely under local API keys and won't commit sensitive details. -> **PASS**
- **Principle V (Static Delivery as the Canonical Publish Target)**: The tests output standard `.html` files in `docs/posts/` behaving like standard canonical deployments for evaluation. -> **PASS**

## Project Structure

### Documentation (this feature)

```text
specs/003-analyze-style-mimicry/
├── plan.md              
├── research.md          
├── data-model.md        
├── quickstart.md        
├── contracts/           
│   └── analyzer-cli.md
└── tasks.md             # To be generated
```

### Source Code (repository root)

```text
backend/
├── inputs/
│   └── 50_ai_bigdata_topics.json    # The static 50 topics
├── batch_status.json                # Runtime checkpoint tracking file
├── batch_generate.py                # Looping runner for daggr/orchestrator
├── structural_analyzer.py           # Counts tag variance across posts
└── style_judge.py                   # Calls LLM-as-a-judge with javipas_profile

docs/
├── COHERENCE_REPORT.md              # The output evaluation metric report
└── posts/                           # The target location of the 50 sample posts
```

## Complexity Tracking

N/A - The requirements clearly map to standard analytical Python scripts calling existing pipeline functions and LLM evaluation APIs. No major architecture changes are required.
