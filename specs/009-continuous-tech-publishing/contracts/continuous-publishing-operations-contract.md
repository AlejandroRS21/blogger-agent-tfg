# Contract: Continuous Publishing Operations

## Scope

Define el comportamiento observable para operar publicacion continua de novedades tecnologicas, incluyendo control operativo, recuperacion ante fallos y consistencia de salida publicada.

## Inputs

- Configuracion de ciclo continuo con cadencia base de 12 horas.
- Fuentes de temas de actualidad (APIs y RSS) con prioridad y fallback.
- Estado operativo solicitado por operador: active o paused.
- Ventana de historial reciente para validacion anti-duplicado (14 dias).

## Operational Interface Contract

- Operacion Start Continuous Publishing
  - Precondicion: configuracion valida y estado actual no activo.
  - Efecto esperado: estado pasa a active y se programa el siguiente ciclo.

- Operacion Pause Continuous Publishing
  - Precondicion: estado actual active o degraded.
  - Efecto esperado: estado pasa a paused sin perder planificacion pendiente.

- Operacion Resume Continuous Publishing
  - Precondicion: estado actual paused.
  - Efecto esperado: estado vuelve a active y reanuda programacion.

- Operacion Get Operational Status
  - Devuelve: estado actual, ultimo ciclo, ultimo resultado, resumen de incidentes abiertos.

## Rules

1. Cada ciclo debe ejecutar seleccion de tema actual, generacion, validacion y publicacion o registrar fallo explicito.
2. Ante fallo transitorio, el sistema aplica como maximo 3 reintentos con backoff progresivo.
3. El sistema no debe detener ciclos futuros por un fallo individual.
4. Se rechaza publicacion redundante si similitud >= 80% contra la ventana de 14 dias.
5. Toda ejecucion y todo fallo deben quedar trazados con marca temporal y causa.
6. La publicacion valida final debe reflejarse en docs/posts.json y docs/posts.
7. Si no hay TopicCandidate valido tras filtros, el ciclo debe cerrarse como skipped_with_reason con reason_code normalizado.
8. Si no existen fuentes confiables disponibles tras allowlist y fallback, el ciclo debe registrarse como source_exhausted.
9. Deben emitirse alertas operativas cuando success-rate o lag de ciclo incumplan umbrales definidos.

## Error Contract

- Error de seleccion de tema
  - Se registra incidente con stage topic_selection y reason_code.
  - Se activa politica de recuperacion del ciclo.

- Error de generacion o validacion
  - Se registra incidente con stage generation o validation.
  - Si se agotan reintentos, el ciclo queda failed y el scheduler continua.

- Error de publicacion
  - Se registra incidente con stage publish y evidencia de artefacto no escrito o inconsistente.
  - El ciclo se marca failed o degraded segun severidad.

## Output Contract

- Estado operativo consultable: active, paused, degraded.
- Historial de ciclos consultable con resultado por intento.
- Historial de incidentes consultable con severidad y estado de resolucion.
- Artefactos canonicos en docs actualizados solo para publicaciones exitosas.
- Alertas operativas consultables con codigo, severidad y marca temporal.

## Non-Goals

- No define estrategia SEO detallada del contenido.
- No define interfaz visual de monitorizacion en frontend para esta fase.
- No incluye migracion masiva de articulos historicos.
