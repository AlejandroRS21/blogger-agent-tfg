# Research: Preservación de caracteres `ñ` en pipeline de artículos

## Decision 1: Contrato explícito de Unicode en artefactos publicados

- **Decision**: Establecer como regla que los artefactos de publicación (`docs/posts.json` y `docs/posts/*.json`) preservan texto Unicode sin transliteración.
- **Rationale**: El problema funcional reportado es pérdida semántica al convertir `ñ` a `n`; el contrato debe fijar resultado observable en salida publicada.
- **Alternatives considered**:
  - Validar solo internamente en memoria: rechazado, porque no garantiza consistencia en archivos finales.
  - Validar solo en frontend: rechazado, porque el daño puede venir desde backend y llegar ya degradado.

## Decision 2: Prohibir normalización ASCII para contenido visible

- **Decision**: El contenido visible (título, excerpt, body) no debe pasar por transliteración o normalización a ASCII; solo identificadores técnicos (por ejemplo slugs/ids) pueden normalizarse cuando aplique.
- **Rationale**: La `ñ` es carácter semántico en español; convertirla en `n` cambia palabras y reduce calidad editorial.
- **Alternatives considered**:
  - Normalizar todo para "compatibilidad": rechazado, rompe textos en castellano.
  - Permitir normalización configurable por feature flag: rechazado, añade complejidad innecesaria para este alcance.

## Decision 3: Verificación automatizada de regresión lingüística

- **Decision**: Añadir pruebas de regresión con frases controladas que contienen `ñ`, y comprobar preservación en salidas relevantes y publicación.
- **Rationale**: Evita regresiones silenciosas y cumple el principio constitucional de verificación automática primero.
- **Alternatives considered**:
  - Revisión manual en cada release: rechazada por baja confiabilidad y alto coste.

## Decision 4: Alcance histórico bajo demanda (clarificación B)

- **Decision**: La corrección obligatoria aplica a contenido nuevo; históricos degradados se corrigen mediante regeneración/corrección manual cuando se solicite.
- **Rationale**: Reduce riesgo de cambios masivos y permite entrega rápida del fix principal.
- **Alternatives considered**:
  - Migración masiva automática del histórico: rechazada por riesgo de efectos colaterales editoriales y esfuerzo no acotado.
