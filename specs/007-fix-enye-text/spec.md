# Feature Specification: Preservar caracteres ñ en artículos

**Feature Branch**: `007-fix-enye-text`  
**Created**: 6 de abril de 2026  
**Status**: Draft  
**Input**: User description: "las ñ no estan en ningun articulo , cuando se escribe algo con ñ lo pone con n , sokucionar esto"

## Clarifications

### Session 2026-04-06

- Q: ¿Cuál debe ser el comportamiento con artículos históricos ya dañados (`ñ` convertida a `n`)? → A: Opción B - corregir contenido nuevo y permitir regeneración/corrección manual de históricos.

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Escritura fiel del castellano (Priority: P1)

Como editor del blog, quiero que los artículos mantengan la letra `ñ` cuando se genera y publica contenido, para no perder calidad lingüística ni cambiar el significado de palabras en español.

**Why this priority**: Es el valor principal del problema reportado: hoy se altera el texto final y baja la calidad editorial de todos los posts afectados.

**Independent Test**: Generar un artículo con varias palabras con `ñ` (por ejemplo: "año", "niñez", "señal", "España") y verificar que en el resultado publicado aparecen exactamente con `ñ`.

**Acceptance Scenarios**:

1. **Given** un contenido fuente que incluye `ñ`, **When** se completa la generación del artículo, **Then** el contenido final conserva todos los caracteres `ñ` sin convertirlos en `n`.
2. **Given** un artículo ya generado con `ñ`, **When** se publica y se visualiza en el blog, **Then** la interfaz muestra esos caracteres correctamente.

---

### User Story 2 - Consistencia entre fases del flujo (Priority: P2)

Como mantenedor del sistema, quiero que todas las fases de procesamiento del artículo conserven caracteres propios del español, para evitar que una fase intermedia degrade el texto aunque la fase inicial sea correcta.

**Why this priority**: El fallo puede ocurrir en una etapa intermedia y provocar regresiones silenciosas aunque el resultado aparente estar bien generado.

**Independent Test**: Ejecutar un flujo completo con términos que incluyan `ñ` y comprobar que cada salida intermedia relevante conserva los mismos caracteres especiales.

**Acceptance Scenarios**:

1. **Given** un flujo de generación completo, **When** se revisan las salidas entre fases, **Then** no se observan sustituciones de `ñ` por `n`.

---

### User Story 3 - Prevención de regresiones editoriales (Priority: P3)

Como responsable de calidad, quiero contar con una verificación repetible sobre caracteres españoles, para detectar de forma temprana cualquier regresión futura.

**Why this priority**: Reduce retrabajo y evita que el problema reaparezca tras cambios posteriores del pipeline.

**Independent Test**: Ejecutar una validación automatizada con un conjunto fijo de frases en español y confirmar que pasa en todas las ejecuciones; adicionalmente, validar que un artículo histórico puede corregirse mediante regeneración/corrección manual.

**Acceptance Scenarios**:

1. **Given** una batería de validación lingüística, **When** se ejecuta en una versión nueva del sistema, **Then** el resultado confirma que no hay pérdidas de `ñ`.

---

### Edge Cases

- ¿Qué ocurre cuando un artículo incluye muchas palabras con `ñ` en títulos, subtítulos, cuerpo y metadatos a la vez?
- ¿Qué ocurre cuando el texto mezcla `ñ` con otros caracteres acentuados y signos de apertura (`¿`, `¡`)?
- ¿Cómo se comporta el sistema si el contenido llega desde distintas fuentes con codificaciones de texto heterogéneas?
- ¿Qué ocurre con artículos ya existentes que fueron degradados (si se regeneran o actualizan)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema DEBE preservar el carácter `ñ` en todo el contenido generado en español.
- **FR-002**: El sistema DEBE evitar cualquier sustitución automática de `ñ` por `n` durante el procesamiento del artículo.
- **FR-003**: El sistema DEBE conservar `ñ` tanto en contenido principal como en datos asociados del artículo (por ejemplo, título, resumen y texto visible).
- **FR-004**: El sistema DEBE mantener consistencia textual entre las distintas etapas de generación y publicación para caracteres españoles.
- **FR-005**: El sistema DEBE incluir una validación repetible que detecte pérdidas de caracteres españoles antes de considerar una ejecución como correcta.
- **FR-006**: El sistema DEBE seguir permitiendo la publicación normal de artículos que no contengan `ñ`, sin afectar su contenido.
- **FR-007**: El sistema DEBE garantizar que la visualización final del artículo en el blog muestre `ñ` correctamente.
- **FR-008**: El alcance de esta feature DEBE aplicarse de forma obligatoria a contenido nuevo; para artículos históricos degradados, la corrección DEBE realizarse por regeneración o corrección manual bajo demanda.

### Key Entities *(include if feature involves data)*

- **Artículo Generado**: Contenido textual final listo para publicar; incluye título, cuerpo y resumen.
- **Salida Intermedia de Flujo**: Representa versiones parciales del texto durante el pipeline; debe conservar integridad lingüística.
- **Regla de Validación Lingüística**: Criterio de calidad que verifica que caracteres españoles (incluida `ñ`) no se degradan.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100% de los artículos de validación que incluyen `ñ` mantienen esos caracteres sin sustituciones en la salida publicada.
- **SC-002**: El 100% de los casos de prueba con palabras en español que contienen `ñ` superan la validación lingüística definida para esta feature.
- **SC-003**: Se reduce a 0 la aparición de incidencias reportadas por reemplazo de `ñ` por `n` en los artículos nuevos generados tras el despliegue.
- **SC-004**: Los artículos sin `ñ` siguen publicándose sin regresiones de formato ni contenido en al menos el 95% de la muestra de control.

## Assumptions

- Se asume que el idioma objetivo principal de los artículos afectados es español.
- Se asume que el problema ocurre dentro del flujo interno de generación/publicación y no por edición manual posterior.
- Se asume que esta feature no ejecuta una migración masiva automática del histórico; los artículos antiguos se corrigen de forma manual o bajo demanda.
- Se asume que la interfaz de blog ya es capaz de renderizar correctamente texto en español cuando recibe contenido íntegro.
