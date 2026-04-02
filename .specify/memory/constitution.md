<!--
Sync Impact Report
- Version change: template -> 1.0.0
- Modified principles:
	- template placeholder PRINCIPLE_1_NAME -> Python Pipeline Ownership
	- template placeholder PRINCIPLE_2_NAME -> Reproducible Content Generation
	- template placeholder PRINCIPLE_3_NAME -> Automated Verification First
	- template placeholder PRINCIPLE_4_NAME -> Provenance, Privacy, and Safe Output
	- template placeholder PRINCIPLE_5_NAME -> Static Delivery as the Canonical Publish Target
- Added sections:
	- Runtime and Dependency Standards
	- Workflow and Quality Gates
- Removed sections: none
- Templates requiring updates:
	- ✅ reviewed .specify/templates/plan-template.md (no content change required)
	- ✅ reviewed .specify/templates/spec-template.md (no content change required)
	- ✅ reviewed .specify/templates/tasks-template.md (no content change required)
- Follow-up TODOs: none
-->

# Blogger Agent TFG Constitution

## Core Principles

### I. Python Pipeline Ownership
All runtime generation, orchestration, scraping, transformation, and publishing logic MUST be
implemented in Python modules under the backend tree. Each agent, workflow, and orchestrator step
MUST have one clear responsibility and expose a small, testable interface.

Rationale: the repository is a content-generation pipeline; clear module boundaries reduce coupling
between agents and make failures local.

### II. Reproducible Content Generation
Every generated post MUST be traceable to explicit inputs: topic, source URLs, style corpus or
profile, and selected provider configuration. External model calls MUST be parameterized through
config, and their outputs, prompts, and derived artifacts MUST be persisted when they influence
published content.

Rationale: posts are generated artifacts that need auditability and repeatability.

### III. Automated Verification First
Any change that affects agents, orchestration, HTML building, scraping, publishing, or deployment
MUST include automated verification. Unit tests MUST cover individual components; integration or
end-to-end tests MUST cover the full pipeline or the affected cross-component boundary.

Rationale: regressions in multi-step content pipelines usually happen at interfaces, not isolated
functions.

### IV. Provenance, Privacy, and Safe Output
The system MUST keep source content, generated content, and deployment artifacts distinct. Scraped
text, news research, and prompts MUST preserve attribution where relevant and MUST NOT leak secrets,
tokens, or local environment details into generated output or repository files.

Rationale: the project mixes web scraping, LLM prompts, and static publishing, which creates
provenance and disclosure risks.

### V. Static Delivery as the Canonical Publish Target
The canonical public surface is the static site under docs/. Any publishing or deployment change
MUST preserve the consistency of docs/posts.json, generated post pages, and the GitHub Pages
subtree boundary. Backend changes that alter output schemas MUST be reflected in the static site
generation path before they are considered complete.

Rationale: GitHub Pages is the delivery mechanism, so static artifacts are the source of truth for
readers.

## Runtime and Dependency Standards

- The supported runtime is Python 3.11 or newer.
- Local development MUST use uv when available for environment creation and dependency
	installation.
- The dependency set MUST stay compatible with the declared backend tooling in pyproject.toml,
	including pytest, ruff, black, daggr, gradio, httpx, beautifulsoup4, lxml, pydantic,
	python-dotenv, and the configured LLM providers.
- Provider selection MUST use the repository's factory and fallback pattern. If a primary provider
	is unavailable, the code MUST fail with a clear error or fall back to an explicitly configured
	alternative.
- Network-bound operations MUST define timeouts and handle provider or scraping failures explicitly
	instead of relying on implicit retries.

## Workflow and Quality Gates

- A feature or fix is not complete until the relevant tests pass and the generated artifacts are
	validated locally.
- Changes to prompts, style profiles, corpus data, or output schemas MUST include a matching update
	to the docs or sample artifacts that depend on them.
- Deployment changes MUST be validated against the static publish path before release, including the
	docs/ subtree and any script that writes into it.
- If a proposed change violates this constitution, the constitution wins; the change MUST be
	redesigned before implementation.
- Any constitution amendment MUST update the version, ratification metadata, and sync report in the
	same change.

## Governance

This constitution overrides conflicting guidance in READMEs, prompts, task templates, and ad hoc
instructions. Amendments require a documented rationale, a semantic version bump, and an updated
sync impact report at the top of this file.

Versioning policy:
- MAJOR for principle removals, principle redefinitions, or backward-incompatible governance
	changes.
- MINOR for new principles or materially expanded standards.
- PATCH for clarifications, wording fixes, or non-semantic refinements.

Compliance review expectations:
- Spec, plan, and task generation MUST be checked against the constitution before implementation
	begins.
- Implementation review MUST reject changes that introduce hidden coupling, untested pipeline stages,
	leaked secrets, or unsafe publish behavior.
- Releases that alter generated output MUST include a local validation step for the affected artifact
	path.

**Version**: 1.0.0 | **Ratified**: 2026-04-02 | **Last Amended**: 2026-04-02
