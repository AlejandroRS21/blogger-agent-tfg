# organic-content-generation Specification

## Capability

organic-content-generation

## Description

Enhances the Content Generator prompt to prioritize the research brief as the PRIMARY source of content, forbid predetermined section structures, derive section titles from research content, and produce different post structures for different topics while maintaining the blogger's style.

## Priority

Medium

## Dependencies

- research-synthesis (provides the research brief)
- Existing ContentGenerator LLM provider and style system (unchanged)

## Requirements

1. The system MUST use the research brief as the PRIMARY source of factual content — the LLM SHALL base all claims, dates, and references on the brief, not on training knowledge.

2. The system MUST explicitly forbid predetermined section titles in the prompt — titles like "Introducción", "Conclusión", "Análisis", "Desarrollo", or "Contexto" SHALL NOT appear unless the brief itself contains them.

3. The system MUST require that section titles be derived from the SPECIFIC content of the research brief — for example, if the brief mentions "regulación europea de IA", a section title could be "Lo que dice Europa" rather than a generic "Contexto legal".

4. The system MUST maintain the blogger's voice and style from `sample_text` — style matching rules from the existing prompt remain unchanged.

5. The system MUST produce DIFFERENT post structures for different topics — the same structural template SHALL NOT be reused across topics.

6. The system SHOULD apply the enhanced prompt even when only 1 article was scraped (minimal brief).

7. The system MUST fall back to the current behavior (style-only mode without research brief) when the research brief is empty — no generated post SHALL be lost due to missing research.

8. The system MUST still enforce all existing rules: no AI disclosure, conversational human tone, word count limits (min_words/max_words), keyword mentions, and no excessive markdown.

## Scenarios

### Scenario: Rich research brief drives custom structure

- GIVEN a research brief with extensive data (multiple facts, statistics, quotes from 3+ articles)
- WHEN `generate_draft` is called with this brief
- THEN the generated post has section titles derived from the research content (not generic)
- AND the structure differs from posts on other topics
- AND facts in the post can be traced back to the brief
- AND the blogger's voice from sample_text is maintained

### Scenario: Minimal research still avoids templates

- GIVEN a research brief with only 1 article's content
- WHEN `generate_draft` is called with this brief
- THEN the post still avoids generic section titles (no "Introducción"/"Conclusión")
- AND the brief data is still used as primary factual source
- AND the structure is NOT identical to other minimal-brief posts

### Scenario: No research brief — graceful fallback

- GIVEN the research brief is empty (no articles scraped)
- WHEN `generate_draft` is called
- THEN the system falls back to the current style-only prompt (no research block)
- AND the generated post still respects all existing rules (style, tone, keywords, length)
- AND no error is raised
