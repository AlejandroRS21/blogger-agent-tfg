# Feature Specification: Publicacion Continua de Novedades Tecnologicas

**Feature Branch**: `[009-continuous-tech-publishing]`  
**Created**: 2026-04-09  
**Status**: Draft  
**Input**: User description: "el proyecto esta muy conseguido pero aun falta algo, que continuamente vaya publicando posts de temas actuales relacionados con todas las novedades tecnologicas top, es decir esto tiene que funcionar continuamente publicando articulos"

## Clarifications

### Session 2026-04-09

- Q: Cual es la cadencia exacta de publicacion continua para esta fase? -> A: Cada 12 horas (2 publicaciones al dia).
- Q: Cual debe ser la estrategia de fuentes para actualidad tematica? -> A: Multiples fuentes (APIs de noticias + RSS) con fallback automatico.
- Q: Cual es la politica de recuperacion para fallos transitorios? -> A: 3 reintentos por ciclo con backoff 5m/15m/30m.
- Q: Que condiciones de parada explicita aplican? -> A: Solo pausa manual o degradacion critica sostenida superior a 24 horas.
- Q: Como se define redundancia para evitar duplicados? -> A: Similitud de contenido >= 80% dentro de una ventana de 14 dias.
- Q: Que ocurre si no hay tema publicable tras filtros de actualidad y duplicado? -> A: El ciclo se cierra como skipped_with_reason y se registra causa normalizada sin bloquear ciclos futuros.
- Q: Que controles de seguridad aplican a la ingesta externa? -> A: Sanitizacion obligatoria, allowlist de dominios, limites de tamano/contexto y neutralizacion de instrucciones embebidas antes de generacion.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Publicacion automatica continua (Priority: P1)

Como responsable del blog, quiero que el sistema publique articulos de forma continua sobre novedades tecnologicas actuales para mantener el sitio siempre actualizado sin depender de intervencion manual diaria.

**Why this priority**: Es el objetivo principal del feature y la fuente directa de valor: mantener actividad constante y relevancia editorial.

**Independent Test**: Puede validarse ejecutando un periodo de prueba continuo y comprobando que se publican articulos nuevos con cadencia definida y sin acciones manuales.

**Acceptance Scenarios**:

1. **Given** que el sistema de publicacion continua esta activo, **When** transcurre el intervalo configurado de publicacion, **Then** se publica un nuevo articulo en estado visible para lectores.
2. **Given** que ya existe una cola de temas pendientes, **When** se completa una publicacion, **Then** el sistema programa automaticamente la siguiente sin intervencion manual.
3. **Given** que no hay intervencion humana durante un periodo operativo completo, **When** finaliza ese periodo, **Then** existe evidencia de publicaciones nuevas realizadas de forma autonoma.

---

### User Story 2 - Relevancia y actualidad tematica (Priority: P2)

Como lector del blog, quiero recibir articulos sobre tendencias y novedades tecnologicas recientes para percibir el contenido como util, moderno y alineado con el mercado.

**Why this priority**: Publicar en continuo no aporta valor si los temas no son actuales ni relevantes.

**Independent Test**: Puede validarse revisando una muestra de articulos publicados en un periodo y verificando que sus temas corresponden a novedades tecnologicas recientes y variadas.

**Acceptance Scenarios**:

1. **Given** un ciclo de publicacion activo, **When** se genera una nueva tanda de articulos, **Then** los temas seleccionados pertenecen a categorias de alta actualidad tecnologica.
2. **Given** una ventana de publicaciones recientes, **When** se analiza la secuencia tematica, **Then** no se observan repeticiones consecutivas del mismo enfoque salvo que exista una novedad claramente distinta.

---

### User Story 3 - Control operativo y continuidad (Priority: P3)

Como operador del sistema, quiero visualizar el estado de la publicacion continua y los incidentes para detectar interrupciones y restablecer rapidamente la normalidad.

**Why this priority**: Asegura confiabilidad operacional y reduce tiempos de parada.

**Independent Test**: Puede validarse forzando errores en una ejecucion y confirmando que quedan registrados, el sistema intenta recuperarse y la operacion continua.

**Acceptance Scenarios**:

1. **Given** que ocurre un fallo en la generacion o publicacion, **When** el fallo sucede, **Then** el sistema registra el incidente con motivo y hora.
2. **Given** un fallo transitorio, **When** el sistema aplica su politica de recuperacion, **Then** reanuda la publicacion continua sin perder la planificacion general.

### Edge Cases

