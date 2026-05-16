# research-synthesis Specification

## Capability

research-synthesis

## Description

Takes scraped articles from deep-article-scraping and uses the existing ContentGenerator LLM provider to synthesize a structured research brief. The brief contains key facts, statistics, perspectives, quotes, and source list — formatted for direct injection into the content generator prompt.

## Priority

High

## Dependencies

- deep-article-scraping (provides scraped article content)

## Requirements

1. The system MUST accept the list of scraped articles (title, source, url, full_text) from deep-article-scraping as input.

2. The system MUST reuse the existing ContentGenerator's LLM provider for the synthesis call (same provider, no new credentials).

3. The system MUST produce a structured research brief containing: key facts, dates/statistics found, different perspectives on the topic, relevant quotes (with source), and a numbered source list with URLs.

4. The system MUST format the brief as a plain-text block ready for direct injection into the content generator's prompt.

5. The system SHOULD limit the synthesized brief to 4096 tokens to stay within prompt budgets.

6. The system MUST handle the case where 0 articles were scraped — skip the LLM synthesis call entirely and return an empty brief.

7. The system MUST handle LLM provider failure — when the synthesis call raises an exception, fall back to a simple concatenation of raw scraped text as the brief.

8. The system MUST include source URLs in the brief so the content generator can reference them.

## Scenarios

### Scenario: Happy path — multiple articles synthesized

- GIVEN 3 articles were successfully scraped with full text content
- WHEN the LLM synthesis call completes
- THEN the brief contains key facts, dates, perspectives, quotes, and a source list
- AND the brief is under 4096 tokens

### Scenario: Single article only

- GIVEN only 1 article was successfully scraped
- WHEN the LLM synthesis call completes
- THEN the brief is shorter but still contains structured sections (facts, perspectives, source)
- AND it is still usable as research context

### Scenario: No articles scraped

- GIVEN 0 articles were successfully scraped (all failed or empty URL list)
- WHEN the system attempts synthesis
- THEN the LLM call is skipped entirely
- AND an empty brief is returned

### Scenario: LLM provider failure during synthesis

- GIVEN scraped articles are available
- WHEN the LLM synthesis call raises an exception (timeout, API error, rate limit)
- THEN the system catches the error
- AND falls back to returning concatenated raw scraped text as the brief
