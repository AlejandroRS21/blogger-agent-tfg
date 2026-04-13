# Tasks: Preservar caracteres ñ en artículos

**Input**: Design documents from `/specs/007-fix-enye-text/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/unicode-preservation-contract.md`, `quickstart.md`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Preparar fixtures y utilidades base para validación Unicode

- [ ] T001 Crear fixture base con frases de control para `ñ` en `backend/tests/fixtures/unicode_enye_cases.json`
- [ ] T002 [P] Crear helper de aserciones Unicode para pruebas en `backend/tests/utils/unicode_assertions.py`
- [ ] T003 [P] Añadir datos de ejemplo con `ñ` para validación de catálogo en `docs/posts.json`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Infraestructura de control de integridad lingüística obligatoria para todas las historias

- [ ] T004 Implementar guard de integridad Unicode reutilizable en `backend/src/orchestrator/unicode_guard.py`
- [ ] T005 [P] Integrar verificación de integridad entre fases en `backend/src/orchestrator/main.py`
- [ ] T006 [P] Propagar fallos de integridad Unicode como error accionable en `backend/src/orchestrator/runner.py`
- [ ] T007 Registrar metadatos de fallo de integridad (`unicode_integrity_check`) en `backend/src/orchestrator/state.py`
- [ ] T008 Ajustar serialización de estado para inspección legible de Unicode en `backend/src/orchestrator/state.py`

**Checkpoint**: Base de validación Unicode lista; se puede implementar US1/US2/US3

---

## Phase 3: User Story 1 - Escritura fiel del castellano (Priority: P1) 🎯 MVP

**Goal**: Garantizar que `ñ` se preserva en contenido nuevo generado y publicado

**Independent Test**: Generar un artículo con `año`, `niñez`, `señal`, `España` y verificar preservación en salida final y artefacto publicado

### Tests for User Story 1

- [ ] T009 [P] [US1] Añadir prueba de preservación de `ñ` en salida final del orquestador en `backend/tests/test_orchestrator.py`
- [ ] T010 [P] [US1] Añadir prueba de preservación de `ñ` en artefacto de publicación (`docs/posts*.json`) en `backend/tests/test_batch_generate.py`

### Implementation for User Story 1

- [ ] T011 [US1] Evitar transliteración en campos visibles (`title`, `excerpt`, `content`) durante armado de post en `backend/daggr_blogger_workflow.py`
- [ ] T012 [US1] Asegurar escritura UTF-8 + `ensure_ascii=False` en rutas de publicación de `backend/daggr_blogger_workflow.py`
- [ ] T013 [US1] Preservar `ñ` al normalizar datos de frontend en `frontend/app/lib/api.ts`
- [ ] T014 [US1] Añadir post de control con `ñ` para verificación manual de publicación en `docs/posts/el-futuro-de-openclaw.json`

**Checkpoint**: US1 funcional y verificable de forma independiente

---

## Phase 4: User Story 2 - Consistencia entre fases del flujo (Priority: P2)

**Goal**: Evitar degradación de `ñ` en cualquier etapa intermedia del pipeline

**Independent Test**: Ejecutar pipeline completo y comprobar que snapshots entre fases no convierten `ñ` en `n`

### Tests for User Story 2

- [ ] T015 [P] [US2] Añadir prueba de integridad Unicode entre `draft_content` y `final_content` en `backend/tests/test_orchestrator.py`
- [ ] T016 [P] [US2] Añadir prueba de integridad de texto visible en builder HTML en `backend/tests/test_html_builder.py`

### Implementation for User Story 2

- [ ] T017 [US2] Añadir validación explícita de integridad en transición `draft -> final` en `backend/src/orchestrator/main.py`
- [ ] T018 [US2] Añadir validación explícita de integridad en transición `final -> html` en `backend/src/orchestrator/main.py`
- [ ] T019 [US2] Clasificar fallos de Unicode como tipo de error específico en `backend/src/orchestrator/main.py`
- [ ] T020 [US2] Mostrar hint de recuperación cuando falle integridad Unicode en `backend/src/orchestrator/runner.py`

