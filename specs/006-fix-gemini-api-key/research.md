# Research: Resiliencia del workflow con proveedor Gemini

## Decision 1: Resolver modelo por proveedor en tiempo de creación del LLM

- **Decision**: Cuando `provider == gemini`, forzar un modelo Gemini válido si el modelo recibido no pertenece a la familia Gemini (por ejemplo `meta-llama/...`).
- **Rationale**: El error `404 Not Found` aparece porque `config.default_model` en TOML es de HuggingFace (`meta-llama/...`) y se propaga a `ContentGenerator` y `CriticAgent` aunque el proveedor sea Gemini.
- **Alternatives considered**:
  - Mantener el modelo recibido y dejar que falle: rechazado por degradación silenciosa a fallback y contenido vacío.
  - Cambiar solo `default.toml`: rechazado porque no cubre otros puntos de entrada donde se pase un modelo incompatible.

## Decision 2: Validación de compatibilidad provider-model previa a llamadas remotas

- **Decision**: Añadir validación explícita de compatibilidad provider-model y error accionable antes de invocar la API.
- **Rationale**: Evita costes de red innecesarios y produce diagnóstico rápido (en lugar de 404 tardío).
- **Alternatives considered**:
  - Confiar solo en errores del SDK remoto: rechazado por mala DX y logs ambiguos.

## Decision 3: Parseo robusto en agentes que exigen JSON (ImageSelector/Critic)

- **Decision**: Implementar parseo tolerante a bloques markdown, prefijos/sufijos extra y respuestas vacías, con fallback tipado.
- **Rationale**: El warning `Expecting value: line 1 column 1` indica respuesta vacía o no JSON; hoy el fallback existe, pero sin telemetría ni validación estructural previa.
- **Alternatives considered**:
  - Exigir JSON estricto sin fallback: rechazado porque incrementa fallos duros en producción.

## Decision 4: Garantía mínima de contenido en fallback de generación

- **Decision**: Fallback de `ContentGenerator` debe producir cuerpo con longitud mínima configurable y no solo una línea corta.
- **Rationale**: En el incidente, el flujo completó en verde con `Word Count: 0`, generando un falso positivo de éxito.
- **Alternatives considered**:
  - Mantener fallback actual mínimo: rechazado por romper criterio de calidad y salida útil.

## Decision 5: Cobertura de pruebas de regresión orientadas al incidente

- **Decision**: Añadir tests para:
  - resolución de modelo por proveedor,
  - rechazo temprano de modelo incompatible,
  - parseo JSON robusto en `ImageSelectorAgent`,
  - no producción de contenido vacío tras fallbacks.
- **Rationale**: Cumplimiento del principio de verificación automática primero.
- **Alternatives considered**:
  - Pruebas manuales con CLI solamente: rechazado por riesgo de regresiones repetidas.
