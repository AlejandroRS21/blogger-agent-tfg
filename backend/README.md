# Backend - Blogger Agent TFG

Backend Python del sistema multi-agente para mimetizar el estilo de escritura de bloggers.

## 🏗️ Estructura

```
backend/
├── aphra_blogger/
│   ├── llm/                          # Abstracción LLM multi-provider
│   │   ├── __init__.py
│   │   ├── base.py                   # Clases abstractas
│   │   ├── factory.py                # Factory para proveedores
│   │   ├── huggingface_provider.py   # HuggingFace (primario, gratis)
│   │   ├── openai_provider.py        # OpenAI (fallback)
│   │   ├── gemini_provider.py        # Google Gemini (alternativo)
│   │   └── modal_provider.py         # Modal GPU (producción)
│   ├── agents/                       # Agentes especializados
│   │   ├── __init__.py
│   │   ├── style_analyzer.py         # Análisis de estilo → HF/OpenAI
│   │   ├── keyword_extractor.py      # Extracción de keywords → HF/OpenAI
│   │   ├── content_generator.py      # Generación de contenido → HF/OpenAI
│   │   ├── critic.py                 # Crítica y evaluación → HF/OpenAI
│   │   ├── image_selector.py         # Selección de imágenes → HF/OpenAI
│   │   ├── html_builder.py           # Markdown → HTML/JSX → HF/OpenAI
│   │   ├── anonymous_blogger.py      # Emulación de blogueros anónimos
│   │   ├── style_extractor.py        # Extracción legacy de estilo
│   │   └── README.md                 # Documentación de agentes
│   ├── workflows/
│   │   ├── __init__.py
│   │   └── blogger_style.py          # Workflow principal
│   ├── config/
│   │   ├── __init__.py
│   │   └── default.toml              # Configuración LLM
│   ├── __init__.py
│   └── context.py                    # Contexto compartido
├── src/
│   └── orchestrator/                 # Sistema de orquestación
│       ├── __init__.py
│       ├── main.py                   # BloggerOrchestrator (7 fases)
│       ├── config.py                 # OrchestratorConfig
│       ├── state.py                  # StateManager y WorkflowState
│       ├── runner.py                 # CLI interface
│       └── README.md                 # Documentación del orquestador
├── tools/                            # Herramientas
│   ├── __init__.py
│   ├── scraper.py                    # Web scraper WordPress
│   └── README.md                     # Documentación del scraper
├── tests/                            # ~80 tests
│   ├── test_agents.py                # Tests de agentes
│   ├── test_orchestrator.py          # Tests del orquestador
│   ├── test_html_builder.py          # Tests del HTMLBuilder (23 tests)
│   ├── test_scraper.py               # Tests del scraper
│   ├── test_workflow.py              # Tests del workflow
│   └── test_anonymous_blogger.py     # Tests de blogueros anónimos
├── daggr_blogger_workflow.py         # ⭐ Workflow visual con Daggr
├── modal_app.py                      # Deployment Modal (serverless)
├── llm_modal_host.py                 # Hosting LLM propio en Modal GPU
├── generate_and_deploy.py            # Pipeline simplificado
├── test_full_pipeline.py             # Test end-to-end
├── requirements.txt                  # Dependencias Python
├── pyproject.toml                    # Configuración del proyecto
├── Dockerfile                        # Imagen Docker
├── setup.sh / setup.ps1              # Scripts de instalación
└── README.md                         # Este archivo
```

## 🚀 Setup Local

### Requisitos Previos

- Python 3.11+
- **uv** (gestor de paquetes Python ultrarrápido)
- **HuggingFace Token** (gratis, recomendado): `HF_TOKEN`
- Alternativas: `GEMINI_API_KEY` (gratis), `OPENAI_API_KEY` (pago)

### Obtener HuggingFace Token (Gratis) 🆓

