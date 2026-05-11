# Technical Design: fix-hf-integration

## Architecture Decisions

### 1. LLM Model Selection (HuggingFace)
- **Problem**: Llama 3.1 8B/70B models are gated and fail on the Inference API.
- **Solution**: Standardize on `Qwen/Qwen2.5-72B-Instruct` as the default model. It provides excellent performance and is currently available without gating on the serverless API.
- **Analysis Model**: Use `mistralai/Mistral-7B-Instruct-v0.2` for the `analysis` role in `HuggingFaceProvider`. It's lightweight and reliable.

### 2. Environment Fix (Gemini)
- **Problem**: `google-genai` fails to import due to namespace pollution from older `google-*` packages.
- **Solution**: Force-reinstall `google-genai` after removing conflicting packages.
- **Action**: 
  ```bash
  pip uninstall -y google-api-python-client google-generativeai google-ai-generativelanguage
  pip install google-genai
  ```

### 3. LLM Factory Synchronization
- **Problem**: The factory has hardcoded defaults that contradict the config.
- **Solution**: Update `backend/aphra_blogger/llm/factory.py` to match the new model selections.

## Component Changes

### 1. `backend/aphra_blogger/config/default.toml`
- Update `default_model` and `critic_model` under `[huggingface]`.

### 2. `backend/aphra_blogger/llm/factory.py`
- Update `_default_model_for_provider` dictionary.

### 3. `backend/aphra_blogger/llm/huggingface_provider.py`
- Update `analysis` model ID in the constructor.

## Verification Plan
1. **Import Test**: Verify `from google import genai` works in the `.venv`.
2. **Factory Test**: Verify `create_llm_provider(provider="huggingface")` returns a provider with the correct model ID.
3. **Connectivity Test**: Run `src/orchestrator/safety.py` (if it exists) or a small test script to verify HF API response.
