# Feature Specification: Analyze Style Mimicry vs Format Rigidity

**Feature Branch**: `003-analyze-style-mimicry`  
**Created**: 2026-04-02  
**Status**: Draft  
**Input**: User description: "este proyecto trata de mimetizar escritura, genera 50 posts de topics actuales de bombazos de IA y big data y analiza si unicamente e esta siguiendo el mismo formato para cada articulo del blog y no está cumpliendo con la mimetizacion del autor"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Batch Generation of AI/Big Data Posts (Priority: P1)

As an AI practitioner evaluating the system, I want to automatically generate 50 blog posts about current breaking news in AI and Big Data, so that I have a statistically significant sample size to evaluate the agent's output.

**Why this priority**: Without the sample dataset of 50 posts, no stylistic analysis can be performed. This is the foundational prerequisite.

**Independent Test**: Can be fully tested by triggering the batch generation script and verifying that 50 markdown/HTML post files are created in the output directory, each with a unique topic related to AI or Big Data.

**Acceptance Scenarios**:

1. **Given** a list of 50 trending AI/Big Data topics (or an automated news gatherer), **When** the batch generation is triggered, **Then** the system successfully outputs 50 complete blog posts without failing.
2. **Given** the generated posts, **When** reviewing their content, **Then** all posts pertain to the specified AI and Big Data topics.

---

### User Story 2 - Style Mimicry vs. Template Rigidity Analysis (Priority: P1)

As a system evaluator, I want to analyze the 50 generated posts to determine if the agent is genuinely mimicking the author's voice or merely filling out a rigid, repetitive structural template.

**Why this priority**: This is the core objective of the feature: determining the quality and authenticity of the generation agent.

**Independent Test**: Can be tested by running the analysis tool against a known directory of text files and verifying it outputs a detailed report on structural variance and mimicry quality.

**Acceptance Scenarios**:

1. **Given** 50 generated posts, **When** the analysis tool is executed, **Then** it produces a report scoring the structural similarity (detecting if a rigid template is used).
2. **Given** the analysis report, **When** reading the mimicry evaluation, **Then** it provides actionable insights into whether the author's specific quirks, tone, and pacing are being properly replicated across different topics.

### Edge Cases

- What happens if the content generator fails or times out during the 50-post batch generation? (The system must use explicit exponential backoff (`tenacity`) and a checkpointing file `batch_status.json` to resume from the last successful post without killing the entire batch).
- How does the system handle topics that are heavily technical vs. highly opinionated when measuring style variance?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a mechanism to queue and generate 50 distinct blog posts based on breaking topics in AI and Big Data.
- **FR-002**: The system MUST analyze the structural similarity (e.g., heading placement, paragraph lengths, transition words) across the 50 posts to detect template rigidity.
- **FR-003**: The system MUST evaluate the linguistic style of the posts to verify alignment with the target author's (Javipas) specific stylistic fingerprint.
- **FR-004**: The system MUST output a comprehensive evaluation report (e.g., Markdown or JSON) summarizing the variance, template rigidity ratio, and mimicry success rate.
- **FR-005**: The evaluation process MUST use an LLM-as-a-judge system, provided with the target author's style profile, to score and analyze the posts.

### Key Entities

- **Batch Generation Task**: A configuration or script holding the 50 topics and tracking generation status.
- **Mimicry Evaluation Report**: The resulting artifact containing metrics on structural variance and stylistic fidelity.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 50 unique blog posts are generated natively by the pipeline.
- **SC-002**: An automated analysis report is generated that clearly quantifies the percentage of structural repetition vs. genuine stylistic variance, passing with a Variance Score > 0.7.
- **SC-003**: The report clearly flags if the system is defaulting to a rigid template (e.g., "Intro -> 3 Bullet Points -> Conclusion") instead of mimicking organic author structures, achieving an LLM average Mimicry Score > 0.8.

## Assumptions

- The target author whose style is being mimicked remains "Javipas" as defined in the current project corpus.
- The 50 topics can be statically provided or scraped easily; the core challenge is the generation and subsequent analysis.
- The existing pipeline (`daggr_blogger_workflow.py` or similar) can be adapted for batch processing without major architectural modifications.
