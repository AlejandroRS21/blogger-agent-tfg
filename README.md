# Blogger Agent TFG

> Multi-agent AI system for mimicking blogger writing style using Aphra workflows, Next.js on Vercel, and Modal backend deployment

## 📋 Descripción del Proyecto

Sistema multi-agente de IA que analiza el estilo de escritura de un blogger y genera artículos nuevos que mimetizan su tono, estructura, y forma de escribir. El proyecto utiliza múltiples agentes especializados que colaboran para:

- Analizar el estilo narrativo del blogger
- Extraer palabras clave y patrones lingüísticos
- Generar contenido base
- Criticar y refinar el texto
- Construir HTML/JSX optimizado para Next.js
- Seleccionar y ubicar imágenes apropiadas

## 🏗️ Arquitectura

```
blogger-agent-tfg/
├── backend/                    # Python + Aphra Workflows + HuggingFace
│   ├── aphra_blogger/
│   │   ├── llm/                # ✅ NUEVO: Abstracción multi-provider LLM
│   │   │   ├── base.py         # Clases abstractas
│   │   │   ├── factory.py      # Factory con auto-fallback
│   │   │   ├── huggingface_provider.py  # HuggingFace (primario, gratis)
│   │   │   └── openai_provider.py       # OpenAI (fallback opcional)
│   │   ├── agents/             # ✅ Todos los agentes migrados a HF
│   │   │   ├── style_analyzer.py       # → HuggingFace/OpenAI
│   │   │   ├── keyword_extractor.py    # → HuggingFace/OpenAI
│   │   │   ├── content_generator.py    # → HuggingFace/OpenAI
│   │   │   ├── critic.py               # → HuggingFace/OpenAI
│   │   │   ├── image_selector.py       # → HuggingFace/OpenAI
│   │   │   ├── html_builder.py         # → HuggingFace/OpenAI
│   │   │   └── README.md
│   │   ├── workflows/
│   │   │   └── blogger_style.py
│   │   ├── config/
│   │   │   └── default.toml
│   │   └── context.py
│   ├── src/
│   │   └── orchestrator/       # ✅ Sistema de orquestación completo
│   │       ├── main.py         # ✅ Con HTMLBuilder integrado (7 fases)
│   │       ├── config.py
│   │       ├── state.py
│   │       ├── runner.py
│   │       └── README.md
│   ├── tools/                  # ✅ Herramientas
│   │   ├── scraper.py          # ✅ Web scraper WordPress-optimizado
│   │   ├── README.md
│   │   └── examples_scraper.py
│   ├── tests/                  # ✅ Tests completos (40+ tests)
│   │   ├── test_workflow.py
│   │   ├── test_orchestrator.py
│   │   ├── test_agents.py
│   │   ├── test_scraper.py
│   │   └── test_html_builder.py  # ✅ NUEVO: 20+ tests HTMLBuilder
│   ├── examples_scraper.py
│   ├── test_full_pipeline.py   # ✅ NUEVO: Test completo end-to-end
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                   # ⏳ Pendiente Next.js
│   ├── app/
│   │   ├── api/
│   │   │   └── generate-post/
│   │   ├── posts/[slug]/
│   │   └── components/
│   ├── package.json
│   └── next.config.js
├── docs/                       # ✅ Documentación completa
│   ├── ORCHESTRATION_PLAN.md   # Plan maestro
│   ├── NEXT_STEPS.md           # Roadmap detallado
│   ├── VERCEL_DEPLOYMENT.md    # Guía Vercel
│   ├── MODAL_DEPLOYMENT.md     # ✅ NUEVO: Guía Modal + HuggingFace futures
│   ├── HTMLBUILDER_INTEGRATION.md  # ✅ NUEVO: Integración HTMLBuilder
│   ├── SCRAPER_IMPLEMENTATION.md   # ✅ NUEVO: Guía del scraper
│   ├── HUGGINGFACE_MIGRATION.md    # ✅ NUEVO: Migración completa a HF
│   └── ENVIRONMENT_VARIABLES.md
├── vercel.json                 # ✅ Config Vercel
└── README.md
```

