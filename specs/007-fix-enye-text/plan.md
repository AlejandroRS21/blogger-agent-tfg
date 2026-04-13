# Implementation Plan: Preservar caracteres ñ en artículos

**Branch**: `007-fix-enye-text` | **Date**: 2026-04-06 | **Spec**: `/specs/007-fix-enye-text/spec.md`
**Input**: Feature specification from `/specs/007-fix-enye-text/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Corregir la degradación de caracteres españoles (especialmente `ñ`) durante generación y publicación de artículos. El enfoque define un contrato explícito de preservación Unicode en el pipeline, valida que no exista transliteración en contenido visible, y añade verificación automatizada de regresión sobre artefactos publicados en `docs/`.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: `daggr`, `pydantic`, `python-dotenv`, `pytest`, agentes `aphra_blogger`, serialización JSON estándar  
**Storage**: Archivos locales JSON/HTML en `docs/`, salidas de workflow en `backend/outputs/`  
**Testing**: `pytest` (unit + integration + regression de contenido textual)  
**Target Platform**: Linux local y CI
**Project Type**: Aplicación web con backend de generación + frontend Next.js + publicación estática en `docs/`  
**Performance Goals**: Sin degradación perceptible en runtime del pipeline actual; validación lingüística adicional de coste bajo  
**Constraints**: No introducir transliteración de contenido visible; mantener compatibilidad con artículos sin `ñ`; no migración masiva automática de histórico  
**Scale/Scope**: Alcance acotado al flujo de generación/publicación y validación de regresión para nuevos artículos

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Gate I. Python Pipeline Ownership**: PASS. Cambios localizados en backend/orquestación y validación de pipeline.
- **Gate II. Reproducible Content Generation**: PASS. Se fijan entradas de validación con frases controladas y evidencia en artefactos publicados.
- **Gate III. Automated Verification First**: PASS con acción. Se incorporan pruebas automáticas de preservación de `ñ` y no regresión.
- **Gate IV. Provenance, Privacy, and Safe Output**: PASS. Sin exposición de secretos; solo cambios de preservación textual.
- **Gate V. Static Delivery as the Canonical Publish Target**: PASS. La validación se centra en `docs/posts.json` y posts publicados.

## Project Structure

### Documentation (this feature)

```text
specs/007-fix-enye-text/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── unicode-preservation-contract.md
└── tasks.md
```

### Source Code (repository root)
```text
backend/
├── src/orchestrator/
│   ├── main.py
│   ├── runner.py
│   └── state.py
├── aphra_blogger/agents/
│   ├── content_generator.py
│   └── html_builder.py
└── tests/
    ├── test_orchestrator.py
    ├── test_agents.py
    └── test_html_builder.py

frontend/
├── app/lib/api.ts
└── __tests__/

docs/
├── posts.json
└── posts/
```

**Structure Decision**: Se mantiene la estructura web actual del repositorio (backend + frontend + docs), implementando la corrección en pipeline backend y verificando resultado en artefactos estáticos publicados.

## Post-Design Constitution Check

- **Gate I. Python Pipeline Ownership**: PASS.
- **Gate II. Reproducible Content Generation**: PASS con casos de validación lingüística definidos.
- **Gate III. Automated Verification First**: PASS sujeto a tareas de tests en fase `/speckit.tasks`.
- **Gate IV. Provenance, Privacy, and Safe Output**: PASS.
- **Gate V. Static Delivery as the Canonical Publish Target**: PASS; contrato y quickstart verifican `docs/`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
