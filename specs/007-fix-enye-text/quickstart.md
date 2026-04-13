# Quickstart: Validación de preservación de `ñ`

Esta guía verifica que los artículos nuevos mantienen `ñ` durante generación y publicación.

## Prerrequisitos

- Entorno Python del backend activo.
- Dependencias instaladas para ejecutar el pipeline y tests.
- Frontend configurado para leer contenido desde `docs/`.

## Reproducción del caso

1. Generar contenido con términos que incluyan `ñ` en varias posiciones (título, excerpt, cuerpo):

```bash
cd backend
.venv/bin/python -m src.orchestrator.runner \
  --topic "Tecnología para niños en España" \
  --blog-url "https://javipas.com" \
  --provider gemini \
  --output outputs/test_enye_article.json
```

2. Verificar que la salida contiene `ñ` en campos visibles:

```bash
rg "ñ|España|niños|año" backend/outputs/test_enye_article.json
```

3. Publicar/actualizar catálogo en `docs/` y comprobar artefactos:

```bash
rg "ñ|España|niños|año" docs/posts.json docs/posts/*.json
```

## Validación rápida automatizada

```bash
cd backend
.venv/bin/pytest tests/test_orchestrator.py tests/test_agents.py tests/test_html_builder.py -q
```

## Resultado esperado

- El contenido publicado conserva `ñ` en todos los campos visibles (`title`, `excerpt`, `content`).
- No hay sustituciones de `ñ` por `n` en snapshots validados.
- Los artículos sin `ñ` no presentan regresiones de formato.

## Nota de alcance histórico

- Esta feature corrige obligatoriamente contenido nuevo.
- Artículos históricos degradados se corrigen bajo demanda mediante regeneración/corrección manual.
