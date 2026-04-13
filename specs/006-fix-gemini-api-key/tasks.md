# Tasks: Workflow resiliente para Gemini y selección de imágenes

**Input**: Design documents from `/specs/006-fix-gemini-api-key/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/llm-provider-contract.md`, `quickstart.md`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Preparar baseline de validación y cobertura de regresión del incidente

- [X] T001 Crear baseline de regresión para configuración de credenciales en backend/tests/test_orchestrator_config.py
- [X] T002 [P] Documentar y fijar comando de reproducción del incidente en specs/006-fix-gemini-api-key/quickstart.md
- [X] T003 [P] Revisar variables de entorno soportadas para proveedores en backend/.env.example

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Infraestructura común obligatoria para todas las historias

- [X] T004 Implementar validación de credenciales por proveedor en backend/src/orchestrator/config.py
- [X] T005 [P] Implementar resolución centralizada provider-model en backend/aphra_blogger/llm/factory.py
- [X] T006 [P] Endurecer normalización y validación de modelos Gemini en backend/aphra_blogger/llm/gemini_provider.py
- [X] T007 Añadir metadatos de error tipado y uso de fallback en backend/src/orchestrator/state.py
- [X] T008 Ajustar propagación de errores accionables en backend/src/orchestrator/runner.py

**Checkpoint**: base técnica lista, se puede implementar US1 y US2

---

## Phase 3: User Story 1 - Ejecución exitosa con Gemini AI (Priority: P1) 🎯 MVP

**Goal**: Ejecutar el workflow con solo `GEMINI_API_KEY` sin errores de validación ni llamadas con modelo incompatible

**Independent Test**: Ejecutar `python -m src.orchestrator.runner --provider gemini --topic "Texto" --blog-url "URL"` con solo `GEMINI_API_KEY` y verificar flujo completo sin `404` por modelo no Gemini

- [X] T009 [P] [US1] Añadir prueba de validación con solo GEMINI_API_KEY en backend/tests/test_orchestrator_config.py
- [X] T010 [P] [US1] Añadir prueba de regresión provider-model para Gemini en backend/tests/test_orchestrator.py
- [X] T011 [US1] Actualizar carga de claves Gemini en métodos default/from_toml de backend/src/orchestrator/config.py
- [X] T012 [US1] Corregir inyección de API key por proveedor en inicialización de agentes en backend/src/orchestrator/main.py
- [X] T013 [US1] Aplicar resolución de modelo efectiva antes de crear proveedor LLM en backend/aphra_blogger/llm/factory.py
- [X] T014 [US1] Bloquear éxito de workflow con contenido final vacío en backend/src/orchestrator/main.py
- [X] T015 [US1] Mejorar fallback de borrador para contenido mínimo útil en backend/aphra_blogger/agents/content_generator.py

**Checkpoint**: US1 operativa y verificable de forma independiente

---

## Phase 4: User Story 2 - Mensajes de error informativos (Priority: P2)

**Goal**: Ofrecer errores de validación y ejecución claros que indiquen credencial/proveedor/modelo esperados

**Independent Test**: Ejecutar el runner sin claves y comprobar mensaje que incluya `GEMINI_API_KEY`; forzar modelo incompatible y comprobar error explícito provider-model

- [X] T016 [P] [US2] Añadir prueba de mensaje de validación sin credenciales en backend/tests/test_orchestrator_config.py
- [X] T017 [P] [US2] Añadir prueba de error explícito provider-model incompatible en backend/tests/test_orchestrator.py
- [X] T018 [US2] Actualizar mensaje de validación para incluir GEMINI_API_KEY en backend/src/orchestrator/config.py
- [X] T019 [US2] Incluir provider y modelo efectivo en errores de Gemini en backend/aphra_blogger/llm/gemini_provider.py
- [X] T020 [US2] Homogeneizar mensajes de error de creación de proveedor en backend/aphra_blogger/llm/factory.py

**Checkpoint**: US2 operativa y verificable de forma independiente

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Robustez transversal y cierre de calidad

- [X] T021 [P] Implementar parseo robusto de respuesta JSON en backend/aphra_blogger/agents/image_selector.py
- [X] T022 [P] Añadir pruebas de respuesta vacía/no JSON para imagen y crítica en backend/tests/test_agents.py
- [X] T023 Actualizar contrato de compatibilidad provider-model en specs/006-fix-gemini-api-key/contracts/llm-provider-contract.md
- [X] T024 [P] Validar escenario end-to-end y registrar salida en backend/outputs/Elfuturoesopenclaw.json
- [X] T025 Ejecutar suite objetivo y documentar resultado en specs/006-fix-gemini-api-key/quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- Phase 1: sin dependencias
- Phase 2: depende de Phase 1 y bloquea historias
- Phase 3 (US1): depende de Phase 2
- Phase 4 (US2): depende de Phase 2
- Phase 5: depende de US1 y US2

### User Story Dependencies

- US1: requiere resolución provider-model y validación de credenciales implementadas en Phase 2
- US2: requiere base de validación y propagación de errores de Phase 2; puede ejecutarse en paralelo con US1 tras completar Phase 2

### Within Each User Story

- Crear pruebas de regresión de la historia antes de cambios de implementación
- Ajustar configuración/proveedor antes de validación de flujo completo
- Validar historia de forma independiente antes de avanzar

---

## Parallel Execution Examples

### User Story 1

```bash
T009 backend/tests/test_orchestrator_config.py
T010 backend/tests/test_orchestrator.py
```

```bash
T011 backend/src/orchestrator/config.py
T012 backend/src/orchestrator/main.py
```

### User Story 2

```bash
T016 backend/tests/test_orchestrator_config.py
T017 backend/tests/test_orchestrator.py
```

```bash
T019 backend/aphra_blogger/llm/gemini_provider.py
T020 backend/aphra_blogger/llm/factory.py
```

---

## Implementation Strategy

### MVP First (US1)

1. Completar Phase 1
2. Completar Phase 2
3. Completar Phase 3 (US1)
4. Validar ejecución real con `--provider gemini`

### Incremental Delivery

1. Base técnica (Phase 1-2)
2. Entrega US1 validada
3. Entrega US2 validada
4. Cierre de robustez transversal (Phase 5)

### Parallel Team Strategy

1. Equipo completa Phase 1 y Phase 2
2. Un frente implementa US1 y otro US2 en paralelo
3. Ambos convergen en Phase 5 para hardening y validación final

---

## Notes

- Todas las tareas usan formato checklist estricto con ID secuencial
- Las tareas `[P]` son paralelizables al tocar archivos distintos o sin dependencia directa
- Las tareas `[US1]` y `[US2]` están encapsuladas para pruebas independientes

---

## Tech Debt Tasks (Generated by /speckit.cleanup)

**Generated**: 2026-04-06T00:00:00Z
**Source**: Post-implementation cleanup of 006-fix-gemini-api-key
**Priority**: Address before next feature iteration

### Detected Issues

- [ ] TD001 [P] Endurecer selección de `agent_api_key` en `backend/src/orchestrator/main.py` para reducir riesgo de mezcla de credenciales cuando `provider=auto`
- [ ] TD002 Añadir prueba de no filtrado de secretos en mensajes de error/log en `backend/tests/test_orchestrator.py` y `backend/tests/test_orchestrator_config.py`
- [ ] TD003 Actualizar documentación de la feature para unificar referencia de SDK Gemini (`google-genai`) en `specs/006-fix-gemini-api-key/spec.md`
