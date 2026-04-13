# Quickstart: Diagnóstico y validación del workflow con Gemini

Esta guía reproduce el incidente reportado y define la validación esperada tras aplicar la solución.

## Prerrequisitos

- Entorno Python del backend activo.
- Dependencias instaladas (incluyendo `google-genai`).
- Archivo `.env` con `GEMINI_API_KEY` válida.

## Reproducción del problema actual

Desde `backend/` ejecutar:

```bash
.venv/bin/python3 -m src.orchestrator.runner \
	--topic "El futuro de la IA Openclaw" \
	--blog-url "https://javipas.com" \
	--output "outputs/Elfuturoesopenclaw.json" \
	--provider gemini
```

Síntomas observados:

- Error Gemini con modelo `meta-llama/Meta-Llama-3.1-8B-Instruct` y `404 Not Found`.
- Fallback en `content_generation` y `critique`.
- `Image selection failed: Expecting value: line 1 column 1`.
- Flujo finaliza como éxito pero con `Word Count: 0`.

## Validación esperada tras la solución

- No se intenta invocar Gemini con modelo de familia Llama.
- Si hay modelo incompatible, se resuelve a un Gemini válido o se falla temprano con error explícito.
- `ImageSelectorAgent` no lanza parse error no controlado en respuestas vacías/no JSON.
- El resultado final no puede ser contenido vacío cuando el workflow marca éxito.

## Comandos de verificación rápida

```bash
pytest tests/test_orchestrator_config.py tests/test_orchestrator.py tests/test_agents.py -q
```

```bash
.venv/bin/python3 -m src.orchestrator.runner \
	--topic "Prueba compatibilidad provider-model" \
	--blog-url "https://javipas.com" \
	--provider gemini
```

## Resultado de validación (2026-04-04)

- Suite objetivo: `45 passed` (`tests/test_orchestrator_config.py`, `tests/test_orchestrator.py`, `tests/test_agents.py`).
- Ejecución end-to-end con `--provider gemini`:
  - sin error `404` por modelo no compatible,
  - salida JSON generada en `backend/outputs/Elfuturoesopenclaw.json`,
  - contenido no vacío (`Word Count: 1072`).
