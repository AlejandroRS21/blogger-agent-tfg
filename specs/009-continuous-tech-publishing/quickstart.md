# Quickstart: Publicacion Continua de Novedades Tecnologicas

Esta guia permite validar, en entorno local, el comportamiento esperado de publicacion continua con cadencia de 12 horas y recuperacion ante fallos.

## Prerrequisitos

- Entorno Python 3.11+ activo en backend.
- Dependencias instaladas con el gestor definido por el proyecto.
- Configuracion de proveedores y despliegue continua disponible en entorno de prueba.
- Permisos para escribir en docs y backend/outputs.

## 1. Preparar entorno de pruebas

1. Activar entorno del backend.
2. Verificar variables de configuracion para orquestacion y publicacion.
3. Confirmar acceso a fuentes de actualidad (API y RSS) o usar fixtures controlados.

## 2. Ejecutar pruebas automatizadas clave

1. Correr la suite de orquestacion y workflow para asegurar baseline verde.
2. Ejecutar pruebas de scraping/seleccion de temas para validar entrada multi-fuente.
3. Ejecutar pruebas de publicacion para verificar escritura consistente en docs.

## 3. Simular ciclos continuos

1. Iniciar ejecucion en modo continuo en entorno controlado.
2. Verificar que se programa un ciclo cada 12 horas (o intervalo reducido de test equivalente).
3. Forzar un fallo transitorio y comprobar reintentos con backoff esperado (5m, 15m, 30m).
4. Verificar que tras fallo individual el sistema no pierde la planificacion global.

## 4. Validar reglas editoriales y operativas

1. Confirmar que los temas publicados son actuales y no duplican contenido reciente (>= 80% en 14 dias).
2. Confirmar que cada intento queda registrado con estado y motivo.
3. Validar que los estados operativos son observables: activo, pausado y degradado.
4. Comprobar que pausar y reanudar conserva la planificacion.

## 4.1 Runbook rapido para estado degraded

1. Revisar `get_operational_status` y comprobar `status=degraded`.
2. Revisar `backend/outputs/continuous_history.json` para identificar `reason_code` dominante.
3. Validar fuentes confiables activas (allowlist) y conectividad de proveedor principal/fallback.
4. Comprobar si existen alertas de `SLI_SUCCESS_RATE_BREACH` o `SLI_CYCLE_LAG_BREACH`.
5. Mitigar causa raiz y ejecutar `resume_continuous_publishing`.
6. Si persiste degradacion critica >24h, mantener `paused` y escalar a revision operativa.

## 4.2 Umbrales de accion

- Success-rate objetivo: >= 95% en ventana movil de 30 dias.
- Lag de ciclo objetivo: <= 90 minutos.
- SLA de alerta: emision en menos de 5 minutos tras breach.
- Pausa automatica por calidad: relevancia semanal < 70% durante 2 semanas consecutivas.

## 5. Validar destino canonico de salida

1. Confirmar que docs/posts.json incorpora las publicaciones nuevas.
2. Confirmar que existen artefactos correspondientes en docs/posts.
3. Verificar que los metadatos de publicacion y trazabilidad quedan consistentes con el historial operativo.

## Resultado esperado

- Operacion continua estable con 2 publicaciones diarias en condicion normal.
- Recuperacion automatica de fallos transitorios sin parada global.
- Trazabilidad completa de ciclos, incidentes y publicaciones.
- Consistencia final de artefactos publicados en docs como superficie canonica.