## 👥 División de Tareas (3 Personas)

### 👤 Persona 1: Backend Lead + Workflows Core
**Responsabilidades:**
- Estructura base del `BloggerStyleWorkflow`
- Agentes principales:
  - `style_analyzer.py` - Análisis del estilo del blogger
  - `content_generator.py` - Redacción base + refinada  
  - `critic.py` - Crítica y feedback
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
  - `keyword_extractor.py` - Palabras clave y términos
  - `html_builder.py` - Construcción JSON/HTML
  - `image_selector.py` - Descripciones de imágenes
- Prompts tuneados en `prompts/`
- `runner.py` - CLI para ejecutar workflows
- Tests de integración
- Documentación técnica (`ARCHITECTURE.md`, `API.md`)
- **Integración con Modal** para deployment

**Branches:**
- `feature/keyword-extractor`
- `feature/html-builder`  
- `feature/image-selector`
- `feature/runner-cli`
- `feature/modal-deployment`
- `docs/architecture`

### 👤 Persona 3: Frontend Full Stack + DevOps
**Responsabilidades:**
- Frontend completo Next.js:
  - Componentes React (`<BlogLayout>`, `<PostHeader>`, `<PostBody>`, etc.)
  - Página dinámica `app/posts/[slug]/page.tsx`
  - API route `app/api/generate-post/route.ts`
  - Estilos y UX (Tailwind CSS)
- DevOps:
  - `docker-compose.yml` completo
  - GitHub Actions CI/CD
  - **Vercel deployment** para Next.js frontend
  - `SETUP.md` y `DEPLOYMENT.md`
- Testing frontend

**Branches:**
- `feature/blog-components`
- `feature/post-page`
- `feature/api-endpoint`
- `feature/docker-setup`
- `feature/vercel-deployment`
- `feature/ci-cd`
- `docs/setup`

## 🚀 Quick Start (Estado Actual)

### Backend - Sistema Completo con HuggingFace ✅

```bash
# 1. Clonar repositorio
git clone https://github.com/IES-Rafael-Alberti/blogger-agent-tfg.git
cd blogger-agent-tfg/backend

# 2. Setup automatizado con UV (10-100x más rápido que pip) ⚡
.\setup.ps1  # Windows
# o
./setup.sh   # Linux/macOS

# 3. Configurar API token (gratis) 🆓
export HF_TOKEN="your_huggingface_token"
# Obtén tu token gratis en: https://huggingface.co/settings/tokens

# Alternativa (pago): OpenAI como fallback
export OPENAI_API_KEY="sk-..."

# 4. Activar entorno
.venv\Scripts\Activate.ps1  # Windows
# o
source .venv/bin/activate    # Linux/macOS

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
- 🔄 **Fallback**: OpenAI como respaldo si HF no disponible
- 📖 [Guía completa de migración](docs/HUGGINGFACE_MIGRATION.md)

**Resultado:** JSON completo con:
- ✅ Análisis de estilo del blogger
- ✅ Keywords extraídas
- ✅ Contenido generado en Markdown
- ✅ Feedback de crítica
- ✅ **Estructura HTML/JSX** (new!)
  - HTML optimizado
  - JSX para React/Next.js
  - Meta tags SEO (title, description, keywords)
  - Tabla de contenidos (headings)
  - Tiempo de lectura y conteo de palabras
  - Componente Next.js completo
- ✅ Prompts de imágenes con ubicaciones

### Tests

```bash
# Ejecutar todos los tests (40+ tests)
pytest tests/ -v

# Tests del orquestador completo
pytest tests/test_orchestrator.py -v

# Tests de agentes
pytest tests/test_agents.py -v

# Tests del HTMLBuilder (20+ tests)
pytest tests/test_html_builder.py -v

