# Implementation Plan: Workflow resiliente para Gemini y selección de imágenes

**Branch**: `006-fix-gemini-api-key` | **Date**: 2026-04-04 | **Spec**: `/specs/006-fix-gemini-api-key/spec.md`
**Input**: Feature specification from `/specs/006-fix-gemini-api-key/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Corregir la inicialización y ejecución del workflow cuando se usa proveedor Gemini para evitar llamadas con modelos incompatibles (ej. `meta-llama/...`), y robustecer la fase de selección de imágenes para no degradar silenciosamente por respuestas no JSON o vacías. El enfoque técnico aplica resolución de modelo por proveedor, validación previa de compatibilidad y parseo tolerante en agentes que esperan JSON estructurado.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11+  
**Primary Dependencies**: `google-genai`, `pytest`, `python-dotenv`, agentes `aphra_blogger`  
**Storage**: Archivos locales JSON en `backend/outputs/` y estado en memoria del workflow  
**Testing**: `pytest` (unit + integration de orquestador y agentes)  
**Target Platform**: Linux local + ejecución CI
**Project Type**: Backend Python de orquestación multi-agente (CLI + librería interna)  
**Performance Goals**: Mantener duración total de workflow en el mismo orden de magnitud actual (segundos) sin reintentos en cascada por modelo inválido  
**Constraints**: Sin credenciales hardcodeadas; mantener fallback seguro ante error de proveedor; compatibilidad con OpenAI/HF/Modal  
**Scale/Scope**: Corrección acotada a resolución de proveedor/modelo, parseo de respuesta y validaciones de configuración

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Gate I. Python Pipeline Ownership**: PASS. Cambios acotados a módulos Python de `backend/src/orchestrator` y `backend/aphra_blogger`.
- **Gate II. Reproducible Content Generation**: PASS con acción. Se documenta estrategia de resolución de modelo para reproducibilidad por proveedor.
- **Gate III. Automated Verification First**: PASS con acción. Se requieren tests para selección de modelo y parseo JSON en `ImageSelectorAgent`.
- **Gate IV. Provenance, Privacy, and Safe Output**: PASS. Se evita exponer tokens en errores y se conserva fallback sin datos sensibles.
- **Gate V. Static Delivery as Canonical Publish Target**: PASS. No hay cambios de schema en `docs/`.

## Project Structure

### Documentation (this feature)

```text
specs/006-fix-gemini-api-key/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── llm-provider-contract.md
└── tasks.md
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
backend/
├── src/orchestrator/
│   ├── config.py
│   ├── main.py
│   └── runner.py
├── aphra_blogger/
│   ├── llm/
│   │   ├── factory.py
│   │   └── gemini_provider.py
│   └── agents/
│       ├── content_generator.py
│       ├── critic.py
│       └── image_selector.py
└── tests/
  ├── test_orchestrator.py
  ├── test_orchestrator_config.py
  └── test_agents.py

frontend/
└── (sin cambios para esta feature)
```

**Structure Decision**: Se adopta estructura tipo web application ya existente (backend + frontend), con cambios solo en backend y pruebas de backend.

## Post-Design Constitution Check

- **Gate I. Python Pipeline Ownership**: PASS.
- **Gate II. Reproducible Content Generation**: PASS. Se define contrato explícito provider-model.
- **Gate III. Automated Verification First**: PASS condicionado a implementar tests en tareas.
- **Gate IV. Provenance, Privacy, and Safe Output**: PASS.
- **Gate V. Static Delivery as Canonical Publish Target**: PASS (sin impacto en `docs/`).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
