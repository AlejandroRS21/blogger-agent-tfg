# Tasks: Publicacion Continua de Novedades Tecnologicas

**Input**: Design documents from /specs/009-continuous-tech-publishing/
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Inicializar estructura y configuracion comun para operacion continua

- [x] T001 Crear configuracion base de ciclo continuo en backend/src/orchestrator/config.py
- [x] T002 [P] Definir estados operativos y metadatos iniciales en backend/src/orchestrator/state.py
- [x] T003 [P] Consolidar exportaciones del paquete continuo en backend/src/orchestrator/continuous/__init__.py
- [x] T004 [P] Crear modulo de monitoreo para SLI/SLO y alertas en backend/src/orchestrator/continuous/monitoring.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Infraestructura obligatoria para todas las historias de usuario

**CRITICAL**: No iniciar historias de usuario hasta completar esta fase

- [x] T005 Implementar modelo de historial de ciclos/incidentes/publicaciones en backend/src/orchestrator/continuous/history_store.py
- [x] T006 [P] Implementar scheduler con cadencia de 12h y calculo de lag en backend/src/orchestrator/continuous/scheduler.py
- [x] T007 [P] Implementar politica reusable de reintentos 5m/15m/30m en backend/src/orchestrator/continuous/retry_policy.py
- [x] T008 [P] Implementar controles de trust boundary (allowlist, sanitizacion, neutralizacion, limites) en backend/src/orchestrator/continuous/source_guard.py
- [x] T009 Configurar dispatcher de alertas operativas en backend/src/orchestrator/continuous/alerts.py
- [x] T010 Integrar servicios fundacionales en el bootstrap de orquestacion en backend/src/orchestrator/main.py

**Checkpoint**: Fundacion completa y lista para historias de usuario

---

## Phase 3: User Story 1 - Publicacion automatica continua (Priority: P1)

**Goal**: Publicar articulos de forma autonoma cada 12 horas sin intervencion manual diaria

**Independent Test**: Ejecutar un periodo controlado y verificar publicacion autonoma, programacion del siguiente ciclo y cierre skipped_with_reason cuando no haya tema valido

- [x] T011 [P] [US1] Crear prueba de publicacion periodica autonoma en backend/tests/test_workflow.py
- [x] T012 [P] [US1] Crear prueba de cierre skipped_with_reason sin bloqueo de ciclos futuros en backend/tests/test_orchestrator.py
- [x] T013 [US1] Implementar bucle continuo y programacion del siguiente ciclo en backend/src/orchestrator/runner.py
- [x] T014 [US1] Implementar transiciones planned/running/success/skipped_with_reason en backend/src/orchestrator/main.py
- [x] T015 [US1] Persistir resultado de cada ciclo con reason_code en backend/src/orchestrator/continuous/history_store.py
- [x] T016 [US1] Integrar escritura canonica de publicaciones en docs en backend/aphra_blogger/agents/html_builder.py
- [x] T017 [US1] Exponer start/pause/resume/status continuo para Modal en backend/modal_app.py

**Checkpoint**: US1 funcional e independiente

---

## Phase 4: User Story 2 - Relevancia y actualidad tematica (Priority: P2)

**Goal**: Seleccionar temas actuales y diversos, evitando redundancia semantica

**Independent Test**: Verificar multi-fuente con fallback, diversidad de categoria y rechazo por similitud >= 0.80 en 14 dias

- [x] T018 [P] [US2] Crear prueba de multi-fuente con fallback y source_exhausted en backend/tests/test_scraper.py
- [x] T019 [P] [US2] Crear prueba de anti-duplicado con umbral 0.80 y ventana de 14 dias en backend/tests/test_structural_diversity.py
- [x] T020 [US2] Implementar fetch multi-fuente con fallback automatico en backend/aphra_blogger/agents/research_agent.py
- [x] T021 [US2] Implementar scoring por recencia y rotacion de categorias en backend/src/orchestrator/continuous/topic_selector.py
- [x] T022 [US2] Implementar validacion de similitud y rechazo de borradores redundantes en backend/src/orchestrator/continuous/validation.py
- [x] T023 [US2] Implementar manejo determinista no-topic como skipped_with_reason en backend/src/orchestrator/main.py
- [x] T024 [US2] Propagar source_summary y topic_category a registro publicado en backend/aphra_blogger/agents/content_generator.py

**Checkpoint**: US1 y US2 funcionales de forma independiente

---

## Phase 5: User Story 3 - Control operativo y continuidad (Priority: P3)

**Goal**: Asegurar resiliencia operativa con incidentes, alertas, pausa/reanudacion y degradacion controlada

