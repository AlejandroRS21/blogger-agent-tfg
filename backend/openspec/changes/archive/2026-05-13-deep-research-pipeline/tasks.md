# Tasks: deep-research-pipeline

## Phase 1: Dependencies & Setup

- [x] **Task 1.1**: Add `scrapling[fetchers]>=0.4.0` to `backend/requirements.txt`
  - Verify: `pip install -r requirements.txt` succeeds; `import scrapling; from scrapling import Fetcher` works

- [x] **Task 1.2**: Add deep research config fields to `OrchestratorConfig` in `backend/src/orchestrator/config.py`
  - Add: `max_research_articles: int = 5`, `max_scrape_chars_per_article: int = 5000`, `enable_deep_research: bool = True`
  - Verify: `OrchestratorConfig()` creates with defaults; `config.enable_deep_research=False` disables scraping

## Phase 2: Deep Article Scraping (Capability 1)

- [x] **Task 2.1**: Add `_scrape_with_scrapling(url: str) -> Optional[str]` to `NewsResearchAgent` in `news_research_agent.py`
  - Import `Fetcher` from `scrapling`, stealth HTTP GET with 30s timeout, extract clean text via `get_all_text()`, truncate to `max_scrape_chars_per_article`
  - Handle: connection errors → return None, HTTP errors → return None, empty content → return None

- [x] **Task 2.2**: Add `_scrape_multiple_articles(urls: List[str], max_articles: int) -> List[Dict]` to `NewsResearchAgent`
  - Iterate URLs (up to `max_articles`), call `_scrape_with_scrapling()` per URL, skip failures with warning
  - Return per-article dicts: `{title, source, url, full_text, word_count, scrape_success}` + `scrape_stats: {total, succeeded, failed}`

## Phase 3: Research Synthesis (Capability 2)

- [x] **Task 3.1**: Add `_synthesize_research(articles: List[Dict], llm_provider) -> str` to `NewsResearchAgent`
  - Build LLM prompt from scraped texts to produce structured brief (key facts, dates/statistics, perspectives, quotes with source, numbered source list)
  - If 0 articles → return empty string (skip LLM call)
  - On LLM exception → fallback to raw concatenation of scraped text
  - Brief limited to 8000 chars

- [x] **Task 3.2**: Modify `research()` method — add `llm_provider=None, max_articles=5` params, integrate pipeline
  - Flow: `_search_brave()` → `_scrape_multiple_articles()` → `_synthesize_research()` (when `enable_deep_research=True`)
  - When `enable_deep_research=False`: skip scraping/synthesis, return current title-only behavior
  - Enrich returned dict/articles with `full_text`, `scrape_stats`, `research_synthesis`

- [x] **Task 3.3**: Update `research_and_format_for_generation()` — accept `llm_provider` param, pass through chain
  - Include `scrape_stats` and `research_synthesis` in returned dict
  - Ensure backward compatibility: callers without `llm_provider` still work (synthesis skipped)

## Phase 4: Enhanced Content Generation (Capability 3)

- [x] **Task 4.1**: Strengthen `generate_draft()` prompt in `content_generator.py`
  - Add: "La estructura del post debe surgir NATURALMENTE del contenido investigado. No fuerces una estructura predeterminada."
  - Add: "Cada título de sección debe ser ESPECÍFICO al contenido. Si el título pudiera aparecer en otro post, está mal."
  - Forbid predetermined titles: "Introducción", "Conclusión", "Análisis", "Desarrollo", "Contexto" as section headings
  - Ensure fallback to existing prompt when `research_context` is empty — no posts lost due to missing research

## Phase 5: Orchestrator Integration

- [x] **Task 5.1**: Update `_phase_research()` in `backend/src/orchestrator/main.py`
  - Pass `self.content_generator.llm` to research agent for synthesis
  - Store new metadata: `state.metadata['research_synthesis']`, `state.metadata['scrape_stats']`
  - Log richer progress messages: "Scraped X/Y articles, synthesis: N chars"
  - Respect `config.max_research_articles` when calling research

- [x] **Task 5.2**: Update `_phase_content_generation_draft()`
  - Read `research_synthesis` from `state.metadata`
  - If available, pass it as `research_context` to `generate_draft()`
  - If not available, fall back to existing `research_context`

## Phase 6: Modal Deployment Verification

- [x] **Task 6.1**: Verify `scrapling[fetchers]` installs in Modal deployment
  - No code change needed: Modal Image uses `pip_install_from_requirements(requirements.txt)` which picks up the new dep
  - Confirm: `Fetcher` (not `DynamicFetcher`) has no browser dependency, no `scrapling install` step needed
  - Verify by deploying and running a test workflow with `enable_deep_research=True`
