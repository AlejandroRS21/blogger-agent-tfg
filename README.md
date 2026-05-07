# Blogger Agent TFG

> Sistema multi-agente de IA para mimetizar estilos de escritura, con generación visual (Daggr) y despliegue estático en GitHub Pages.

## 🌐 Despliegue Automatizado (GitHub Pages)

El blog se actualiza en `https://AlejandroRS21.github.io/blogger-agent-tfg/` mediante un botón **🌐 DESPLEGAR BLOG** o ejecutando el script de deploy.

### ¿Cómo funciona el despliegue?

1.  **Generación Local/Modal**: El sistema genera los posts y los guarda en `docs/posts/`.
2.  **Sincronización Automática**: Al desplegar, se ejecuta `deploy.ps1`.
3.  **Git Subtree**: El script usa `git subtree push --prefix docs origin gh-pages` para enviar **únicamente** `docs/` a la rama de producción sin interferir con `main`.

> [!NOTE]
> Necesitás permisos de escritura en el repositorio y Git configurado localmente.

---

## 📋 Descripción del Proyecto

Sistema multi-agente que analiza el estilo de un blogger y genera artículos que mimetizan su tono. El backend usa **HuggingFace** como LLM primario (gratis), **Modal** para deployment serverless con GPU y **Daggr** para visualización interactiva del workflow. Frontend en **Next.js 16** con React 19, TypeScript y Tailwind CSS 4. Web estática complementaria en GitHub Pages.

## 🏗️ Arquitectura

```
blogger-agent-tfg/
├── backend/                         # Python + Orquestador + Daggr
│   ├── aphra_blogger/
│   │   ├── llm/                     # Abstracción multi-provider LLM
│   │   │   ├── base.py              # Clases abstractas
│   │   │   ├── factory.py           # Factory con auto-fallback
│   │   │   ├── huggingface_provider.py  # HuggingFace (primario, gratis)
│   │   │   ├── openai_provider.py       # OpenAI (fallback)
│   │   │   ├── gemini_provider.py       # Gemini (alternativo)
│   │   │   └── modal_provider.py        # Modal con GPU (producción)
│   │   ├── agents/                  # Agentes especializados
│   │   │   ├── style_analyzer.py        # Análisis de estilo
│   │   │   ├── keyword_extractor.py     # Extracción de keywords
│   │   │   ├── content_generator.py     # Generación y refinamiento
│   │   │   ├── critic.py                # Crítica y evaluación
│   │   │   ├── image_selector.py        # Selección de imágenes
│   │   │   ├── html_builder.py          # Markdown → HTML/JSX
│   │   │   ├── anonymous_blogger.py     # Emulación de blogueros anónimos
│   │   │   └── style_extractor.py       # Extracción legacy de estilo
│   │   ├── workflows/
│   │   │   └── blogger_style.py
│   │   ├── config/
│   │   │   └── default.toml
│   │   └── context.py
│   ├── src/
│   │   └── orchestrator/            # Sistema de orquestación
│   │       ├── main.py              # Orquestador (7 fases)
│   │       ├── config.py
│   │       ├── state.py
│   │       └── runner.py            # CLI
│   ├── tools/
│   │   └── scraper.py               # Web scraper WordPress
│   ├── tests/                       # ~80 tests
│   │   ├── test_agents.py
│   │   ├── test_orchestrator.py
│   │   ├── test_html_builder.py
│   │   ├── test_scraper.py
│   │   ├── test_workflow.py
│   │   └── test_anonymous_blogger.py
│   ├── daggr_blogger_workflow.py    # Workflow visual con Daggr
│   ├── modal_app.py                 # Deployment Modal (serverless)
│   ├── llm_modal_host.py            # Hosting LLM propio en Modal GPU
│   ├── generate_and_deploy.py       # Pipeline simplificado
│   ├── outputs/                     # Posts generados (JSON)
│   ├── requirements.txt
│   ├── pyproject.toml
│   ├── DAGGR_WORKFLOW.md
│   └── setup.sh / setup.ps1
├── frontend/                         # Next.js 16 + React 19 + Tailwind 4
│   ├── app/
│   │   ├── layout.tsx                # Root layout
│   │   ├── page.tsx                  # Homepage
│   │   ├── globals.css
│   │   ├── generate/page.tsx         # Formulario de generación
│   │   ├── posts/[slug]/page.tsx     # Vista de post individual
│   │   └── api/generate-post/route.ts # API endpoint (mock/real)
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   ├── GenerateForm.tsx          # Client component
│   │   ├── PostCard.tsx
│   │   └── PostContent.tsx
│   ├── types/post.ts
│   ├── lib/api.ts
│   ├── package.json
│   └── README.md
├── docs/                            # Web Estática (GitHub Pages)
│   ├── posts/                       # Posts HTML generados
│   ├── index.html                   # Homepage (Tailwind CDN)
│   ├── posts.json                   # Metadatos del blog
│   └── COHERENCE_REPORT.md          # Informe de coherencia
├── project_docs/                    # Documentación técnica
│   ├── ORCHESTRATION_PLAN.md
│   ├── MODAL_DEPLOYMENT.md
│   ├── HUGGINGFACE_MIGRATION.md
│   ├── FRONTEND_IMPLEMENTATION.md   # Histórico: frontend eliminado
│   └── ...
├── deploy.ps1                       # Script de despliegue a GH Pages
└── LICENSE                          # MIT
```

