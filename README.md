# Blogger Agent TFG (Static Edition)

> Sistema multi-agente de IA para mimetizar estilos de escritura, con generación visual (Daggr) y despliegue estático en GitHub Pages.

## � Despliegue Automatizado (GitHub Pages)

Para que el blog se actualice en la web (`https://AlejandroRS21.github.io/blogger-agent-tfg/`), el sistema incluye un botón interactivo **🌐 DESPLEGAR BLOG** en la interfaz de usuario.

### ¿Cómo funciona el despliegue?
1.  **Generación Local**: El sistema guarda los archivos JSON en `docs/posts/`.
2.  **Sincronización Automática**: Al pulsar el botón de despliegue, el backend ejecuta el script `deploy.ps1`.
3.  **Git Subtree**: El script utiliza el comando `git subtree push --prefix docs origin gh-pages` para enviar **únicamente** la carpeta `docs` a la rama de producción sin interferir con el código fuente del `main`.

> [!NOTE]
> Debes tener permisos de escritura en el repositorio y haber configurado tu usuario de Git localmente para que el botón funcione sin pedir contraseña.

---

## �📋 Descripción del Proyecto

Sistema multi-agente que analiza el estilo de un blogger y genera artículos que mimetizan su tono. Esta versión utiliza un **backend serverless en Modal** con el modelo **Qwen 2.5 7B** (desplegado en GPUs NVIDIA A10G) para máxima velocidad y privacidad, eliminando cualquier dependencia de OpenAI.

## 🏗️ Arquitectura Actualizada

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
│   ├── test_full_pipeline.py   # ✅ Test completo end-to-end
│   ├── daggr_blogger_workflow.py  # ✅ Workflow visual con Daggr
│   ├── outputs/                # ✅ Posts generados (JSON)
│   ├── requirements.txt        # daggr>=0.7.0 (incluye Gradio)
│   ├── DAGGR_WORKFLOW.md       # ✅ NUEVO: Documentación Daggr
│   └── Dockerfile
├── frontend/                   # ✅ Next.js + TypeScript + Tailwind
│   ├── app/
│   │   ├── api/
│   │   │   └── generate-post/
│   │   │       └── route.ts    # ✅ API endpoint con modo mock
│   │   ├── components/
│   │   │   ├── BlogLayout.tsx  # ✅ Layout principal
│   │   │   ├── PostHeader.tsx  # ✅ Metadata de posts
│   │   │   ├── PostBody.tsx    # ✅ Renderizado HTML
│   │   │   └── GenerateForm.tsx # ✅ Formulario de generación
│   │   ├── generate/
│   │   │   └── page.tsx        # ✅ Página del formulario
│   │   ├── posts/[slug]/
│   │   │   └── page.tsx        # ✅ Post dinámico
│   │   ├── types/
│   │   │   └── post.ts         # ✅ TypeScript types
│   │   ├── layout.tsx          # ✅ Root layout
│   │   ├── page.tsx            # ✅ Homepage con hero y features
│   │   └── globals.css
│   ├── .env.local              # ✅ Variables de entorno
│   ├── package.json
│   ├── README.md               # ✅ Documentación frontend
│   └── tailwind.config.ts
├── docs/                       # ✅ Documentación completa
│   ├── ORCHESTRATION_PLAN.md   # Plan maestro
│   ├── NEXT_STEPS.md           # Roadmap detallado
│   ├── VERCEL_DEPLOYMENT.md    # Guía Vercel
│   ├── MODAL_DEPLOYMENT.md     # ✅ NUEVO: Guía Modal + HuggingFace futures
│   ├── HTMLBUILDER_INTEGRATION.md  # ✅ NUEVO: Integración HTMLBuilder
│   ├── SCRAPER_IMPLEMENTATION.md   # ✅ NUEVO: Guía del scraper
│   ├── HUGGINGFACE_MIGRATION.md    # ✅ NUEVO: Migración completa a HF
│   ├── FRONTEND_IMPLEMENTATION.md  # ✅ NUEVO: Implementación frontend Next.js
│   ├── GRADIO_INTERFACE.md         # ✅ NUEVO: Interfaz Gradio para testing
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

### Frontend - Next.js con Modo Mock ✅

