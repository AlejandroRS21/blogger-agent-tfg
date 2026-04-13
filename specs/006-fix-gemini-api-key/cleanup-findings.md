## Cleanup Findings: 006-fix-gemini-api-key

### Critical Issues (BLOCKING)
*None detected.*

### Small Issues (Propose to fix now)
| # | File | Issue | Proposed Fix |
|---|------|-------|--------------|
| 1 | `backend/aphra_blogger/agents/html_builder.py` | Debug print statements in `if __name__ == '__main__':` block | These are for manual testing, but could be cleaner if they used logging or were removed. However, since they are in a main block, I will keep them as intentional for dev. |
| 2 | `backend/aphra_blogger/llm/factory.py` | Redundant `os.getenv` calls for `GEMINI_API_KEY`/`GOOGLE_API_KEY` | Refactor to prioritize passed `api_key` and use consistent env var names. (Actually already handles this reasonably, but could be tighter). |

### Medium Issues (Will create tasks)
| # | File | Issue | Task Description |
|---|------|-------|------------------|
| 1 | `backend/aphra_blogger/llm/gemini_provider.py` | `google-generativeai` deprecation warning | Migrate from `google-generativeai` to `google-genai` package. |
| 2 | `backend/src/orchestrator/main.py` | Type of API key selection | The logic selects *any* available key regardless of provider if `api_key` is not specifically set for a provider. Could lead to using wrong key if multiple are set. |

### Large Issues (Will generate analysis)
*None detected.*

**Proceed with cleanup?** (yes/no/skip-small/only-report)
