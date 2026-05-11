# Change Proposal: fix-hf-integration

## Intent
Resolve blocking errors in the LLM provider layer:
1. **HuggingFace 404**: The currently configured Llama 3.1 models are gated or unavailable on the serverless API, causing `model_not_found` errors.
2. **Gemini ImportError**: A namespace conflict in the Python environment prevents importing the new `google-genai` SDK.

## Scope
- `backend/aphra_blogger/config/default.toml`
- `backend/aphra_blogger/llm/factory.py`
- `backend/aphra_blogger/llm/huggingface_provider.py`
- Backend Python environment (`.venv`)

## Approach

### 1. Model Migration (HuggingFace)
- Replace `meta-llama/Meta-Llama-3.1-8B-Instruct` with `Qwen/Qwen2.5-72B-Instruct`.
- Replace `meta-llama/Meta-Llama-3.1-70B-Instruct` with `Qwen/Qwen2.5-72B-Instruct`.
- Replace `meta-llama/Llama-3.2-1B-Instruct` (analysis) with `mistralai/Mistral-7B-Instruct-v0.2`.

### 2. Gemini SDK Fix
- Purge old `google-*` packages that conflict with the new namespace.
- Re-install `google-genai` in the `.venv`.

## Risks
- **Rate Limiting**: Qwen 2.5 72B is a popular model; the free Inference API might rate-limit more strictly than smaller models.
- **Breaking Changes**: Updating packages in the venv might affect other parts of the system if they relied on specific versions.

## Rollback Plan
- Revert file changes via git.
- Re-install previous package versions if needed.