## 🚀 Quick Start

### Backend — Orquestador Completo

```bash
# 1. Clonar repositorio
git clone https://github.com/AlejandroRS21/blogger-agent-tfg.git
cd blogger-agent-tfg/backend

# 2. Setup automatizado con UV ⚡
./setup.sh   # Linux/macOS
# o
.\setup.ps1  # Windows

# 3. Configurar API token (gratis) 🆓
export HF_TOKEN="hf_..."           # HuggingFace (primario, gratis)
# Alternativas:
export GEMINI_API_KEY="..."        # Gemini (gratis con límites)
export OPENAI_API_KEY="sk-..."     # OpenAI (pago, fallback)

# 4. Ejecutar orquestador (7 fases)
python -m src.orchestrator.runner \
  --topic "Las mejores prácticas para desarrollar APIs REST con Python" \
  --blog-url "https://javipas.com" \
  --output "post.json"
```

### Interfaz Visual con Daggr (Recomendado) 🎨

```bash
cd backend
python daggr_blogger_workflow.py
# Abrir http://localhost:7860
```

**Features Daggr:**
- 📊 **Visualización de Workflow**: Canvas interactivo con agentes conectados
- 🔍 **Inspección por Nodo**: Ver input/output de cada agente
- 🔄 **Re-ejecución Selectiva**: Ejecutar solo el nodo necesario
- ⏱️ **Debugging Visual**: Identificar problemas en cada paso
- 💾 **Persistencia**: Estado guardado entre sesiones

### Pipeline Simplificado

```bash
cd backend
python generate_and_deploy.py "El futuro de la IA en 2026"
```

### Frontend — Next.js 16 ⚛️

```bash
cd frontend
npm install
npm run dev
# Abrir http://localhost:3000
```

**Modo Mock** (default): Funciona sin backend, genera datos de ejemplo.
**Modo Real**: Configurar `USE_MOCK=false` y `BACKEND_URL` en `frontend/.env.local`.

#### Deploy a Vercel 🚀