- Que ocurre cuando no hay temas nuevos suficientemente relevantes en la ventana temporal actual.
- Que ocurre cuando se intenta publicar un articulo demasiado similar a uno reciente.
- Como actua el sistema si se acumulan fallos consecutivos y no puede publicar durante varios intervalos.
- Como se comporta el sistema ante picos de volumen de novedades tecnologicas en una misma categoria.
- Que ocurre si una publicacion queda incompleta o invalida justo antes de su salida.
- Que ocurre cuando fallan temporalmente varias fuentes externas y solo queda disponible una fuente de respaldo.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST ejecutar un ciclo continuo de publicacion sin requerir lanzamiento manual en cada articulo.
- **FR-002**: El sistema MUST mantener una cadencia de publicacion de 12 horas por defecto (2 publicaciones al dia), configurable por operacion para futuras fases sin afectar esta meta base.
- **FR-003**: El sistema MUST seleccionar temas orientados a novedades tecnologicas recientes en cada ciclo de publicacion.
- **FR-004**: El sistema MUST evitar publicaciones duplicadas o sustancialmente redundantes considerando redundancia cuando la similitud de contenido sea >= 80% en una ventana de 14 dias.
- **FR-005**: El sistema MUST aplicar reglas de diversidad tematica para no concentrar todas las publicaciones en una sola subcategoria tecnologica.
- **FR-006**: El sistema MUST validar cada articulo antes de su publicacion para asegurar completitud minima (titulo, cuerpo y fecha).
- **FR-007**: El sistema MUST registrar el resultado de cada intento de publicacion (exito o fallo) con marca temporal y motivo cuando aplique.
- **FR-008**: El sistema MUST reintentar automaticamente una publicacion fallida con 3 reintentos maximos por ciclo y backoff progresivo de 5m, 15m y 30m.
- **FR-009**: El sistema MUST continuar con el siguiente ciclo aunque un intento individual falle, salvo si existe pausa manual o degradacion critica sostenida superior a 24 horas.
- **FR-010**: Los operadores MUST poder pausar y reanudar la publicacion continua sin perder el estado de planificacion.
- **FR-011**: El sistema MUST exponer un estado operativo legible que indique si la publicacion continua esta activa, pausada o degradada.
- **FR-012**: El sistema MUST conservar un historial consultable de publicaciones generadas para auditoria editorial.
- **FR-013**: El sistema MUST seleccionar temas usando multiples fuentes de actualidad tecnologica con fallback automatico cuando una fuente no este disponible.
- **FR-014**: El sistema MUST cerrar el ciclo como skipped_with_reason cuando no exista TopicCandidate valido tras aplicar reglas de actualidad, diversidad y anti-duplicado, registrando reason_code y manteniendo la programacion de ciclos siguientes.
- **FR-015**: El sistema MUST aplicar controles de confianza sobre datos externos antes de su uso en generacion: allowlist de fuentes, sanitizacion de contenido, limites de tamano/contexto y neutralizacion de instrucciones embebidas.
- **FR-016**: El sistema MUST emitir alertas operativas cuando se incumplan los umbrales de continuidad o lag de ciclo definidos para operacion normal.

### Key Entities *(include if feature involves data)*

- **Publication Cycle**: Unidad temporal de operacion continua; incluye estado, hora planificada, resultado y referencias a intentos.
- **Topic Candidate**: Propuesta de tema tecnologico reciente con categoria, nivel de prioridad editorial y señal de actualidad.
- **Article Draft**: Contenido preparado para publicar con metadatos editoriales, validaciones y estado de calidad.
- **Published Article Record**: Registro final de cada publicacion con identificador, fecha/hora, tema principal y resultado operativo.
- **Operational Incident**: Evento de error o degradacion con causa, severidad, momento de deteccion y estado de resolucion.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Durante una ventana continua de 30 dias, al menos el 95% de los intervalos programados finalizan con una publicacion exitosa.
- **SC-007**: Con la cadencia base definida, el sistema entrega 2 publicaciones diarias de forma sostenida durante operacion normal.
- **SC-002**: El tiempo de interrupcion acumulado de la publicacion continua no supera el 2% del tiempo operativo mensual.
- **SC-003**: Al menos el 90% de los articulos publicados en cada semana tratan temas identificables como novedades tecnologicas recientes.
- **SC-004**: Menos del 5% de publicaciones mensuales son marcadas como redundantes respecto a articulos recientes.
- **SC-005**: El 100% de los fallos de publicacion quedan registrados con informacion suficiente para diagnostico operativo.
- **SC-006**: En evaluacion editorial mensual, al menos el 85% de una muestra representativa de articulos se considera relevante para audiencia interesada en tendencias tech.
- **SC-008**: Ante violaciones de continuidad (success rate diario < 90%) o lag de ciclo > 90 minutos, el sistema emite alerta operativa en menos de 5 minutos.
- **SC-009**: Si la relevancia semanal cae por debajo de 70% durante 2 semanas consecutivas, el sistema activa pausa automatica controlada y notifica a operacion para revision editorial.

## Assumptions

- Existe una fuente continua de temas tecnologicos recientes apta para mantener la frecuencia de publicacion objetivo.
- Las fuentes de actualidad tecnologica combinan proveedores estructurados (API) y fuentes sindicadas (RSS), con disponibilidad razonable para fallback.
- La prioridad del alcance es continuidad y actualidad; la expansion a otros dominios editoriales queda fuera de esta fase.
- El sistema ya dispone de mecanismos basicos para mostrar articulos una vez publicados.
- El equipo operativo revisa periodicamente indicadores y alertas para actuar ante incidencias prolongadas.
- Se considera aceptable que algunos intervalos puntuales fallen siempre que se mantenga la continuidad global definida en criterios de exito.
