# Data Model: Integridad de caracteres españoles

## Entities

- **Artículo Publicable** (existing, constrained)
  - `title`: texto visible del artículo.
  - `excerpt`: resumen corto visible en listados.
  - `content`: cuerpo del artículo (markdown/html renderizable).
  - `metadata`: metadatos asociados (fecha, tags, autor, etc.).

- **Snapshot Intermedio de Flujo** (new logical entity)
  - `phase_name`: fase del pipeline.
  - `text_payload`: contenido textual parcial.
  - `has_enye`: indicador de presencia de `ñ` para validación.

- **Regla de Validación Lingüística** (new logical entity)
  - `rule_id`: identificador de regla (ej. `preserve_enye`).
  - `input_fixture`: frase o bloque de prueba con caracteres españoles.
  - `expected_output`: texto esperado sin degradación.
  - `validation_scope`: `intermediate | published`.

## Validation Rules

- Si `text_payload` de entrada contiene `ñ`, la salida equivalente en cada etapa validada no puede reemplazarla por `n`.
- Los campos visibles del artículo (`title`, `excerpt`, `content`) deben preservar Unicode español en artefactos publicados.
- La normalización para slugs/ids no debe alterar los campos visibles del artículo.
- Los artículos sin `ñ` deben seguir pasando sin cambios de formato ni contenido.

## State Transitions

- **Pipeline textual**
  - `raw_generation` -> `intermediate_snapshot` -> `published_artifact`
  - validación en transición: `unicode_integrity_check`

- **Gestión de error lingüístico**
  - `unicode_integrity_check_failed` -> `workflow_failed` o `manual_review_required`

- **Históricos (scope B)**
  - `historical_article_detected` -> `manual_regeneration_requested` -> `published_artifact_updated`
