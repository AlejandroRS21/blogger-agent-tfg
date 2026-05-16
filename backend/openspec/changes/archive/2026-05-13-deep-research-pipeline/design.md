# Design: deep-research-pipeline

## Technical Approach

Replace the current Brave-only title-search research phase with a three-stage pipeline: **Brave Search → Scrapling Full-Text Scrape → LLM Synthesis**. The content generator receives a rich structured brief so post structure emerges from real data, not templates.

Key constraint: **zero orchestration refactoring**. Keep sync execution, reuse existing `ContentGenerator.llm` for synthesis, and degrade gracefully at every stage.

## Architecture Decisions

### Decision: Scrapling `Fetcher` over `DynamicFetcher`

| Option | Tradeoff | Decision |
|--------|----------|----------|
| `Fetcher` (stealth HTTP) | No JS rendering, but lighter weight, no browser deps | **Selected** — news articles work without JS |
| `DynamicFetcher` (Playwright) | Handles JS-rendered sites, but heavier, needs browser install | Rejected — unneeded complexity for text articles |

### Decision: Sync over async

| Option | Tradeoff | Decision |
|--------|----------|----------|
| Keep sync | Matches existing orchestrator, no `asyncio` refactor | **Selected** — orchestrator is blocking calls throughout |
| Convert to async | Better IO concurrency for N scrapes | Rejected — would require rewriting 7-phase pipeline |

### Decision: LLM reuse vs dedicated provider

| Option | Tradeoff | Decision |
|--------|----------|----------|
| Reuse `ContentGenerator.llm` | Zero extra config, same model & auth | **Selected** — synthesis is lightweight, no new secrets |
| New LLM provider instance | Could use cheaper model for synthesis | Rejected — config overhead outweighs savings |

### Decision: Fallback granularity

| Stage | On Failure | Rationale |
|-------|-----------|-----------|
| Brave Search | Return empty, `research_context=""` | No URLs discovered → nothing to scrape |
| Scrapling per URL | Log warning, skip URL | One blocked site ≠ all sites blocked |
| All Scrapling | Degrade to title-only (current behavior) | Better than mock data |
| LLM synthesis | Concatenate raw article text as brief | Raw data > empty output |

### Decision: Token limits

| Boundary | Limit | Why |
|----------|-------|-----|
| Per-article scraped text | 5,000 chars | Covers full article, fits most news content |
| Total scraped for synthesis | 15,000 chars | ~4K tokens, safe for Gemini/ GPT-4 context |
| Research brief output | 8,000 chars | Matches current `research_context[:8000]` ceiling in content_generator.py |

## Data Flow

```
topic ──► _search_brave() ──► URLs list
               │
               ▼
      _scrape_with_scrapling(url) ✕ max_articles
         ┌──────┼──────┐
         ▼      ▼      ▼
      [text1] [text2] [text3]  ← per-URL: max 5000 chars, skip on failure
               │
               ▼
      _synthesize_research(articles, llm_provider)
               │
               ▼
      Research brief (8000 chars) ──► state.metadata.research_context
                                          │
                                          ▼
                                   content_generator.generate_draft()
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `backend/requirements.txt` | Modify | Add `scrapling[fetchers]` |
| `backend/aphra_blogger/agents/news_research_agent.py` | Modify | Add `_scrape_with_scrapling`, `_synthesize_research`; update `research()` and `research_and_format_for_generation()` |
| `backend/src/orchestrator/main.py` | Modify | Update `_phase_research()` to pass LLM provider and store richer metadata |
| `backend/aphra_blogger/agents/content_generator.py` | Modify | Enhance prompt: "NO predetermined structure must EMERGE from research" |
| `backend/src/orchestrator/config.py` | Modify | Add `max_research_articles`, `max_scrape_chars_per_article`, `enable_deep_research` |
| `backend/modal_app.py` | No change | Scrapling auto-installed via `requirements.txt` |

## Interfaces / Contracts

### NewsResearchAgent — new & modified methods

```python
# NEW
def _scrape_with_scrapling(self, url: str) -> Optional[str]:
    """Scrape full article text via Scrapling Fetcher (stealth HTTP).
    Returns up to 5000 chars, or None on any failure."""

# NEW
def _synthesize_research(self, articles: List[Dict], llm_provider) -> str:
    """LLM synthesis of scraped articles into structured brief.
    Returns up to 8000 chars. Falls back to raw concatenation."""

# MODIFIED — new parameter + richer return
def research(self, topic: str, llm_provider=None, max_articles=5) -> Dict:
    """Full pipeline: search → scrape → synthesize.
    Returns dict with: topic, context, articles (with full_text),
    key_findings, scrape_stats: {total, succeeded, failed}."""

# MODIFIED — passes llm_provider through
def research_and_format_for_generation(self, topic: str, llm_provider=None) -> Dict:
```

### State metadata additions

```python
state.metadata['research_articles']   # List[Dict] — each now has 'full_text' key
state.metadata['research_synthesis']  # str — LLM-synthesized brief
state.metadata['research_context']    # str — SAME key, now holds synthesis output
state.metadata['scrape_stats']        # Dict — {total: int, succeeded: int, failed: int}
```

### Config additions (`OrchestratorConfig`)

```python
max_research_articles: int = 5
max_scrape_chars_per_article: int = 5000
enable_deep_research: bool = True  # toggle to disable scraping, use title-only
```

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | `_scrape_with_scrapling` with mock HTTP | Mock scrapling.Fetcher, verify truncation + error handling |
| Unit | `_synthesize_research` with mock LLM | Verify brief structure, fallback path on LLM failure |
| Unit | Updated `research()` with mocked sub-methods | Verify scrape_stats reporting, fallback chain |
| Integration | Full research pipeline (Brave → Scrapling → LLM) | End-to-end with real APIs, verify research_context is populated |
| Regression | Content generation with empty research | Verify existing fallback behavior unchanged |

## Migration / Rollout

No migration required. Feature-flag via `config.enable_deep_research`. When `False`, behavior reverts to current Brave-only flow. Rollback: revert `requirements.txt` + agent code + prompt changes.

## Open Questions

None. All design decisions are resolved in this document.
