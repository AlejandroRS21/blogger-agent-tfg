# Research: Publicacion continua de novedades tecnologicas

## Decision 1: Scheduler por cadencia fija de 12 horas con control de estado operativo

- Decision: Ejecutar el ciclo continuo con un scheduler de cadencia fija de 12 horas y estado explicito activo, pausado y degradado.
- Rationale: La cadencia ya esta aclarada en spec y requiere una base determinista para medir cumplimiento operativo mensual.
- Alternatives considered:
  - Cadencia dinamica por volumen de noticias: rechazada para esta fase por complejidad operativa y dificultad de auditoria.
  - Trigger solo manual: rechazada porque incumple publicacion continua.

## Decision 2: Seleccion tematica multi-fuente con fallback

- Decision: Construir la seleccion de temas a partir de multiples fuentes (APIs de actualidad y feeds RSS) con fallback automatico si una fuente falla.
- Rationale: Reduce puntos unicos de fallo y mejora cobertura tematica sin romper la continuidad.
- Alternatives considered:
  - Una sola API principal: rechazada por riesgo alto de indisponibilidad.
  - Scraping exclusivo de sitios concretos: rechazado por fragilidad de estructura y mantenimiento.

## Decision 3: Politica de recuperacion con reintentos acotados

- Decision: Aplicar 3 reintentos por ciclo con backoff 5m, 15m y 30m para fallos transitorios.
- Rationale: Balancea resiliencia con control de tiempo total por ciclo y evita loops indefinidos.
- Alternatives considered:
  - Reintentos infinitos hasta exito: rechazado por riesgo de bloqueo de ciclos siguientes.
  - Sin reintentos: rechazado por baja robustez ante fallos temporales de red/proveedor.

## Decision 4: Anti-duplicado por similitud semantica en ventana temporal

- Decision: Tratar como redundante cualquier publicacion con similitud >= 80% respecto a articulos de los ultimos 14 dias.
- Rationale: Mantiene variedad editorial y alinea criterio de calidad con la aclaracion cerrada en spec.
- Alternatives considered:
  - Deteccion por titulo exacto: rechazada por insuficiente frente a reformulaciones.
  - Ventana de 7 dias: rechazada por cobertura corta para un blog tecnico.

## Decision 5: Continuidad operacional con parada explicita acotada

- Decision: Mantener continuidad del ciclo incluso ante fallos individuales; detener solo por pausa manual o degradacion critica sostenida mayor de 24 horas.
- Rationale: Cumple objetivo de servicio continuo evitando caidas completas por errores aislados.
- Alternatives considered:
  - Detener al primer fallo: rechazada por impacto en disponibilidad.
  - No permitir pausa manual: rechazada por falta de control operativo.

## Decision 6: Contrato de salida canonica sobre docs

- Decision: Validar exito funcional final sobre artefactos estaticos docs/posts.json y docs/posts en cada verificacion integral.
- Rationale: La constitucion fija docs como superficie canonica de entrega publica.
- Alternatives considered:
  - Validar solo en outputs intermedios backend: rechazado por no garantizar publicacion visible para lectores.
