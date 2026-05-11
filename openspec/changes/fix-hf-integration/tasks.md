# Tasks: fix-hf-integration

## Backend: Environment
- [x] Uninstall conflicting google packages: `google-api-python-client`, `google-generativeai`, `google-ai-generativelanguage`
- [x] Reinstall `google-genai`
- [x] Verify `from google import genai` import (Requires PYTHONPATH fix)

## Backend: LLM Configuration
- [x] Update `backend/aphra_blogger/config/default.toml`:
    - Set `huggingface.default_model` to `Qwen/Qwen2.5-72B-Instruct`
    - Set `huggingface.critic_model` to `Qwen/Qwen2.5-72B-Instruct`
- [x] Update `backend/aphra_blogger/llm/factory.py`:
    - Set `huggingface` default to `Qwen/Qwen2.5-72B-Instruct`
- [x] Update `backend/aphra_blogger/llm/huggingface_provider.py`:
    - Set `analysis` model to `mistralai/Mistral-7B-Instruct-v0.2`

## Verification
- [ ] Run environment check script
- [ ] Run LLM factory unit test (if exists) or create one
- [ ] Verify HF provider initialization with new defaults
