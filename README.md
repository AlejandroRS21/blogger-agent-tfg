# Blogger Agent TFG (Static Edition)

> Sistema multi-agente de IA para mimetizar estilos de escritura, con generación visual (Daggr) y despliegue estático en GitHub Pages.

## 📋 Descripción del Proyecto

Sistema multi-agente que analiza el estilo de un blogger y genera artículos que mimetizan su tono. Esta versión utiliza un **backend serverless en Modal** con modelos de **HuggingFace** (desplegados en GPUs NVIDIA A10G) para máxima velocidad y privacidad, eliminando cualquier dependencia de OpenAI.

## 🏗️ Arquitectura Actualizada

```
blogger-agent-tfg/
├── backend/                          # Python + Aphra Workflows + HuggingFace
│   ├── aphra_blogger/
│   │   ├── agents/                   # 7 agentes
│   │   │   ├── style_analyzer.py     # Análisis de estilo del blogger
│   │   │   ├── keyword_extractor.py  # Extracción de keywords
│   │   │   ├── content_generator.py  # Generación de contenido
│   │   │   ├── critic.py             # Crítica y feedback
│   │   │   ├── image_selector.py     # Descripciones de imágenes
│   │   │   ├── html_builder.py       # Construcción HTML/JSX
│   │   │   └── research_agent.py     # Investigación sobre el tema
│   │   ├── llm/                      # Abstracción multi-provider LLM
│   │   │   ├── base.py               # Clases abstractas
│   │   │   ├── factory.py            # Factory con auto-fallback
│   │   │   ├── huggingface_provider.py  # HuggingFace (primario, gratis)
│   │   │   ├── openai_provider.py       # OpenAI (fallback opcional)
│   │   │   ├── gemini_provider.py       # Google Gemini
│   │   │   └── modal_provider.py        # Modal serverless
│   │   ├── workflows/
│   │   │   └── blogger_style.py
│   │   ├── config/
│   │   │   └── default.toml
│   │   └── context.py
│   ├── src/orchestrator/             # Sistema de orquestación completo
│   │   ├── main.py                   # 7 fases con todos los agentes
│   │   ├── config.py
│   │   ├── state.py
│   │   ├── runner.py
│   │   ├── continuous/               # Módulo de publicación continua
│   │   │   ├── scheduler.py
│   │   │   ├── topic_selector.py
│   │   │   ├── source_guard.py
│   │   │   ├── monitoring.py
│   │   │   ├── alerts.py
│   │   │   ├── history_store.py
│   │   │   ├── incident_manager.py
│   │   │   ├── retry_policy.py
│   │   │   └── validation.py
│   │   └── README.md
│   ├── tools/
│   │   └── scraper.py                # Web scraper WordPress-optimizado
│   ├── tests/                        # 10 archivos de test (~75 tests passing)
│   │   ├── test_agents.py
│   │   ├── test_orchestrator.py
│   │   ├── test_orchestrator_config.py
│   │   ├── test_workflow.py
│   │   ├── test_scraper.py
│   │   ├── test_html_builder.py
│   │   ├── test_batch_generate.py
│   │   ├── test_structural_diversity.py
│   │   ├── conftest.py
│   │   └── __init__.py
│   ├── daggr_blogger_workflow.py     # Workflow visual con Daggr
│   ├── modal_app.py                  # App para Modal serverless
│   ├── outputs/                      # Posts generados (JSON)
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/                         # Next.js 16 + React 19 + Tailwind CSS 4
│   ├── app/
│   │   ├── components/
│   │   │   ├── HTMLRenderer.tsx      # Renderizado HTML sanitizado
│   │   │   ├── PostCard.tsx          # Tarjeta de post en homepage
│   │   │   └── PostMeta.tsx          # Metadatos del post
│   │   ├── posts/[slug]/
│   │   │   └── page.tsx              # Página de post individual
│   │   ├── lib/
│   │   │   ├── api.ts                # Lectura de posts desde docs/
│   │   │   └── postAudit.ts          # Auditoría de calidad de posts
│   │   ├── types/
│   │   │   └── post.ts               # Schemas Zod + tipos TypeScript
│   │   ├── layout.tsx                # Root layout
│   │   ├── page.tsx                  # Homepage con grid de PostCards
│   │   └── not-found.tsx             # Página 404
│   ├── __tests__/                    # 5 archivos de test (Jest + Testing Library)
│   │   ├── api.test.ts
│   │   ├── HTMLRenderer.test.tsx
│   │   ├── integrity.test.ts
│   │   ├── PostCard.test.tsx
│   │   └── seo.test.ts
│   ├── package.json                  # next 16.1.6, react 19.2.3, tailwindcss ^4
│   ├── next.config.ts                # Static export (output: 'export')
│   └── jest.config.ts
├── docs/                             # Documentación técnica
│   ├── ORCHESTRATION_PLAN.md         # Plan maestro de orquestación
│   ├── NEXT_STEPS.md                 # Roadmap detallado
│   ├── MODAL_DEPLOYMENT.md           # Guía de deployment Modal
│   ├── VERCEL_DEPLOYMENT.md          # Guía de deployment Vercel
│   ├── HUGGINGFACE_MIGRATION.md      # Migración a HuggingFace
│   ├── FRONTEND_IMPLEMENTATION.md    # Implementación frontend
│   ├── HTMLBUILDER_INTEGRATION.md    # Integración HTMLBuilder
│   ├── SCRAPER_IMPLEMENTATION.md     # Implementación del scraper
│   ├── ENVIRONMENT_VARIABLES.md      # Variables de entorno
│   ├── GRADIO_INTERFACE.md           # Interfaz Gradio para testing
│   ├── COHERENCE_REPORT.md           # Reporte de coherencia
│   └── RESUMEN_TRABAJO_COMPLETADO.md # Resumen del TFG
├── specs/                            # 9 specs con SDD artifacts
├── project_docs/                     # (deprecado — contenido migrado a docs/)
├── vercel.json
└── README.md
```