# Test end-to-end completo
python test_full_pipeline.py
```

## 🚀 Integración con Modal (Pendiente)

**Modal** se usará para deployment serverless del backend Python:

### ¿Por qué Modal?
- Ejecución serverless de código Python
- Escalado automático según demanda
- Gestión de dependencias integrada
- GPU/CPU bajo demanda para LLMs
- Costos eficientes (pay-per-use)

### Implementación (Issue #5 - Pendiente)

```python
# backend/modal_app.py
import modal
from src.orchestrator.main import BloggerOrchestrator

stub = modal.Stub("blogger-agent")
image = modal.Image.debian_slim().pip_install_from_requirements("requirements.txt")

@stub.function(image=image, secrets=[modal.Secret.from_name("openai-secret")])
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

### Conexión Next.js → Modal

```typescript
// frontend/app/api/generate-post/route.ts
export async function POST(request: Request) {
  const { bloggerUrls, topic } = await request.json();
  
  const response = await fetch(process.env.MODAL_WEBHOOK_URL!, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ blogger_urls: bloggerUrls, topic })
  });
  
  const post = await response.json();
  return Response.json(post);
}
```

## 🔧 Setup Rápido

### Backend (Orquestador)

**Usando uv** (recomendado - 10-100x más rápido) ⚡:
```bash
cd backend

# Instalar uv si no lo tienes
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
# O: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows

# Crear entorno e instalar dependencias
uv venv
uv pip install -r requirements.txt

# Activar entorno
source .venv/bin/activate  # Linux/macOS
# O: .venv\Scripts\Activate.ps1  # Windows PowerShell

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
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend  
```bash
cd frontend
npm install
npm run dev
```

### Docker (Todo junto)
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
6. **Construcción HTML** (`html_builder`) → ✅ **NUEVO**: Convierte Markdown a HTML/JSX optimizado
   - Convierte Markdown a HTML usando `python-markdown`
   - Genera JSX para componentes React/Next.js
   - Extrae headings para tabla de contenidos (TOC)
   - Genera meta tags (title, description, keywords)
   - Calcula tiempo de lectura y conteo de palabras
   - Crea componente Next.js completo listo para usar
7. **Selección de Imágenes** (`image_selector`) → Prompts y ubicaciones para imágenes

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

- [Arquitectura](docs/ARCHITECTURE.md) - Diseño del sistema
- [Plan de Orquestación](docs/ORCHESTRATION_PLAN.md) - Plan completo de desarrollo ⭐
- [Próximos Pasos](docs/NEXT_STEPS.md) - Roadmap y tareas pendientes 📋
- [Orchestrator README](backend/src/orchestrator/README.md) - Documentación del orquestador
- [API](docs/API.md) - Especificación de agentes y workflows
- [Setup](docs/SETUP.md) - Configuración detallada
- [Modal Deployment](docs/MODAL_DEPLOYMENT.md) - Guía de deployment backend
- [Vercel Deployment](docs/VERCEL_DEPLOYMENT.md) - Guía de deployment frontend ✅

## 🧪 Testing

```bash
# Backend
cd backend
pytest tests/

# Frontend
cd frontend  
npm test
```

## 📦 Tech Stack

### Backend
- Python 3.11+
- Aphra (workflow framework)
- OpenAI API / OpenRouter
- **python-markdown** - Conversión Markdown→HTML (nuevo)
- **Pygments** - Syntax highlighting para código (nuevo)
- **beautifulsoup4** - Web scraping (nuevo)
- **lxml** - Parser HTML rápido (nuevo)
- Modal (serverless deployment) - Pendiente
- pytest (40+ tests)

### Frontend
- Next.js 14 (App Router)
- React 18
- TypeScript
- Tailwind CSS
- Jest + Testing Library

### DevOps
- Docker + Docker Compose
- GitHub Actions
- Modal (backend serverless)
- Vercel (frontend deployment)

## 📝 Licencia

MIT License - Ver [LICENSE](LICENSE) para detalles.

## 👨‍🎓 Proyecto Académico

Trabajo Final de Grado (TFG) - Especialización en IA y Big Data  
IES Rafael Alberti - 2026
