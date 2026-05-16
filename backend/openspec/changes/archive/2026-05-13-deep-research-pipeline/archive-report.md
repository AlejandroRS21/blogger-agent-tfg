# Archive Report: deep-research-pipeline

**Change**: deep-research-pipeline
**Status**: archived
**Date**: 2026-05-13
**Phase Completing**: SDD cycle — fully planned, implemented, verified, archived

---

## Summary

Replaced the weak Brave-only title research with a deep research pipeline using Scrapling for stealth article scraping + LLM synthesis. The content generator now receives rich structured research briefs, so post structure emerges from real data instead of template patterns.

**3 new capabilities**:
1. **deep-article-scraping** — Scrapes full article content from Brave-discovered URLs via Scrapling `Fetcher` (stealth HTTP, no Playwright needed)
2. **research-synthesis** — LLM synthesis of scraped articles into structured research brief (key facts, perspectives, quotes, source list)
3. **organic-content-generation** — Enhanced generator prompt forcing structure-from-content, forbidding predetermined section titles

**Key design decisions**:
- Scrapling `Fetcher` (stealth HTTP) over `DynamicFetcher` (Playwright) — lighter weight, no browser deps
- Sync execution over async — matches existing orchestrator pattern
- Reused ContentGenerator LLM for synthesis — zero extra config
- Graceful fallback at every stage (Brave fails → empty, Scrapling per URL → skip, all Scrapling → degrade, LLM → raw concat)

---

## Files Changed

### Modified Files
| File | Action | Description |
|------|--------|-------------|
| `backend/requirements.txt` | Modified | Added `scrapling[fetchers]>=0.4.0` (line 37) |
| `backend/src/orchestrator/config.py` | Modified | Added 4 deep research config fields (`enable_deep_research`, `max_research_articles`, `max_scrape_chars_per_article`, `max_research_chars_total`) — lines 38-42 |
| `backend/aphra_blogger/agents/news_research_agent.py` | Modified | Full rewrite: added `_scrape_with_scrapling()` (lines 346-383), `_scrape_multiple_articles()` (lines 385-455), `_synthesize_research()` (lines 461-538), modified `research()` (lines 544-618) and `research_and_format_for_generation()` (lines 624-675), added `_build_context_from_result()` fallback (lines 677-701) |
| `backend/aphra_blogger/agents/content_generator.py` | Modified | Enhanced `generate_draft()` prompt with anti-template instructions: "No uses estructuras de plantilla", "Cada sección debe tener un título ESPECÍFICO", "La estructura debe surgir NATURALMENTE" — lines 133-143 |
| `backend/src/orchestrator/main.py` | Modified | Updated `_phase_research()` (lines 350-390) to pass LLM provider and store rich metadata (`research_synthesis`, `scrape_stats`); updated `_phase_content_generation_draft()` (lines 392-421) to use `research_synthesis` as primary context with fallback |

### New Files
| File | Description |
|------|-------------|
| `backend/tests/test_deep_research.py` | 37 unit tests covering deep research pipeline (672 lines) |

### OpenSpec Artifacts (Archived)
| Artifact | Path |
|----------|------|
| Proposal | `openspec/changes/archive/2026-05-13-deep-research-pipeline/proposal.md` |
| Design | `openspec/changes/archive/2026-05-13-deep-research-pipeline/design.md` |
| Spec: deep-article-scraping | `openspec/changes/archive/2026-05-13-deep-research-pipeline/specs/deep-article-scraping/spec.md` |
| Spec: research-synthesis | `openspec/changes/archive/2026-05-13-deep-research-pipeline/specs/research-synthesis/spec.md` |
| Spec: organic-content-generation | `openspec/changes/archive/2026-05-13-deep-research-pipeline/specs/organic-content-generation/spec.md` |
| Tasks | `openspec/changes/archive/2026-05-13-deep-research-pipeline/tasks.md` |
| Verify Report | `openspec/changes/archive/2026-05-13-deep-research-pipeline/verify-report.md` |
| Archive Report | `openspec/changes/archive/2026-05-13-deep-research-pipeline/archive-report.md` |

---

## Test Results

| Metric | Value |
|--------|-------|
| Tests (deep_research) | 37/37 passing |
| Tests (full suite) | 111/116 passing (4 pre-existing failures in `test_html_builder.py` — unrelated) |
| Test lines | 672 lines in `test_deep_research.py` |
| Test type | All unit-level with mocked dependencies |
| Tasks | 11/11 completed |
| Linter (ruff) | 0 critical errors, 207 warnings (mostly pre-existing W293 blank-line whitespace) |
| Coverage threshold | 0% (config) — pytest-cov not installed |

### Test Layer Distribution
| Layer | Tests |
|-------|-------|
| Unit | 37 |
| Integration | 0 |
| E2E | 0 |

### Key Test Areas
- `_scrape_with_scrapling`: successful scrape, HTTP error, connection error, empty content, truncation
- `_scrape_multiple_articles`: all success, partial failure, all fail, max_articles cap, empty URLs
- `_synthesize_research`: multiple articles, single article, empty articles, LLM fallback, output truncation
- `research()` pipeline: full pipeline, deep research disabled, no LLM provider
- `research_and_format_for_generation()`: llm_provider passthrough, backward compatibility
- Content generation: anti-template prompt verification (smoke), empty research fallback