## 🏛️ Next.js como Motor del Blog

**IMPORTANTE**: Este proyecto **NO usa WordPress**. El blog completo está construido con **Next.js 16** usando App Router y estática generada.

### Arquitectura del Blog

```
Backend (Workflow Agentes)          Frontend (Next.js Blog — Static Export)
┌──────────────────────────┐       ┌────────────────────────────────┐
│ Workflow Aphra + LLMs    │       │ Next.js 16 (App Router)       │
│ + Modal Serverless       │  -->  │ + Static Generation           │
│                          │       │ + SEO Metadata API            │
│ Genera JSON + HTML       │       │ + Componentes React           │
│ → docs/posts/            │       │ + Tailwind CSS 4              │
│ → docs/posts.json        │       │ + DOM Purify sanitization     │
└──────────────────────────┘       └────────────────────────────────┘
```

### Flujo de Generación y Publicación

1. **Workflow ejecuta agentes** en backend Python
2. **Genera JSON estructurado** y HTML para cada post
3. **Guarda el resultado** en `docs/posts/{slug}.json` y `docs/posts.json`
4. **Next.js lee desde el filesystem** en build time (`lib/api.ts`)
5. **Renderiza el post** en `/posts/[slug]` con Server Components
6. **Static Export** genera HTML estático para deploy en GitHub Pages/Vercel

### Estructura Frontend

```
frontend/
└── app/
    ├── page.tsx                  # Homepage: grid de PostCards
    ├── posts/[slug]/page.tsx     # Post individual: HTMLRenderer + PostMeta
    ├── components/
    │   ├── HTMLRenderer.tsx      # Renderizado HTML sanitizado con DOM Purify
    │   ├── PostCard.tsx          # Tarjeta de resumen (grid homepage)
    │   └── PostMeta.tsx          # Metadatos (tags, tiempo lectura, etc.)
    └── lib/
        ├── api.ts                # Lee posts desde docs/posts.json y docs/posts/
        └── postAudit.ts          # Auditoría de calidad de posts generados
```

### Componentes Principales

- **`<PostCard>`**: Tarjeta de resumen usada en el grid de la homepage (slug, título, fecha, extracto)
- **`<HTMLRenderer>`**: Renderizado de HTML con sanitización mediante `isomorphic-dompurify`
- **`<PostMeta>`**: Visualización de metadatos del post (tags, tiempo de lectura, etc.)

## 👥 División de Tareas (3 Personas)

### 👤 Persona 1: Backend Lead + Workflows Core
**Responsabilidades:**
- Estructura base del `BloggerStyleWorkflow`
- Agentes principales:
  - `style_analyzer.py` — Análisis del estilo del blogger
  - `content_generator.py` — Redacción base + refinada
  - `critic.py` — Crítica y feedback
- Configuración de `config/default.toml`
- Tests unitarios backend
- Docker setup para backend

**Branches:**
- `feature/workflow-base`
- `feature/style-analyzer`
- `feature/content-generator`
- `feature/critic-agent`

