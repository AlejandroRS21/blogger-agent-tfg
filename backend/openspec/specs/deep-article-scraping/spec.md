# deep-article-scraping Specification

## Capability

deep-article-scraping

## Description

Scrapes full article content from URLs discovered by Brave Search using Scrapling's stealth HTTP Fetcher. Extracts clean text, removes HTML boilerplate, and returns structured results with graceful failure handling per URL.

## Priority

High

## Dependencies

None (consumes URLs from existing Brave Search, but does not depend on other new capabilities).

## Requirements

1. The system MUST accept a list of URLs (with title and source metadata) and scrape full article content from each one using Scrapling's `Fetcher` in stealth mode.

2. The system MUST extract clean text content — stripping HTML tags, navigation, ads, sidebars, and non-article boilerplate.

3. The system MUST process up to `max_articles` URLs (configurable, default: 5).

4. The system MUST set a per-URL timeout of 30 seconds to prevent hanging on slow sites.

5. The system MUST return structured per-article data containing: `title`, `source`, `url`, `full_text`, `word_count`, and `scrape_success`.

6. The system MUST truncate scraped text to 4096 tokens per article before synthesis to avoid LLM context limits.

7. The system MUST NOT fail entirely when individual URLs fail — partial results SHALL be returned for successfully scraped articles.

8. The system MUST handle the case of 0 input URLs gracefully — return an empty results list without errors.

## Scenarios

### Scenario: Happy path — all URLs scraped successfully

- GIVEN 5 URLs discovered by Brave Search, all pointing to accessible news articles
- WHEN the system scrapes each URL
- THEN all 5 return `scrape_success: true` with `full_text` and `word_count` populated
- AND no errors are logged

### Scenario: Partial failure — some URLs blocked

- GIVEN 5 URLs where 2 are behind Cloudflare/blocked and 3 are accessible
- WHEN the system scrapes each URL
- THEN 3 articles return `scrape_success: true` with full text
- AND 2 articles return `scrape_success: false` with no full text
- AND the system does NOT raise an exception

### Scenario: All URLs fail

- GIVEN 5 URLs where all are blocked or timeout
- WHEN the system scrapes each URL
- THEN all return `scrape_success: false`
- AND the system returns an empty list for downstream fallback

### Scenario: No URLs provided

- GIVEN Brave Search returned 0 results (empty URL list)
- WHEN the system attempts to scrape
- THEN scraping is skipped entirely
- AND an empty results list is returned immediately
