# Contract: Provider-Model Compatibility and Fallback Semantics

## Scope

Define the observable behavior for:

- LLM provider creation (`create_llm_provider`).
- Provider/model compatibility enforcement.
- JSON-dependent agent behavior (`ImageSelectorAgent`, `CriticAgent`).

## Inputs

- `provider`: `auto | gemini | huggingface | openai | modal`
- `api_key`: optional string
- `model`: optional string
- Generation params: `temperature`, `max_tokens`

## Provider/Model Rules

1. If `provider == gemini`, runtime must not call Gemini API with non-Gemini model IDs (e.g. `meta-llama/...`).
2. If `provider == huggingface`, model must be compatible with HuggingFace inference endpoint format.
3. If `provider == auto`, provider selection follows configured fallback order and chooses a provider with valid credential + compatible model.
4. On incompatibility, implementation must either:
   - resolve to a compatible default model for that provider, or
   - fail fast with explicit actionable error.

## Error Contract

- Provider errors must include provider name and effective model attempted.
- Parse errors in JSON-dependent agents must not crash workflow phase irrecoverably.
- Fallback activation must be explicit in logs/state.
- Workflow phase records must include typed metadata when available:
  - `error_type` (`provider_error | parse_error | timeout | unknown`)
  - `fallback_used` (boolean)
  - `effective_provider` and `effective_model`

## Output Contract

- Successful workflow output must include non-empty final content.
- Image selection output must always be a list of image objects with fields:
  - `position`
  - `prompt`
  - `alt_text`
  - `context`

## Non-Goals

- No change to frontend contract.
- No schema change for static publishing under `docs/` in this feature.