### 👤 Persona 2: Backend Specialization + Integration
**Responsabilidades:**
- Agentes especializados:
  - `keyword_extractor.py` — Palabras clave y términos
  - `html_builder.py` — Construcción JSON/HTML
  - `image_selector.py` — Descripciones de imágenes
  - `research_agent.py` — Investigación sobre el tema
- Prompts tuneados en cada agente
- `runner.py` — CLI para ejecutar workflows
- Tests de integración
- Documentación técnica
- **Integración con Modal** para deployment serverless
- **Integración con Vercel** para deployment del frontend Next.js

**Branches:**
- `feature/keyword-extractor`
- `feature/html-builder`
- `feature/image-selector`
- `feature/research-agent`
- `feature/runner-cli`
- `feature/modal-deployment`
- `docs/architecture`

### 👤 Persona 3: Frontend Full Stack + DevOps
**Responsabilidades:**
- Frontend completo Next.js:
  - Componentes React (`<PostCard>`, `<HTMLRenderer>`, `<PostMeta>`)
  - Página dinámica `app/posts/[slug]/page.tsx`
  - Homepage con grid de PostCards
  - Estilos y UX (Tailwind CSS 4)
- DevOps:
  - GitHub Actions CI/CD
  - **Vercel deployment** para frontend estático
- Testing frontend (Jest + Testing Library)
- Documentación frontend

**Branches:**
- `feature/post-components`
- `feature/post-page`
- `feature/homepage`
- `feature/vercel-deployment`
- `feature/ci-cd`
- `feature/frontend-tests`

## 🚀 Quick Start (Estado Actual)

### Backend — Sistema Completo con HuggingFace ✅

```bash
# 1. Clonar repositorio
git clone https://github.com/IES-Rafael-Alberti/blogger-agent-tfg.git
cd blogger-agent-tfg/backend

# 2. Setup automatizado con UV (10-100x más rápido que pip) ⚡
./setup.sh   # Linux/macOS
# o
.\setup.ps1  # Windows

# 3. Configurar API token (gratis) 🆓
export HF_TOKEN="your_huggingface_token"
# Obtén tu token gratis en: https://huggingface.co/settings/tokens

# Alternativa: OpenAI como fallback
export OPENAI_API_KEY="sk-..."

# 4. Activar entorno
source .venv/bin/activate    # Linux/macOS
# o
.venv\Scripts\Activate.ps1  # Windows

# 5. Ejecutar orquestador completo (7 fases) con HuggingFace
python -m src.orchestrator.runner \
  --topic "Las mejores prácticas para desarrollar APIs REST con Python" \
  --blog-url "https://javipas.com" \
  --output "post.json"

# 6. Ver resultados
cat post.json
```

**✨ Novedad: Migración a HuggingFace**
- 🆓 **Gratis**: HuggingFace Inference API sin coste
- 🚀 **Rápido**: Modelos Llama 3.1 y Mistral optimizados
- 🔄 **Fallback**: OpenAI, Gemini y Modal como respaldos
- 📖 [Guía completa de migración](docs/HUGGINGFACE_MIGRATION.md)

### Frontend — Next.js con Static Export ✅

```bash
# 1. Ir al directorio frontend
cd frontend

# 2. Instalar dependencias
npm install

# 3. Iniciar servidor de desarrollo
npm run dev

# 4. Abrir en navegador
# http://localhost:3000
```

**✨ Frontend:**
- 🎨 **3 Componentes**: PostCard, HTMLRenderer, PostMeta
- 📄 **2 Páginas**: Homepage (grid de PostCards), Posts dinámicos
- 🧪 **Tests**: 5 archivos con Jest + Testing Library
- 📱 **Responsive**: Tailwind CSS 4 + diseño mobile-first
- 📖 [Documentación frontend](frontend/README.md)

### Generación y Testing con Daggr (Recomendado) 🎨

```bash
# Interfaz visual para generar y debuggear posts
cd backend
python daggr_blogger_workflow.py

# Abrir http://localhost:7860
```

**✨ Features Daggr:**
- 📊 **Visualización de Workflow**: Canvas interactivo con 6 agentes conectados
- 🔍 **Inspección por Nodo**: Ver input/output de cada agente
- 🔄 **Re-ejecución Selectiva**: Ejecutar solo el nodo que necesites
- ⏱️ **Debugging Visual**: Identifica problemas en cada paso
- 💾 **Persistencia**: Estado guardado entre sesiones
- 🧪 **Testing Manual**: Prueba diferentes estilos y temas