**Checkpoint**: US2 funcional y verificable de forma independiente

---

## Phase 5: User Story 3 - Prevención de regresiones editoriales (Priority: P3)

**Goal**: Consolidar validación automática y flujo manual para históricos degradados

**Independent Test**: Ejecutar suite de regresión lingüística y validar que pasa en todos los casos de control

### Tests for User Story 3

- [ ] T021 [P] [US3] Crear suite fixture-driven de regresión lingüística en `backend/tests/test_unicode_regression.py`
- [ ] T022 [P] [US3] Añadir prueba para artículos sin `ñ` (no regresión) en `backend/tests/test_unicode_regression.py`

### Implementation for User Story 3

- [ ] T023 [US3] Documentar flujo manual para corrección bajo demanda de históricos en `specs/007-fix-enye-text/quickstart.md`
- [ ] T024 [US3] Añadir sección de evidencias de validación Unicode en `specs/007-fix-enye-text/quickstart.md`

**Checkpoint**: US3 funcional y verificable de forma independiente

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Cierre de calidad transversal

- [ ] T025 [P] Revisar consistencia del contrato Unicode con implementación en `specs/007-fix-enye-text/contracts/unicode-preservation-contract.md`
- [ ] T026 Ejecutar pruebas objetivo y registrar resultados en `specs/007-fix-enye-text/quickstart.md`
- [ ] T027 [P] Verificar visualización final del artículo con `ñ` en `frontend/app/posts/[slug]/page.tsx`

---

## Dependencies & Execution Order

### Phase Dependencies

- Phase 1: sin dependencias
- Phase 2: depende de Phase 1 y bloquea historias
- Phase 3 (US1): depende de Phase 2
- Phase 4 (US2): depende de Phase 2
- Phase 5 (US3): depende de Phase 2
- Phase 6: depende de US1, US2 y US3

### User Story Dependencies

- US1: requiere guard y validación Unicode de Phase 2
- US2: requiere guard y trazabilidad de errores de Phase 2
- US3: requiere fixtures y guard de Phase 1/2; puede avanzar en paralelo con US1/US2 tras completar fundación

### Within Each User Story

- Crear pruebas de regresión de la historia antes de cambios de implementación
- Implementar validación núcleo antes de ajustes de UX/logs
- Validar historia de forma independiente antes de avanzar

---

## Parallel Execution Examples

### User Story 1

```bash
T009 backend/tests/test_orchestrator.py
T010 backend/tests/test_batch_generate.py
```

```bash
T012 backend/daggr_blogger_workflow.py
T013 frontend/app/lib/api.ts
```

### User Story 2

```bash
T015 backend/tests/test_orchestrator.py
T016 backend/tests/test_html_builder.py
```

```bash
T017 backend/src/orchestrator/main.py
T020 backend/src/orchestrator/runner.py
```

### User Story 3

```bash
T021 backend/tests/test_unicode_regression.py
T022 backend/tests/test_unicode_regression.py
```

---

## Implementation Strategy

### MVP First (US1)

1. Completar Phase 1
2. Completar Phase 2
3. Completar Phase 3 (US1)
4. Validar publicación con artículo de control que incluya `ñ`

### Incremental Delivery

1. Base Unicode y trazabilidad (Phase 1-2)
2. Entrega US1 validada
3. Entrega US2 validada
4. Entrega US3 validada
5. Cierre transversal (Phase 6)

### Parallel Team Strategy

1. Equipo completa Phase 1 y Phase 2
2. Un frente implementa US1, otro US2, y QA implementa US3 en paralelo
3. Convergencia en Phase 6 para verificación final

---

## Notes

- Todas las tareas usan formato checklist estricto con ID secuencial
- Las tareas `[P]` son paralelizables al tocar archivos distintos o sin dependencia directa
- Las tareas `[US1]`, `[US2]` y `[US3]` están encapsuladas para pruebas independientes
