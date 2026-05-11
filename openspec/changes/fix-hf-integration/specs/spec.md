# Change Specification: fix-hf-integration

## Requirements
1. **Model Accessibility**: All default LLM configurations for the HuggingFace provider MUST point to models that are publicly available via the serverless Inference API (non-gated).
2. **SDK Compatibility**: The Python environment MUST support importing `google.genai` without namespace conflicts.
3. **Configuration Consistency**: Default model IDs in `default.toml` MUST match the actual working models on HuggingFace.

## Scenarios

### Scenario 1: HuggingFace Provider Initialization
**Given** the system is configured to use the `huggingface` provider
**And** no specific model is provided in the environment or config
**When** the LLM factory creates the provider
**Then** it SHOULD default to `Qwen/Qwen2.5-72B-Instruct`
**And** subsequent API calls SHOULD succeed without 404 errors.

### Scenario 2: Gemini Provider Availability
**Given** the `google-genai` package is installed in the virtual environment
**When** the `GeminiProvider` is imported
**Then** `GEMINI_AVAILABLE` SHOULD be `True`
**And** `from google import genai` SHOULD NOT raise an `ImportError`.

### Scenario 3: Auto Provider Selection
**Given** `HF_TOKEN` is set
**And** `GEMINI_API_KEY` is set
**When** the provider is set to `auto`
**Then** the factory SHOULD try providers in priority order (Gemini -> HuggingFace)
**And** return a working instance.