### Tests

```bash
# Backend (10 archivos, ~75 tests)
cd backend
pytest tests/ -v

# Tests del orquestador
pytest tests/test_orchestrator.py -v

# Tests de agentes
pytest tests/test_agents.py -v

# Tests del HTMLBuilder
pytest tests/test_html_builder.py -v

# Tests del scraper
pytest tests/test_scraper.py -v

# Frontend (5 archivos, Jest + Testing Library)
cd frontend
npm test
```

**Resultado:** JSON completo con:
- ✅ Análisis de estilo del blogger
- ✅ Keywords extraídas
- ✅ Contenido generado en Markdown
- ✅ Feedback de crítica
- ✅ Estructura HTML/JSX optimizada
  - HTML sanitizado
  - JSX para React/Next.js
  - Meta tags SEO (title, description, keywords)
  - Tabla de contenidos (headings)
  - Tiempo de lectura y conteo de palabras
- ✅ Prompts de imágenes con ubicaciones

## 🚀 Integración con Modal

**Modal** se usa para deployment serverless del backend Python. La implementación está lista en `backend/modal_app.py`.

### Implementación

```python
# backend/modal_app.py
import modal
from src.orchestrator.main import BloggerOrchestrator

stub = modal.Stub("blogger-agent")
image = modal.Image.debian_slim().pip_install_from_requirements("requirements.txt")

@stub.function(image=image, secrets=[modal.Secret.from_name("hf-secret")])
def generate_blog_post(blogger_urls: list[str], topic: str) -> dict:
    orchestrator = BloggerOrchestrator()
    result = orchestrator.run(blogger_urls=blogger_urls, topic=topic)
    return result

@stub.webhook(method="POST")
def webhook(data: dict):
    result = generate_blog_post.call(
        blogger_urls=data["blogger_urls"],
        topic=data["topic"]
    )
    return result
```

### Deploy

```bash
modal deploy backend/modal_app.py
```

📖 [Guía completa de deployment Modal](docs/MODAL_DEPLOYMENT.md)

## 🔧 Setup Rápido

### Backend (Orquestador)

**Usando uv** (recomendado — 10-100x más rápido) ⚡:
```bash
cd backend

# Instalar uv si no lo tienes
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux

# Crear entorno e instalar dependencias
uv venv
uv pip install -r requirements.txt

# Activar entorno
source .venv/bin/activate  # Linux/macOS

# Ejecutar orquestador
python -m src.orchestrator.runner \
  --topic "AI en educación" \
  --blog-url "https://javipas.com" \
  --output "output.json"
```

**Usando pip tradicional** (alternativa):
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Docker
```bash
docker-compose up
```

### Modal Deployment (Backend)
```bash
modal deploy backend/modal_app.py
```

### Vercel Deployment (Frontend)
```bash
cd frontend
vercel deploy --prod
```

O conecta tu repositorio de GitHub con Vercel para deployment automático.

## 📊 Flujo de Trabajo (Workflow)

**Pipeline completo con 7 fases orquestadas:**

1. **Análisis de Estilo** (`style_analyzer`) → Analiza posts del blogger
2. **Extracción de Keywords** (`keyword_extractor`) → Palabras clave recurrentes
3. **Generación de Contenido** (`content_generator`) → Genera contenido con estilo del blogger
4. **Crítica** (`critic`) → Feedback sobre coherencia y estilo
5. **Refinamiento** (`content_generator`) → Mejora contenido basado en crítica (si necesario)
6. **Construcción HTML** (`html_builder`) → Convierte Markdown a HTML/JSX optimizado
   - Convierte Markdown a HTML usando `python-markdown`
   - Genera JSX para componentes React/Next.js
   - Extrae headings para tabla de contenidos (TOC)
   - Genera meta tags (title, description, keywords)
   - Calcula tiempo de lectura y conteo de palabras
7. **Selección de Imágenes** (`image_selector`) → Prompts y ubicaciones para imágenes
8. _Investigación_ (`research_agent`) → Investigación adicional del tema (integrado en fases previas)

## 📊 Estado del Proyecto

### ✅ Completado (Backend)
- **LLM Abstraction**: Multi-provider con HuggingFace (gratis), OpenAI, Gemini y Modal
- **7 Agentes**: StyleAnalyzer, KeywordExtractor, ContentGenerator, Critic, ImageSelector, HTMLBuilder, ResearchAgent
- **Orquestador**: 7 fases completas con integración de todos los agentes
- **Módulo Continuo**: scheduler, topic_selector, source_guard, monitoring, alerts, history_store, incident_manager
- **Scraper**: WordPress-optimizado para blogs (javipas.com compatible)
- **Tests**: 10 archivos de test (~75 passing)
- **Modal**: `modal_app.py` listo para deploy serverless
- **Documentación**: 12 guías completas en `docs/`

