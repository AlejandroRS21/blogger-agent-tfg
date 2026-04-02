# Research & Decisions: Style Mimicry vs Format Rigidity

## 1. 50 Topics Generation
**Decision**: Use a static JSON file (`backend/inputs/50_ai_bigdata_topics.json`) containing 50 breaking news topics on AI and Big Data.
**Rationale**: Ensures reproducibility (Constitution Principle II) and isolates the generation/analysis from the unpredictability of a live news scraper.
**Alternatives considered**: Live web scraping for 50 breaking news articles (rejected due to instability and potential rate limits for batch testing).

## 2. Batch Generation Mechanism
**Decision**: Create a `backend/batch_generate.py` script that iterates over the 50 topics, invoking the existing pipeline for each, with error handling to resume on failure.
**Rationale**: Reuses the tested pipeline (`daggr_blogger_workflow.py` or similar) while adding batch-specific resilience.
**Alternatives considered**: Modifying the existing pipeline directly (rejected to adhere to Single Responsibility and avoid breaking existing single-post flows).

## 3. Measuring Template Rigidity (Structural Variance)
**Decision**: Create a Python heuristic script (`backend/structural_analyzer.py`) that counts structural elements (h2/h3 tags, paragraph counts, list counts) and calculates standard deviation/variance across the 50 posts. Low variance = rigid template.
**Rationale**: LLMs can be subjective about "format"; extracting hard structural counts (HTML/Markdown elements) is deterministic and easily quantified.
**Alternatives considered**: Asking the LLM if the formats are the same (rejected because LLMs struggle to hold 50 full posts in context to compare their lengths and heading counts accurately).

## 4. LLM-as-a-Judge for Stylistic Mimicry
**Decision**: Create `backend/style_judge.py` using an LLM provider (e.g., OpenAI/Anthropic). It will receive the `javipas_style_profile.json` as the rubrics, and the text of a generated post, returning a JSON evaluation of how well it mimics the specific quirks, voice, and tone.
**Rationale**: Directly fulfills FR-005. LLMs excel at qualitative tone analysis when prompted with a structured rubric.
**Alternatives considered**: Traditional NLP stylistic classification (e.g., word frequencies) (rejected as it struggles to capture nuanced pacing or author "voice").