**Independent Test**: Forzar fallos transitorios y confirmar retries, continuidad del scheduler, alertas en SLA y control operativo completo

- [x] T025 [P] [US3] Crear prueba de retries 5m/15m/30m y continuidad tras fallo individual en backend/tests/test_orchestrator.py
- [x] T026 [P] [US3] Crear prueba de pausa/reanudacion y estado degraded en backend/tests/test_workflow.py
- [x] T027 [P] [US3] Crear prueba de alertas por success-rate diario y lag de ciclo en backend/tests/test_orchestrator.py
- [x] T028 [US3] Implementar gestor de incidentes con severity/stage/reason_code en backend/src/orchestrator/continuous/incident_manager.py
- [x] T029 [US3] Implementar snapshot de estado active/paused/degraded para consulta operativa en backend/src/orchestrator/state.py
- [x] T030 [US3] Emitir eventos operativos por etapa y reason_code en backend/src/orchestrator/runner.py
- [x] T031 [US3] Implementar evaluacion de SLI/SLO y emision de alertas en backend/src/orchestrator/continuous/monitoring.py
- [x] T032 [US3] Implementar pausa automatica por relevancia semanal < 70% durante 2 semanas en backend/src/orchestrator/main.py

**Checkpoint**: Todas las historias funcionales de forma independiente

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Cerrar calidad transversal, runbooks y validacion final

- [x] T033 [P] Añadir pruebas de resiliencia para 429/5xx, timeout y RSS malformado en backend/tests/test_scraper.py
- [x] T034 [P] Añadir pruebas de neutralizacion de instrucciones embebidas en backend/tests/test_agents.py
- [x] T035 Actualizar contrato operacional con skipped_with_reason, source_exhausted y alertas en specs/009-continuous-tech-publishing/contracts/continuous-publishing-operations-contract.md
- [x] T036 [P] Actualizar quickstart con runbook de degraded y umbrales de accion en specs/009-continuous-tech-publishing/quickstart.md
- [x] T037 [P] Actualizar guia operativa continua en project_docs/ORCHESTRATION_PLAN.md
- [x] T038 Ejecutar validacion integral y registrar evidencia final en specs/009-continuous-tech-publishing/checklists/requirements.md

---

## Dependencies & Execution Order

### Phase Dependencies

- Phase 1: sin dependencias
- Phase 2: depende de Phase 1 y bloquea historias
- Phase 3: depende de Phase 2
- Phase 4: depende de Phase 2
- Phase 5: depende de Phase 2
- Phase 6: depende de completar Phase 3, Phase 4 y Phase 5

### User Story Dependencies

- US1 (P1): arranca al completar fundacion y entrega MVP autonomo
- US2 (P2): arranca al completar fundacion y añade calidad editorial sin romper US1
- US3 (P3): arranca al completar fundacion y añade control operativo y continuidad

### Story Completion Order

- US1 -> US2 -> US3 para entrega incremental de valor

---

## Parallel Opportunities

- Setup: T002, T003, T004 en paralelo
- Foundational: T006, T007, T008 en paralelo
- US1: T011 y T012 en paralelo
- US2: T018 y T019 en paralelo
- US3: T025, T026 y T027 en paralelo
- Polish: T033, T034, T036 y T037 en paralelo

---

## Parallel Example: User Story 1

- [x] T011 [P] [US1] Crear prueba de publicacion periodica autonoma en backend/tests/test_workflow.py
- [x] T012 [P] [US1] Crear prueba de cierre skipped_with_reason sin bloqueo de ciclos futuros en backend/tests/test_orchestrator.py

## Parallel Example: User Story 2

- [x] T018 [P] [US2] Crear prueba de multi-fuente con fallback y source_exhausted en backend/tests/test_scraper.py
- [x] T019 [P] [US2] Crear prueba de anti-duplicado con umbral 0.80 y ventana de 14 dias en backend/tests/test_structural_diversity.py

## Parallel Example: User Story 3

- [x] T025 [P] [US3] Crear prueba de retries 5m/15m/30m y continuidad tras fallo individual en backend/tests/test_orchestrator.py
- [x] T027 [P] [US3] Crear prueba de alertas por success-rate diario y lag de ciclo en backend/tests/test_orchestrator.py

---

## Implementation Strategy

### MVP First (US1)

1. Completar Phase 1
2. Completar Phase 2
3. Completar Phase 3 (US1)
4. Validar US1 de forma independiente

### Incremental Delivery

1. Foundation completa
2. Entregar US1 y validar
3. Entregar US2 y validar
4. Entregar US3 y validar
5. Endurecer con Phase 6

