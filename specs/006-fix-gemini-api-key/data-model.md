# Data Model: Corrección de workflow Gemini + fallback seguro

## Entities

- **OrchestratorConfig** (existing, modified)
  - `provider`: `auto | gemini | huggingface | openai | modal`.
  - `default_model`: modelo preferido global (puede ser incompatible con un proveedor concreto).
  - `gemini_api_key`, `huggingface_token`, `openai_api_key`, `modal_api_key`: credenciales por proveedor.
  - `validate()`: valida existencia de al menos una credencial y consistencia básica.

- **LLMConfig** (existing, modified)
  - `api_key`: credencial efectiva.
  - `model`: modelo efectivo post-resolución por proveedor.
  - `temperature`, `max_tokens`: parámetros de inferencia.

- **ProviderModelResolution** (new logical entity)
  - `requested_provider`: proveedor solicitado.
  - `requested_model`: modelo entrante (puede ser `None` o incompatible).
  - `resolved_model`: modelo final compatible usado en runtime.
  - `resolution_reason`: `defaulted | normalized | passthrough | rejected`.

- **AgentExecutionResult** (existing logical, extended)
  - `agent_name`, `success`, `duration_ms`.
  - `error_type`: `provider_error | parse_error | timeout | unknown`.
  - `fallback_used`: boolean.
  - `output_payload`: contenido generado (texto o JSON según agente).

## Validation Rules

- Si `provider == gemini`, el modelo efectivo DEBE cumplir patrón Gemini (`gemini-*` o alias soportado).
- Si `provider == huggingface`, el modelo efectivo DEBE ser compatible con endpoint/model ID de HF.
- Si un agente requiere JSON de salida, una respuesta vacía o inválida DEBE marcar `parse_error` y activar fallback tipado.
- El workflow NO debe marcarse exitoso con contenido final vacío.

## State Transitions

- **Modelo**
  - `input_model_received` -> `resolved_model_selected` -> `provider_call_executed`
  - rama de error: `provider_call_failed` -> `fallback_used`

- **Selección de imágenes**
  - `raw_llm_response` -> `json_parse_attempt`
  - si parsea: `validated_images`
  - si no parsea: `parse_error_recorded` -> `fallback_images_generated`

- **Generación de contenido**
  - `draft_requested` -> `draft_generated`
  - si error de proveedor: `provider_error_recorded` -> `fallback_draft_generated`
  - validación final: `non_empty_content_required`
