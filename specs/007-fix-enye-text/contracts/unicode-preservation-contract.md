# Contract: Preservación Unicode para caracteres españoles

## Scope

Define el comportamiento observable para preservar caracteres españoles (especialmente `ñ`) en generación, procesamiento intermedio y publicación de artículos.

## Inputs

- Texto fuente de artículo (topic/prompts/contenido intermedio).
- Campos visibles de publicación: `title`, `excerpt`, `content`.
- Artefactos de salida: `backend/outputs/*.json`, `docs/posts.json`, `docs/posts/*.json`.

## Rules

1. Si la entrada contiene `ñ`, las salidas visibles equivalentes deben mantener `ñ` sin convertirla en `n`.
2. No se permite transliteración ASCII en campos visibles de artículo.
3. La normalización de slugs/ids está permitida únicamente en identificadores técnicos, no en contenido visible.
4. Los artefactos publicados bajo `docs/` son la referencia canónica para validación.

## Error Contract

- La validación lingüística fallida debe marcar la ejecución como no válida para publicación.
- Debe quedar evidencia verificable de fallo (test o validación explícita) cuando se detecte degradación `ñ -> n`.

## Output Contract

- `title`, `excerpt` y `content` en publicación conservan Unicode español.
- No hay regresiones en artículos sin `ñ`.

## Non-Goals

- No incluye migración masiva automática del histórico.
- No redefine estrategia SEO de slugs más allá de preservar campos visibles.
