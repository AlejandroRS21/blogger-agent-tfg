# Implementation Plan: Publicacion Continua de Novedades Tecnologicas

**Branch**: 009-continuous-tech-publishing | **Date**: 2026-04-09 | **Spec**: /specs/009-continuous-tech-publishing/spec.md
**Input**: Feature specification from /specs/009-continuous-tech-publishing/spec.md

**Note**: This template is filled in by the /speckit.plan command. See .specify/templates/plan-template.md for the execution workflow.

## Summary

Habilitar un flujo de publicacion continua con cadencia base de 12 horas, seleccion de temas tech actuales desde multiples fuentes con fallback, controles anti-duplicado, y operacion resiliente con reintentos y trazabilidad operativa. El enfoque prioriza ejecucion backend en Python, verificaciones automatizadas y consistencia del destino canonico de publicacion en docs.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: daggr, pydantic, python-dotenv, httpx, beautifulsoup4, lxml, tenacity, modal, gradio  
**Storage**: Archivos locales JSON y HTML en docs y backend/outputs, estado de ejecucion en memoria con persistencia de historico operativo en artefactos  
**Testing**: pytest y pytest-asyncio para unit, integration y regresion de orquestacion/publicacion  
**Target Platform**: Linux para desarrollo y CI, despliegue de ejecucion continua en Modal  
**Project Type**: Aplicacion web con backend de orquestacion multiagente y publicacion estatica en docs  
**Performance Goals**: Cumplir 2 publicaciones diarias en operacion normal, con recuperacion automatica de fallos transitorios sin detener el ciclo global  
**Constraints**: Mantener consistencia de docs/posts.json y docs/posts, evitar duplicacion semantica >= 80% en 14 dias, no detener operacion salvo pausa manual o degradacion critica sostenida  
**Scale/Scope**: Flujo continuo para un blog tecnico unico con horizonte operativo mensual y auditoria completa de intentos/publicaciones

## Trust Boundaries & Security Controls

- Trusted boundary interna: modulos de orquestacion y publicacion en backend.
- Untrusted boundary externa: APIs de noticias, RSS y cualquier contenido remoto previo a validacion.
- Controles obligatorios de ingesta antes de generacion:
    - allowlist de dominios/fuentes aprobadas para consumo operativo,
    - sanitizacion de HTML/texto remoto para eliminar contenido activo o no confiable,
    - limites de tamano y contexto por item ingerido para evitar desbordes y ruido,
    - neutralizacion de instrucciones embebidas en contenido externo para reducir riesgo de prompt injection indirecta.
- Regla de seguridad: ningun contenido externo cruza a etapa de generacion sin pasar por estos controles.

## Operational SLI/SLO and Alerts

- SLI-1 Daily Success Rate: porcentaje de ciclos diarios con resultado published o skipped_with_reason valido.
- SLI-2 Cycle Lag: diferencia entre scheduled_at y cierre efectivo del ciclo.
- SLI-3 Critical Open Incidents: numero de incidentes criticos abiertos.
- SLO objetivo:
    - Daily Success Rate >= 90%.
    - Cycle Lag <= 90 minutos en operacion normal.
    - Critical Open Incidents = 0 sostenido.
- Umbrales de alerta:
    - alertar en menos de 5 minutos cuando SLI-1 < 90% en ventana diaria,
    - alertar en menos de 5 minutos cuando SLI-2 > 90 minutos,
    - alertar inmediatamente ante cualquier incidente critico abierto.
- Accion automatica por calidad: activar pausa controlada si relevancia semanal < 70% por 2 semanas consecutivas.

## Failure State Extensions

- Estados adicionales del ciclo para comportamiento determinista:
    - skipped_with_reason: ciclo cerrado sin publicacion por ausencia de tema valido,
    - source_exhausted: agotamiento de fuentes tras fallback y retries,
    - degraded: continuidad afectada pero scheduler activo.
- Transiciones clave:
    - running -> skipped_with_reason cuando no existe TopicCandidate valido,
    - running -> source_exhausted cuando no hay fuentes utilizables tras fallback,
    - source_exhausted -> degraded cuando persiste agotamiento dentro de la ventana operativa,
    - degraded -> paused por accion manual o por pausa automatica de calidad.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Gate I. Python Pipeline Ownership: PASS. El diseno concentra scheduler, seleccion de temas, validacion y publicacion en modulos Python de backend.
- Gate II. Reproducible Content Generation: PASS con accion. Se exige trazabilidad de ciclo, fuentes y resultado de publicacion por intento.
- Gate III. Automated Verification First: PASS con accion. Se planifican pruebas unitarias e integracion para cadencia, retries, anti-duplicados y estados operativos.
- Gate IV. Provenance, Privacy, and Safe Output: PASS. Se separan claramente fuentes externas, artefactos generados y salida canonica publicada.
- Gate V. Static Delivery as the Canonical Publish Target: PASS. La salida valida final se confirma sobre docs/posts.json y docs/posts.

## Project Structure

### Documentation (this feature)

text
specs/009-continuous-tech-publishing/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── continuous-publishing-operations-contract.md
└── tasks.md

### Source Code (repository root)

text
backend/
├── src/orchestrator/
│   ├── main.py
│   ├── runner.py
│   ├── state.py
│   └── config.py
├── aphra_blogger/
│   ├── agents/
│   │   ├── research_agent.py
│   │   ├── content_generator.py
│   │   └── html_builder.py
│   └── workflows/
├── modal_app.py
└── tests/
    ├── test_workflow.py
    ├── test_orchestrator.py
    ├── test_scraper.py
    └── test_structural_diversity.py

frontend/
├── app/
├── __tests__/
└── package.json

docs/
├── posts.json
└── posts/

**Structure Decision**: Se usa la estructura existente backend + frontend + docs, implementando la logica continua en backend Python y validando el resultado final en artefactos estaticos de docs como superficie canonica.

## Post-Design Constitution Check

- Gate I. Python Pipeline Ownership: PASS. Se define separacion por responsabilidades en ciclo, seleccion de tema, generacion, validacion y publicacion.
- Gate II. Reproducible Content Generation: PASS. El modelo de datos incorpora trazabilidad de fuentes y resultados por ciclo.
- Gate III. Automated Verification First: PASS. Quickstart y contrato incluyen escenarios verificables para cadencia, recuperacion y continuidad.
- Gate IV. Provenance, Privacy, and Safe Output: PASS. El contrato operacional exige registro sin exponer secretos y delimitacion de artefactos.
- Gate V. Static Delivery as the Canonical Publish Target: PASS. Contrato y quickstart validan explicitamente consistencia en docs/posts.json y docs/posts.

## Resilience Test Expansion

- Incluir pruebas de fallos parciales y corrupcion de datos externos:
    - timeout en fuente principal con fallback exitoso,
    - respuestas 429/5xx con reintento y backoff,
    - RSS malformado y payload parcial,
    - contenido externo con instrucciones embebidas que debe ser neutralizado.
- Incluir pruebas de estados operativos extendidos:
    - cierre skipped_with_reason sin bloquear siguiente ciclo,
    - transicion source_exhausted -> degraded,
    - alerta emitida dentro de SLA de 5 minutos para SLI incumplidos.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