```bash
# 1. Ir al directorio frontend
cd frontend

# 2. Instalar dependencias
npm install

# 3. Configurar variables de entorno (opcional)
# .env.local ya está configurado con modo mock por defecto
# USE_MOCK=true (no requiere backend corriendo)

# 4. Iniciar servidor de desarrollo
npm run dev

# 5. Abrir en navegador
# http://localhost:3000
```

**✨ Frontend Completo:**
- 🎨 **4 Componentes**: BlogLayout, PostHeader, PostBody, GenerateForm
- 📄 **3 Páginas**: Homepage, Generate, Posts dinámicos
- 🔌 **API Route**: /api/generate-post con modo mock
- 🎯 **Modo Mock**: Testing sin backend (USE_MOCK=true)
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
- 📖 [Guía completa Daggr](backend/DAGGR_WORKFLOW.md)

### Testing End-to-End (Backend + Frontend)

```bash
# Terminal 1: Backend
cd backend
uv run uvicorn aphra_blogger.api:app --reload

# Terminal 2: Frontend (modo real)
cd frontend
# Editar .env.local: USE_MOCK=false
npm run dev

# Abrir http://localhost:3000 y generar posts
```


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

## 📊 Estado del Proyecto

### ✅ Completado (Backend - 100%)
- **LLM Abstraction**: Multi-provider con HuggingFace (gratis) y OpenAI (fallback)
- **6 Agentes**: StyleAnalyzer, KeywordExtractor, ContentGenerator, Critic, ImageSelector, HTMLBuilder
- **Orquestador**: 7 fases completas con integración de todos los agentes
- **Scraper**: WordPress-optimizado para blogs (javipas.com compatible)
- **Tests**: 76 tests (75 passing, 1 skipped)
- **Documentación**: 5 guías completas (ORCHESTRATION, HUGGINGFACE_MIGRATION, HTMLBUILDER, etc.)

### ✅ Completado (Frontend - 100%)
- **Next.js 16**: React 19 + TypeScript 5 + Tailwind CSS 4
- **4 Componentes**: BlogLayout, PostHeader, PostBody, GenerateForm
- **3 Páginas**: Homepage (hero + features), Generate (formulario), Posts dinámicos
- **API Route**: `/api/generate-post` con modo mock para desarrollo
- **Configuración**: .env.local con variables de entorno
- **Servidor**: Dev server corriendo en puerto 3000/3001

### ⏳ Pendiente
- **Tests Frontend**: Jest + Testing Library
- **Integración E2E**: Backend Python + Frontend Next.js
- **Deploy Modal**: Backend serverless con HuggingFace
- **Deploy Vercel**: Frontend en producción
- **CI/CD**: GitHub Actions para testing y deployment

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
- [**Daggr Workflow**](backend/DAGGR_WORKFLOW.md) - Guía completa de Daggr ✅ **NUEVO**
- [API](docs/API.md) - Especificación de agentes y workflows
- [Setup](docs/SETUP.md) - Configuración detallada
- [Modal Deployment](docs/MODAL_DEPLOYMENT.md) - Guía de deployment backend
- [Vercel Deployment](docs/VERCEL_DEPLOYMENT.md) - Guía de deployment frontend ✅
- [HuggingFace Migration](docs/HUGGINGFACE_MIGRATION.md) - Migración a HF ✅
- [Frontend Implementation](docs/FRONTEND_IMPLEMENTATION.md) - Guía frontend Next.js ✅

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
- **HuggingFace Inference API** - LLM primario (gratis) ✅
- OpenAI API - Fallback opcional
- **Daggr 0.7.0** - Workflow visual y debugging ✅
- **python-markdown** - Conversión Markdown→HTML
- **Pygments** - Syntax highlighting para código
- **beautifulsoup4** - Web scraping
- **lxml** - Parser HTML rápido
- Modal (serverless deployment) - Pendiente
- pytest (40+ tests)

### Frontend
- Next.js 16.1.6 (App Router) ✅
- React 19.2.3 ✅
- TypeScript 5 ✅
- Tailwind CSS 4 ✅
- Jest + Testing Library (pendiente)

### Testing & Debugging
- **Daggr** - Visualización workflow, inspección nodos, re-ejecución ✅
- pytest - Tests unitarios e integración
- Mock mode - Testing frontend sin backend ✅

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
