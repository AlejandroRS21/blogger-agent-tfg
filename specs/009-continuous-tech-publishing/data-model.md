# Data Model: Publicacion Continua

## Entities

- PublicationCycle
  - cycle_id: identificador unico del ciclo.
  - scheduled_at: instante planificado del ciclo.
  - started_at: instante real de inicio.
  - ended_at: instante real de fin.
  - status: planned, running, success, failed, degraded.
  - retry_count: numero de reintentos ejecutados dentro del ciclo.
  - topic_candidate_id: referencia al tema seleccionado.
  - published_article_id: referencia al articulo publicado cuando hay exito.

- TopicCandidate
  - topic_id: identificador unico.
  - title_hint: titulo base sugerido.
  - category: categoria tecnologica principal.
  - recency_score: puntuacion de actualidad.
  - source_refs: lista de referencias de origen.
  - selection_status: proposed, selected, rejected_duplicate, expired.

- ArticleDraft
  - draft_id: identificador unico.
  - topic_id: referencia al tema de origen.
  - title: titulo del articulo.
  - excerpt: resumen visible.
  - body: contenido principal.
  - quality_status: pending, validated, rejected.
  - redundancy_score: similitud contra ventana reciente.

- PublishedArticleRecord
  - article_id: identificador final publicado.
  - published_at: fecha y hora de publicacion.
  - topic_category: categoria principal.
  - source_summary: resumen de fuentes usadas.
  - publication_status: published, skipped, failed.
  - output_paths: rutas de artefactos en docs.

- OperationalIncident
  - incident_id: identificador unico.
  - detected_at: fecha y hora de deteccion.
  - severity: warning, major, critical.
  - stage: topic_selection, generation, validation, publish.
  - reason_code: codigo normalizado de error.
  - recovery_action: retry, skip, pause_required.
  - resolution_status: open, mitigated, resolved.

## Validation Rules

- Todo PublicationCycle debe cerrar en success, failed o degraded; no puede quedar indefinidamente en running.
- retry_count no puede superar 3 en un mismo ciclo.
- Un ArticleDraft solo puede pasar a validated si contiene titulo, excerpt y body no vacios.
- Un ArticleDraft con redundancy_score >= 0.80 debe marcarse rejected.
- TopicCandidate debe tener al menos una referencia de fuente antes de selected.
- Todo fallo en ciclo debe crear un OperationalIncident asociado con stage y reason_code.
- Todo PublishedArticleRecord en estado published debe incluir output_paths validos dentro de docs.

## State Transitions

- Ciclo operativo
  - planned -> running -> success
  - planned -> running -> failed -> running (retry)
  - running -> degraded (si fallos sostenidos impactan continuidad)
  - degraded -> paused (si operador decide pausar)

- Seleccion de tema
  - proposed -> selected
  - proposed -> rejected_duplicate
  - proposed -> expired

- Borrador de articulo
  - pending -> validated -> published
  - pending -> rejected

- Incidentes
  - open -> mitigated -> resolved
  - open -> resolved (cuando no requiere mitigacion intermedia)
