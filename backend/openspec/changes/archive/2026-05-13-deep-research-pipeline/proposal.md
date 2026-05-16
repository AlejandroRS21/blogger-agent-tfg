# Proposal: deep-research-pipeline

## Intent

**Why**: The research phase (Phase 3) only retrieves titles + 1-line descriptions from Brave Search API. The content generator receives near-empty data, so the LLM falls back to generic template structures. Users report posts look identical ("estructura siempre igual").

**What**: Replace the weak Brave-only title search with a deep research pipeline that discovers URLs, scrapes full article content with Scrapling, and synthesizes it via LLM into a structured research brief.

**Success**: Generated posts have unique structure dictated by real research content, not template patterns.

## Scope

### In Scope
- Add `scrapling[fetchers]` to `backend/requirements.txt`
- Refactor `NewsResearchAgent` with deep scraping (`_scrape_article_content`) using Scrapling `Fetcher` (stealth HTTP)
- Add LLM synthesis step (`_synthesize_research`) to produce structured brief from scraped content
- Update orchestrator research phase (`_phase_research`) for richer data flow
- Improve `content_generator.py` prompt to emphasize structure-from-content
- Ensure Scrapling is installed in Modal deployment image

### Out of Scope
- Frontend changes
- New agents (reuse existing ContentGenerator LLM)
- Changes to style analysis, keyword extraction, critique, HTML building, or image selection
- Database schema changes

## Capabilities

### New Capabilities
- `deep-research`: Full-article scraping + LLM synthesis pipeline producing structured research briefs

### Modified Capabilities
- None — no existing specs are affected at the requirement level

## Approach

1. **Dep**: Add `scrapling[fetchers]` to requirements.txt; Modal auto-installs via `pip_install_from_requirements`
2. **Refactor `NewsResearchAgent`**:
   - Keep Brave Search for URL discovery (existing `_search_brave`)
   - Add `_scrape_article_content(url)` using Scrapling `Fetcher` (stealth HTTP, Playwright-free)
   - Add `_synthesize_research(scraped_articles)` reusing ContentGenerator's LLM for summary + key points
   - Fallback chain: Brave → Scrapling → graceful degradation (no mock data)
3. **Orchestrator**: `_phase_research` passes richer `ResearchResult` with full article content to state
4. **Content prompt**: Strengthen "baseate en la información real" instruction; add "no estructuras genéricas" emphasis

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `backend/requirements.txt` | Modified | Add `scrapling[fetchers]` |
| `backend/aphra_blogger/agents/news_research_agent.py` | Modified | Add deep scrape + LLM synthesis methods |
| `backend/src/orchestrator/main.py` | Modified | Richer research data flow in `_phase_research` |
| `backend/aphra_blogger/agents/content_generator.py` | Modified | Strengthen prompt for organic structure |
| `backend/modal_app.py` | Unchanged | Scrapling auto-installed via requirements.txt |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Sites block Scrapling fetcher | Medium | Graceful skip per URL; fall through to remaining articles |
| Modal 60s timeout with N scrapes | Low | Timeout per scrape; configurable batch size; existing 600s Modal timeout |
| Large scraped content hits LLM token limits | Medium | Truncate scraped text to 4K tokens per article before synthesis |

## Rollback Plan

1. Revert `requirements.txt` — remove `scrapling[fetchers]`
2. Revert `news_research_agent.py` — restore original Brave-only implementation
3. Revert `main.py` — restore original `_phase_research`
4. Revert `content_generator.py` — restore original prompt

## Dependencies

- `scrapling[fetchers]` — MIT license, pure Python, no Playwright/headless browser needed
- Existing LLM provider (Gemini/OpenAI) — reused for synthesis step

## Success Criteria

- [ ] `NewsResearchAgent` scrapes ≥80% of Brave-discovered URLs successfully
- [ ] Scraped content appears verbatim in `research_context` passed to `generate_draft`
- [ ] Generated posts pass manual inspection for non-template structure (no "Introducción"/"Conclusión" forced sections)
- [ ] All existing tests pass; no regressions in non-research phases