1. Crear cuenta en [huggingface.co](https://huggingface.co/)
2. Ir a Settings > [Access Tokens](https://huggingface.co/settings/tokens)
3. Crear nuevo token con permisos "Read"
4. Configurar:
   ```bash
   export HF_TOKEN="your_huggingface_token"
   ```

### Instalación con uv ⚡

**Opción 1: Script automatizado** (recomendado):

```bash
# Linux/macOS
chmod +x setup.sh
./setup.sh

# Windows PowerShell
.\setup.ps1
```

**Opción 2: Instalación manual:**

```bash
# Instalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
# o: pip install uv

cd backend
uv venv
uv pip install -r requirements.txt

# Activar entorno
source .venv/bin/activate     # Linux/macOS
# o: .venv\Scripts\Activate.ps1  # Windows
```

### Ejecución

#### Orquestador (7 fases) — Recomendado

```bash
# Con HuggingFace (gratis)
export HF_TOKEN="hf_..."
python -m src.orchestrator.runner \
  --topic "El futuro de la IA" \
  --blog-url "https://javipas.com" \
  --output "resultado.json" \
  --provider huggingface
```

Fases del orquestador:
1. **STYLE_ANALYSIS** — StyleAnalyzer analiza tono, voz, expresiones
2. **KEYWORD_EXTRACTION** — KeywordExtractor extrae keywords y temas
3. **CONTENT_GENERATION_DRAFT** — ContentGenerator crea borrador
4. **CRITIQUE** — CriticAgent evalúa coherencia (score 0-10)
5. **REFINEMENT** — ContentGenerator refina si score < 7
6. **HTML_BUILD** — HTMLBuilder convierte a HTML/JSX
7. **IMAGE_SELECTION** — ImageSelectorAgent selecciona ubicaciones

#### Uso programático

```python
from src.orchestrator.main import BloggerOrchestrator
from src.orchestrator.config import OrchestratorConfig

config = OrchestratorConfig(
    openai_api_key="sk-...",        # o huggingface_token="hf_..."
    provider="huggingface",
    retry_max_attempts=3,
    save_state=True
)

orchestrator = BloggerOrchestrator(config)
result = orchestrator.run(
    topic="OpenClaw me alucina",
    blogger_urls=["https://javipas.com"]
)

print(f"Score: {result['critique']['overall_score']}/10")
print(f"Contenido: {result['final_content'][:200]}...")
```

#### Workflow Visual con Daggr 🎨

```bash
python daggr_blogger_workflow.py
# → http://localhost:7860
```

Canvas interactivo con los 7 agentes, inspección por nodo, re-ejecución selectiva y debugging visual.

#### Pipeline Simplificado

```bash
python generate_and_deploy.py "Tema del artículo"
```

## 🐳 Docker

```bash
cd backend
docker build -t blogger-agent-backend .
docker run -e HF_TOKEN=tu-token blogger-agent-backend
```

## ⚙️ Configuración

`aphra_blogger/config/default.toml`:

```toml
[models]
default_model = "gpt-4-turbo-preview"
style_analysis_model = "gpt-3.5-turbo"
critic_model = "gpt-4-turbo-preview"

[workflow]
max_iterations = 3
enable_critic = true
verbose = true

[content]
min_word_count = 800
max_word_count = 2000
```

## 🧪 Testing

```bash
# Todos los tests (~80 tests)
pytest tests/ -v

# Por archivo
pytest tests/test_orchestrator.py -v
pytest tests/test_agents.py -v
pytest tests/test_html_builder.py -v

# Con coverage
pytest --cov=aphra_blogger --cov=src.orchestrator tests/

# Test end-to-end
python test_full_pipeline.py
```

## 🔧 Desarrollo

```bash
# Formatear
black aphra_blogger/ src/

# Linter
ruff check aphra_blogger/ src/
```

### Agentes Disponibles

Todos implementados en `aphra_blogger/agents/`:
- ✅ `style_analyzer.py` — Análisis de estilo (tono, voz, estructura)
- ✅ `keyword_extractor.py` — Extracción de keywords y expresiones
- ✅ `content_generator.py` — Generación y refinamiento de contenido
- ✅ `critic.py` — Evaluación de calidad (scoring 0-10)
- ✅ `image_selector.py` — Selección de imágenes y prompts
- ✅ `html_builder.py` — Conversión Markdown → HTML/JSX para Next.js
- ✅ `anonymous_blogger.py` — Emulación de blogueros anónimos
- ✅ `style_extractor.py` — Extracción legacy de perfil de estilo

Ver docs completas: [aphra_blogger/agents/README.md](aphra_blogger/agents/README.md)

## 🌐 Deployment en Modal

### Quick Start

```bash
# Instalar y autenticar
pip install modal
modal token new

# Configurar secretos
modal secret create hf-secret HF_TOKEN="hf-..."

# Desplegar orquestador serverless
modal deploy backend/modal_app.py

# O desplegar LLM propio con GPU
modal deploy backend/llm_modal_host.py
```

### Probar el endpoint

```bash
curl -X POST https://[tu-usuario]--blogger-agent-tfg-webhook.modal.run \
  -H "Content-Type: application/json" \
  -d '{
    "blogger_urls": ["https://javipas.com"],
    "topic": "El futuro de la IA"
  }'
```

## 📋 Roadmap

**Completado:**
- ✅ Estructura base del proyecto
- ✅ Workflow principal y sistema de orquestación (7 fases)
- ✅ 8 agentes implementados (StyleAnalyzer, KeywordExtractor, ContentGenerator, CriticAgent, ImageSelectorAgent, HTMLBuilder, AnonymousBloggerEmulator, StyleExtractor)
- ✅ CLI runner con argparse
- ✅ ~80 tests
- ✅ State management y retry logic
- ✅ Web scraper WordPress-optimizado
- ✅ Abstracción LLM multi-provider (HF, OpenAI, Gemini, Modal)
- ✅ Daggr workflow visual
- ✅ Modal deployment preparado (serverless + GPU hosting)

**Pendiente:**
- ⏳ CI/CD con GitHub Actions
- ⏳ Tests E2E para la web estática
- ⏳ Pruebas de deployment real en Modal

## 📧 Soporte

Repo: [github.com/AlejandroRS21/blogger-agent-tfg](https://github.com/AlejandroRS21/blogger-agent-tfg)