### ✅ Completado (Frontend)
- **Next.js 16**: React 19 + TypeScript 5 + Tailwind CSS 4
- **3 Componentes**: PostCard, HTMLRenderer, PostMeta
- **2 Páginas**: Homepage (grid PostCard), Posts dinámicos (`/posts/[slug]`)
- **Tests Frontend**: 5 archivos con Jest + Testing Library
- **Static Export**: `output: 'export'` para deploy sin servidor
- **Configuración**: next.config.ts con reactCompiler

### ⏳ Pendiente
- **Integración E2E**: Backend Python + Frontend Next.js (automatización)
- **CI/CD**: GitHub Actions completo para testing y deployment
- **GitHub Pages**: Configurar deploy automático del static export

## 🤝 Contribuir

Lee [CONTRIBUTING.md](CONTRIBUTING.md) para entender el flujo de trabajo con Git y GitHub.

### Flujo Git
1. Crear issue desde GitHub Projects
2. Asignarte la issue
3. Crear rama: `git checkout -b feature/nombre`
4. Commits: `git commit -m "feat(scope): description"`
5. Push y PR contra `develop`
6. Esperar 1 approval
7. Merge

## 📚 Documentación

- [Plan de Orquestación](docs/ORCHESTRATION_PLAN.md) — Plan completo de desarrollo ⭐
- [Próximos Pasos](docs/NEXT_STEPS.md) — Roadmap y tareas pendientes 📋
- [Modal Deployment](docs/MODAL_DEPLOYMENT.md) — Guía de deployment backend
- [Vercel Deployment](docs/VERCEL_DEPLOYMENT.md) — Guía de deployment frontend
- [HuggingFace Migration](docs/HUGGINGFACE_MIGRATION.md) — Migración a HF
- [Frontend Implementation](docs/FRONTEND_IMPLEMENTATION.md) — Guía frontend
- [HTMLBuilder Integration](docs/HTMLBUILDER_INTEGRATION.md) — Integración HTMLBuilder
- [Scraper Implementation](docs/SCRAPER_IMPLEMENTATION.md) — Guía del scraper
- [Environment Variables](docs/ENVIRONMENT_VARIABLES.md) — Variables de entorno
- [Gradio Interface](docs/GRADIO_INTERFACE.md) — Interfaz Gradio para testing
- [Coherence Report](docs/COHERENCE_REPORT.md) — Reporte de coherencia
- [Orchestrator README](backend/src/orchestrator/README.md) — Documentación del orquestador

## 🧪 Testing

```bash
# Backend (10 archivos, ~75 tests)
cd backend
pytest tests/

# Frontend (5 archivos, Jest + Testing Library)
cd frontend
npm test
```

## 📦 Tech Stack

### Backend
- Python 3.11+
- Aphra (workflow framework)
- **HuggingFace Inference API** — LLM primario (gratis) ✅
- OpenAI API — Fallback opcional
- Google Gemini API — Fallback opcional
- Modal — Serverless deployment (listo)
- **Daggr 0.7.0** — Workflow visual y debugging ✅
- **python-markdown** — Conversión Markdown → HTML
- **Pygments** — Syntax highlighting para código
- **beautifulsoup4** — Web scraping
- **lxml** — Parser HTML rápido
- pytest (10 archivos, ~75 tests)

### Frontend
- Next.js 16.1.6 (App Router) ✅
- React 19.2.3 ✅
- TypeScript 5 ✅
- Tailwind CSS 4 ✅
- Zod 4 — Validación de schemas
- DOM Purify — Sanitización de HTML
- Jest 30 + Testing Library (5 archivos) ✅

### Testing & Debugging
- **Daggr** — Visualización workflow, inspección nodos, re-ejecución ✅
- pytest — Tests unitarios e integración backend
- Jest + Testing Library — Tests frontend ✅

### DevOps
- Docker
- GitHub Actions
- Modal (backend serverless)
- Vercel (frontend deployment)

## 📝 Licencia

MIT License — Ver [LICENSE](LICENSE) para detalles.

## 👨‍🎓 Proyecto Académico

Trabajo Final de Grado (TFG) — Especialización en IA y Big Data
IES Rafael Alberti — 2026