---

## Spec Compliance

| Capability | Scenarios | Compliant | Partial |
|------------|-----------|-----------|---------|
| deep-article-scraping | 8 | 7 | 1 (token vs char limit — spec says 4096 tokens, code uses 5000 chars per design) |
| research-synthesis | 10 | 9 | 1 (same token vs char discrepancy) |
| organic-content-generation | 8 | 8 | 0 |
| **Total** | **26** | **24** | **2** |

---

## Key Metrics

| Metric | Value |
|--------|-------|
| Lines of code changed (estimate) | ~400+ (728-line news_research_agent.py with ~382 new/modified lines) |
| New dependencies | 1 (`scrapling[fetchers]>=0.4.0`) |
| Feature flag | `enable_deep_research: bool = True` (toggle to revert to Brave-only) |
| Scrapling version installed | 0.4.7 |
| Per-article scrape limit | 5,000 chars |
| Total scrape limit for synthesis | 15,000 chars |
| Synthesis output limit | 8,000 chars |
| Per-URL timeout | 30 seconds |
| Max articles processed | 5 (configurable) |

---

## Architecture Decisions (Recorded)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Scraping engine | Scrapling `Fetcher` (stealth HTTP) | No browser dependencies, news articles work without JS |
| Async vs sync | Sync | Matches existing orchestrator; avoids rewriting 7-phase pipeline |
| LLM for synthesis | Reuse `ContentGenerator.llm` | Zero extra config, same model and auth |
| Fallback granularity | Per-stage, per-URL | One blocked site ≠ all sites blocked |
| Token limits | 5K/15K/8K chars (not tokens) | Simplifies truncation; char-based is easier to debug |

---

## Lessons Learned

### Technical Insights

1. **Spec-design consistency matters**: The original spec specified limits in tokens (4096 tokens), but the design and code used characters (5000 chars). Token vs char counting is a common source of spec/code drift. Future specs should align with design docs on units.

2. **Scrapling `Fetcher` vs `DynamicFetcher`**: The stealth HTTP `Fetcher` was the right choice — it has zero system dependencies, installs pure Python. For news content, JS rendering is unnecessary. The 0.4.7 version worked without any `scrapling install` step.

3. **Feature flag pattern**: `enable_deep_research` toggle proved valuable — it allows instant rollback to Brave-only behavior without code changes. This is a recommended pattern for any phase that introduces external dependencies.

4. **Graceful degradation chain**: The multi-stage fallback (Brave → Scrapling → LLM → raw text → empty) means that every stage can fail independently without crashing the pipeline. This was validated by tests covering each failure mode.

5. **TDD without apply-progress**: The apply phase did not produce a formal `apply-progress` artifact with TDD cycle evidence. While the code is well-tested, this broke the strict TDD protocol. Future work should ensure the apply phase produces the required artifact.

### Gotchas Discovered

- `research()` method defaults to `max_articles=10` while `research_and_format_for_generation()` passes `max_articles=5`. Not a bug (the 5 takes precedence) but inconsistent defaults could cause confusion.
- Content generator tests in the existing suite exercise only the `_fallback_draft()` path (no LLM available in test environment). The anti-template instructions live in the LLM prompt, so they can't be directly tested without mocking.
- The `test_draft_prompt_contains_anti_template_instructions` test name is misleading — it's actually a smoke test that checks string output, not prompt content.

---

## Next Steps

1. **Add integration tests**: The current 37 tests are all unit-level with mocks. Consider adding integration tests that exercise the real Scrapling + LLM pipeline (opt-in, gated behind credentials).
2. **Add coverage tooling**: Install pytest-cov and add coverage thresholds to ensure new code maintains ≥80% coverage.
3. **Fix pre-existing `test_html_builder` failures**: 4 tests fail due to `jsx` attribute missing from `HTMLOutput`. These are unrelated to the deep-research-pipeline change.
4. **Create apply-progress artifact template**: Ensure future apply phases produce a formal TDD Cycle Evidence table to satisfy strict TDD protocol.
5. **Consider async refactor**: If the pipeline grows more external calls, converting to asyncio could improve throughput for N scrapes.

---

## Specs Synced to Main

| Domain | Action | Details |
|--------|--------|---------|
| deep-article-scraping | Created | 8 requirements, 4 scenarios (new spec — no prior main spec existed) |
| research-synthesis | Created | 8 requirements, 4 scenarios (new spec — no prior main spec existed) |
| organic-content-generation | Created | 8 requirements, 3 scenarios (new spec — no prior main spec existed) |

### Source of Truth Updated
The following specs now reflect the new behavior:
- `backend/openspec/specs/deep-article-scraping/spec.md`
- `backend/openspec/specs/research-synthesis/spec.md`
- `backend/openspec/specs/organic-content-generation/spec.md`

---

## SDD Cycle Complete

The deep-research-pipeline change has been fully planned, implemented, verified, and archived. Ready for the next change.