1. Importar el repo en [vercel.com](https://vercel.com)
2. **Root Directory**: `frontend`
3. **Environment Variables**: `USE_MOCK=true` (o `false` con `BACKEND_URL` si tenés Modal)
4. Deploy — Vercel autodetecta Next.js

```bash
# O por CLI
cd frontend && npx vercel --prod
```

### Previsualizar Web Estática

```bash
cd docs
python -m http.server 8000
# Abrir http://localhost:8000
```

### Tests

```bash
cd backend
# Ejecutar todos los tests (~80 tests)
pytest tests/ -v

# Tests específicos
pytest tests/test_orchestrator.py -v
pytest tests/test_html_builder.py -v
pytest tests/test_agents.py -v

# Test end-to-end
python test_full_pipeline.py
```

## 📊 Flujo de Trabajo (7 Fases)

1. **Análisis de Estilo** (`style_analyzer`) → Analiza posts del blogger
2. **Extracción de Keywords** (`keyword_extractor`) → Palabras clave recurrentes
3. **Generación de Contenido** (`content_generator`) → Borrador con estilo del blogger
4. **Crítica** (`critic`) → Feedback sobre coherencia y estilo (score 0-10)
5. **Refinamiento** (`content_generator`) → Mejora basada en crítica (si score < 7)
6. **Construcción HTML** (`html_builder`) → Convierte Markdown a HTML/JSX optimizado
   - HTML semántico con meta tags SEO
   - JSX para React/Next.js
   - Tabla de contenidos (TOC)
   - Tiempo de lectura y conteo de palabras
7. **Selección de Imágenes** (`image_selector`) → Prompts y ubicaciones para imágenes

## 🚀 Integración con Modal

**Modal** se usa para deployment serverless con GPU:

- **`modal_app.py`**: Despliega el orquestador como webhook serverless
- **`llm_modal_host.py`**: Hostea Qwen 2.5 7B en GPU A10G para inferencia propia

```bash
# Desplegar orquestador serverless
modal deploy backend/modal_app.py

# Desplegar LLM propio con GPU
modal deploy backend/llm_modal_host.py
```

## 📊 Estado del Proyecto

### ✅ Completado
- **LLM Abstraction**: Multi-provider (HuggingFace, OpenAI, Gemini, Modal GPU)
- **7 Agentes**: StyleAnalyzer, KeywordExtractor, ContentGenerator, Critic, ImageSelector, HTMLBuilder, AnonymousBloggerEmulator
- **Orquestador**: 7 fases completas con retry, logging y state management
- **Scraper**: WordPress-optimizado (javipas.com compatible)
- **Tests**: ~80 tests
- **Daggr**: Workflow visual interactivo con Gradio
- **Frontend Next.js**: App Router, React 19, TypeScript, Tailwind 4
- **Web Estática**: HTML5 + Tailwind CDN, GitHub Pages
- **Modal**: Deployment serverless preparado (`modal_app.py` + `llm_modal_host.py`)

### ⏳ Pendiente
- **CI/CD**: GitHub Actions para testing y deployment automático
- **Tests E2E**: Cypress/Playwright para validación de la web estática
- **Testing en Modal**: Probar el deployment real en producción

## 📚 Documentación

- [Plan de Orquestación](project_docs/ORCHESTRATION_PLAN.md) — Plan completo de desarrollo ⭐
- [Próximos Pasos](project_docs/NEXT_STEPS.md) — Roadmap y tareas pendientes 📋
- [Modal Deployment](project_docs/MODAL_DEPLOYMENT.md) — Guía de deployment backend
- [HuggingFace Migration](project_docs/HUGGINGFACE_MIGRATION.md) — Migración a HF ✅
- [HTMLBuilder Integration](project_docs/HTMLBUILDER_INTEGRATION.md) — HTMLBuilder
- [Frontend Implementation](project_docs/FRONTEND_IMPLEMENTATION.md) — Histórico Next.js (eliminado)
- [Frontend README](frontend/README.md) — Documentación del frontend Next.js ⚛️
- [Daggr Workflow](backend/DAGGR_WORKFLOW.md) — Guía completa de Daggr ✅
- [Agents Guide](backend/AGENTS_GUIDE.md) — Guía para agentes IA
- [Coherence Report](docs/COHERENCE_REPORT.md) — Informe de coherencia documental
- [Resumen de Trabajo](project_docs/RESUMEN_TRABAJO_COMPLETADO.md) — Historial de issues

## 📦 Tech Stack

### Backend
- Python 3.11+
- **HuggingFace Inference API** — LLM primario (gratis) ✅
- OpenAI API — Fallback opcional
- Google Gemini — Alternativa gratuita
- **Modal** — Deployment serverless con GPU (A10G)
- **Daggr + Gradio** — Workflow visual interactivo ✅
- **python-markdown + Pygments** — Conversión Markdown → HTML
- **beautifulsoup4 + lxml** — Web scraping
- pytest — ~80 tests

### Frontend
- **Next.js 16.1** (App Router) ✅
- **React 19** ✅
- **TypeScript 5** ✅
- **Tailwind CSS 4** ✅
- Modo mock para desarrollo sin backend

### Web Estática (complementaria)
- HTML5 semántico
- Tailwind CSS (via CDN)
- GitHub Pages

### DevOps
- Docker + Docker Compose
- Modal (backend serverless con GPU)
- GitHub Pages (web estática)
- Vercel (frontend Next.js)

## 🧭 Coherencia Documental

Este README refleja el estado real del proyecto a mayo 2026. Para verificar la consistencia entre ramas, consultá [COHERENCE_REPORT.md](docs/COHERENCE_REPORT.md).

> **Nota**: El frontend Next.js original fue eliminado en febrero 2026. En mayo 2026 se reconstruyó con Next.js 16, React 19 y Tailwind 4. La documentación del frontend anterior se conserva en `project_docs/FRONTEND_IMPLEMENTATION.md`.

## 📝 Licencia

MIT License — Ver [LICENSE](LICENSE) para detalles.

## 👨‍🎓 Proyecto Académico

Trabajo Final de Grado (TFG) — Especialización en IA y Big Data  
IES Rafael Alberti — 2026
