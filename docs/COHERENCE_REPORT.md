# Coherence Report — Blogger Agent TFG

> Última revisión: mayo 2026

## Resumen General

- **Proyecto**: Sistema multi-agente para mimetizar estilo de bloggers, con generación de posts y despliegue estático.
- **Stack principal**: Backend Python (orquestador + Daggr), LLMs multi-provider (HuggingFace primario, OpenAI/Gemini/Modal alternativos), web estática HTML + Tailwind CDN en GitHub Pages.
- **Estructura clave**: `backend/aphra_blogger` (llm providers, agentes, workflows), `backend/src/orchestrator` (orquestador 7 fases), `tools/scraper`, `tests/` (~80 tests), `docs/` (web estática), `project_docs/` (documentación técnica).

## Coherencia Resuelta (mayo 2026)

### ✅ Unificado: conteo de tests
- **Valor único**: ~80 tests (79 funciones test en 6 archivos)
- Actualizado en: README.md, backend/README.md, PROJECT_STATUS.md

### ✅ Unificado: número de agentes
- **Orquestador**: 6 agentes principales (StyleAnalyzer, KeywordExtractor, ContentGenerator, Critic, HTMLBuilder, ImageSelector)
- **Pipeline simplificado**: 3 agentes (StyleExtractor, NewsResearchAgent, ContentGenerator)
- **Total en código**: 8 agentes (incluye AnonymousBloggerEmulator y StyleExtractor legacy)
- Actualizado en todos los READMEs

### ✅ Unificado: URLs del repositorio
- **URL canónica**: `https://github.com/AlejandroRS21/blogger-agent-tfg`
- Actualizado en: README.md, pyproject.toml, AGENTS_GUIDE.md, deploy.ps1

### ✅ Resuelto: estado de Modal
- **Estado real**: Código listo (`modal_app.py` + `llm_modal_host.py`), pendiente de pruebas en producción
- Actualizado en: README.md, backend/README.md, PROJECT_STATUS.md

### ✅ Resuelto: estructura de docs
- **`project_docs/`**: Documentación técnica (guías, planes)
- **`docs/`**: Web estática + COHERENCE_REPORT.md
- Todos los enlaces corregidos

### ✅ Resuelto: frontend Next.js
- Eliminado en febrero 2026 (commit `18e9e2a`)
- READMEs actualizados para reflejar web estática HTML + Tailwind CDN
- `FRONTEND_IMPLEMENTATION.md` conservado como referencia histórica

### ✅ Resuelto: archivos de configuración
- `requirements.txt`: eliminado `daggr` duplicado
- `pyproject.toml`: fusionado bloque `dependencies` duplicado
- `.env.example`: completado con todas las variables necesarias
- `deploy.ps1`: eliminado path hardcodeado, ahora detecta root automáticamente

## 🧭 Maintenance Checklist

- [ ] Verificar conteo de tests después de cada release y actualizar docs si cambia
- [ ] Validar que los enlaces a `project_docs/` sigan siendo correctos
- [ ] Confirmar estado de Modal después de pruebas en producción
- [ ] Mantener `.env.example` sincronizado con nuevas variables de entorno
- [ ] Revisar coherencia entre `requirements.txt` y `pyproject.toml` al agregar dependencias
- [ ] Ejecutar `pytest --collect-only -q` para verificar conteo real de tests
- [ ] Actualizar AGENTS_GUIDE.md si cambia el pipeline

---

**Nota**: Este informe se actualiza después de cada revisión de coherencia documental. La última corrección mayor fue en mayo 2026, resolviendo 12+ incoherencias identificadas.
