# Guía Rápida: Generación de Contenido Diversificado (Anti-Plantilla)

Esta guía explica cómo ejecutar la nueva generación de posts que evita estructuras fijas y mimetiza la espontaneidad del blog objetivo.

## 01. Generar Post con Diversidad Estructural (Simulado)

Para generar un post que use el nuevo motor de diversidad:

```bash
# Ejecución del pipeline con inyección de modo estructural
python backend/generate_and_deploy.py \
  --topic "El futuro de los procesadores RISC-V" \
  --mode "TECHNICAL" \
  --random-signature
```

## 02. Parámetros de Control Clave

*   `--mode`: `REFLECTIVE` (Ensayo largo), `TECHNICAL` (Specs + Crítica), `QUICK_FLASH` (Opinión corta).
*   `--random-signature`: Si se activa, el agente elegirá una "firma" de estilo aleatoria del corpus de Javipas.

## 03. Verificación de "Salud Estructural"

El sistema ahora falla (error de validación) si:
1.  El post tiene exactamente 3 subtítulos H2 equidistantes.
2.  Todos los párrafos superan los 500 caracteres (falta de ritmo).
3.  No hay nigún elemento de énfasis (negritas, cursivas, listas o blockquotes).

## 04. Desarrollo Local

1.  Ajusta el prompt en `backend/aphra_blogger/agents/content_generator.py`.
2.  Ejecuta los tests de validación estructural:
    ```bash
    pytest backend/tests/test_structural_diversity.py
    ```

