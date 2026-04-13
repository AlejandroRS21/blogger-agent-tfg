# Backend - Blogger Agent

Backend Python del sistema multi-agente para mimetizar el estilo de escritura de bloggers.

## 🏗️ Estructura

```
backend/
├── aphra_blogger/
│   ├── llm/                       # Abstracción LLM multi-provider [✅ NUEVO]
│   │   ├── __init__.py
│   │   ├── base.py                # Clases abstractas
│   │   ├── factory.py             # Factory para proveedores
│   │   ├── huggingface_provider.py# HuggingFace (primario)
│   │   └── openai_provider.py     # OpenAI (fallback)
│   ├── agents/                    # Agentes especializados [✅ COMPLETADO]
│   │   ├── __init__.py
│   │   ├── style_analyzer.py      # Análisis de estilo → HF/OpenAI
│   │   ├── keyword_extractor.py   # Extracción de keywords → HF/OpenAI
│   │   ├── content_generator.py   # Generación de contenido → HF/OpenAI
│   │   ├── critic.py              # Crítica y evaluación → HF/OpenAI
│   │   ├── image_selector.py      # Selección de imágenes → HF/OpenAI
│   │   ├── html_builder.py        # Conversión Markdown→HTML/JSX → HF/OpenAI
│   │   └── README.md              # Documentación de agentes
│   ├── workflows/
│   │   ├── __init__.py
│   │   └── blogger_style.py       # Workflow principal
│   ├── config/
│   │   ├── __init__.py
│   │   └── default.toml           # Configuración LLM (HF primario)
│   ├── __init__.py
│   └── context.py                 # Contexto compartido
├── src/
│   └── orchestrator/              # Sistema de orquestación [✅ COMPLETADO]
│       ├── __init__.py
│       ├── main.py                # BloggerOrchestrator principal (7 fases)
│       ├── config.py              # OrchestratorConfig
│       ├── state.py               # StateManager y WorkflowState
│       ├── runner.py              # CLI interface
│       └── README.md              # Documentación del orquestador
├── tools/                         # Herramientas [✅ COMPLETADO]
│   ├── __init__.py
│   ├── scraper.py                 # Web scraper para corpus
│   └── README.md                  # Documentación del scraper
├── tests/                         # Tests unitarios (40+ tests)
│   ├── test_workflow.py
│   ├── test_orchestrator.py       # Tests del orquestador [✅]
│   ├── test_agents.py             # Tests de agentes [✅]
│   ├── test_scraper.py            # Tests del scraper [✅]
│   └── test_html_builder.py       # Tests del HTMLBuilder [✅ NUEVO]
├── modal_app.py                   # Deployment Modal [✅ NUEVO]
├── test_full_pipeline.py          # Test end-to-end [✅ NUEVO]
├── requirements.txt               # Dependencias Python
├── Dockerfile                     # Imagen Docker
└── README.md                      # Este archivo
```

## 🚀 Setup Local

## 🔁 Publicacion Continua (Feature 009)

El orquestador ahora incluye modo continuo para ejecutar ciclos de publicacion en cadencia fija.

### Ejecucion continua local (acotada)

```bash
cd backend
python -m src.orchestrator.runner \
  --topic "Novedades de IA para desarrollo" \
  --blog-url "https://javipas.com" \
  --continuous \
  --cycles 2 \
  --interval-seconds 0
```

### Estado operativo

El modo continuo mantiene estados `active`, `paused` y `degraded`, con historial de ciclos/incidentes en:

- `backend/outputs/continuous_history.json`

### Publicacion canonica en `docs/`

Cuando `write_canonical_docs=true` en configuracion, cada ciclo exitoso actualiza:

- `docs/posts.json`
- `docs/posts/<slug>.json`

### Requisitos Previos

- Python 3.11+
- **uv** (gestor de paquetes Python ultrarrápido)
- **HuggingFace Token** (gratis, recomendado): `HF_TOKEN` o `HUGGINGFACE_TOKEN`
  - O alternativamente: `OPENAI_API_KEY` (pago, fallback opcional)

### Obtener HuggingFace Token (Gratis) 🆓

1. Crear cuenta en [huggingface.co](https://huggingface.co/)
2. Ir a Settings > [Access Tokens](https://huggingface.co/settings/tokens)
3. Crear nuevo token con permisos "Read"
4. Configurar:
   ```bash
   export HF_TOKEN="your_huggingface_token"
   ```

### Instalación con uv ⚡

**Opción 1: Usando script automatizado** (recomendado):

```bash
# Linux/macOS
chmod +x setup.sh
./setup.sh

# Windows PowerShell
.\setup.ps1
```

**Opción 2: Instalación manual:**

1. **Instalar uv** (si no lo tienes):

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# O con pip
pip install uv
```

2. **Crear entorno virtual y instalar dependencias** (todo en un comando):

```bash
cd backend
uv venv
uv pip install -r requirements.txt
```

3. **Activar entorno virtual:**

```bash
# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate.bat
```

4. **Configurar variables de entorno:**

```bash
# Crear archivo .env (no commitear!)
echo "OPENAI_API_KEY=tu-api-key-aqui" > .env
```

### Ejecución

#### Opción 1: Ejecutar Orquestador (Recomendado) [✅ COMPLETADO]

```bash
# Configurar API key
export OPENAI_API_KEY="sk-..."

# Ejecutar pipeline completo
cd backend
python -m src.orchestrator.runner \
  --topic "El futuro de OpenClaw me alucina" \
  --blog-url "https://javipas.com" \
  --output "resultado.json"
```

El orquestador ejecuta automáticamente todos los agentes en secuencia (7 fases):
1. StyleAnalyzer - Analiza estilo del blogger
2. KeywordExtractor - Extrae keywords y expresiones  
3. ContentGenerator - Genera borrador inicial
4. CriticAgent - Evalúa calidad (score 0-10)
5. ContentGenerator - Refina contenido (si score < 7)
6. HTMLBuilder - Convierte a HTML/JSX para Next.js [✅ NUEVO]
7. ImageSelectorAgent - Selecciona ubicación de imágenes

#### Opción 2: Ejecutar workflow directamente:

```bash
cd backend
python -m aphra_blogger.workflows.blogger_style
```

Este comando ejecutará un ejemplo de prueba del workflow legacy.

#### Uso programático (Orquestador):

```python
from src.orchestrator.main import BloggerOrchestrator
from src.orchestrator.config import OrchestratorConfig

# Configurar
config = OrchestratorConfig(
    openai_api_key="sk-...",
    retry_max_attempts=3,
    save_state=True
)

# Inicializar orquestador
orchestrator = BloggerOrchestrator(config)

# Ejecutar pipeline completo
result = orchestrator.run(
    topic="OpenClaw me alucina",
    blogger_urls=["https://javipas.com"]
)

# Obtener resultados
print(f"Score: {result['critique']['overall_score']}/10")
print(f"Contenido: {result['final_content'][:200]}...")
print(f"Imágenes: {len(result['images'])}")
```

#### Uso programático (Workflow Legacy):

```python
from aphra_blogger.workflows.blogger_style import BloggerStyleWorkflow

workflow = BloggerStyleWorkflow()
result = workflow.run(
    blogger_urls=["https://ejemplo.com/blog"],
    topic="El futuro de la IA"
)
```

## 🐳 Docker

### Construir imagen:

```bash
cd backend
docker build -t blogger-agent-backend .
```

### Ejecutar contenedor:

```bash
docker run -e OPENAI_API_KEY=tu-api-key blogger-agent-backend
```

## ⚙️ Configuración

El archivo `aphra_blogger/config/default.toml` contiene la configuración principal:

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

### Configuraciones personalizadas:

```python
# Usar archivo de configuración personalizado
workflow = BloggerStyleWorkflow(config_path="path/to/custom_config.toml")
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Tests del orquestador
pytest tests/test_orchestrator.py -v

# Tests de agentes individuales
pytest tests/test_agents.py -v

# Tests del workflow legacy
pytest tests/test_workflow.py -v

# Con coverage
pytest --cov=aphra_blogger --cov=src.orchestrator tests/

# Test específico de un agente
pytest tests/test_agents.py::TestStyleAnalyzer -v
```

## 📝 Workflow

### Orquestador (Implementado - 7 Fases) ✅

El `BloggerOrchestrator` ejecuta automáticamente:

1. **STYLE_ANALYSIS** - StyleAnalyzer analiza tono, voz, expresiones
2. **KEYWORD_EXTRACTION** - KeywordExtractor extrae keywords, expresiones, temas
3. **CONTENT_GENERATION_DRAFT** - ContentGenerator crea borrador (1500-2500 palabras)
4. **CRITIQUE** - CriticAgent evalúa coherencia (0-10), estilo, engagement
5. **REFINEMENT** - ContentGenerator refina si score < 7 (max 2 iteraciones)
6. **IMAGE_SELECTION** - ImageSelectorAgent selecciona ubicaciones y genera prompts
7. **COMPLETE** - Resultado final con contenido + imágenes + metadatos

Cada fase tiene:
- Retry automático (3 intentos con exponential backoff)
- Logging detallado
- State persistence para debugging

### Workflow Legacy

El `BloggerStyleWorkflow` incluye placeholders para desarrollo futuro.

## 🔧 Desarrollo

### Linting y formato:

```bash
# Formatear código
black aphra_blogger/

# Linter
ruff check aphra_blogger/
```

### Agentes Disponibles:

Todos los agentes están implementados en `aphra_blogger/agents/`:
- ✅ `style_analyzer.py` - Análisis de estilo (tono, voz, estructura)
- ✅ `keyword_extractor.py` - Extracción de keywords y expresiones
- ✅ `content_generator.py` - Generación y refinamiento de contenido
- ✅ `critic.py` - Evaluación de calidad (scoring 0-10)
- ✅ `image_selector.py` - Selección estratégica de imágenes
- ✅ `html_builder.py` - Conversión Markdown→HTML/JSX para Next.js [✅ NUEVO]

Ver documentación completa: [aphra_blogger/agents/README.md](aphra_blogger/agents/README.md)

### Agregar nuevos agentes:

```python
# En aphra_blogger/agents/custom_agent.py
class CustomAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
    
    def process(self, data):
        # Implementar lógica
        return result

# Integrar en src/orchestrator/main.py
self.custom_agent = CustomAgent(api_key=config.openai_api_key)
```

## 🌐 Deployment en Modal

El backend puede desplegarse en [Modal](https://modal.com) como función serverless.

### Quick Start

```bash
# 1. Instalar Modal CLI
pip install modal

# 2. Autenticarse
modal token new

# 3. Configurar secret con API key
modal secret create openai-secret OPENAI_API_KEY="sk-your-key"

# 4. Desplegar
modal deploy backend/modal_app.py
```

### Probar el endpoint

```bash
curl -X POST https://[your-username]--blogger-agent-tfg-webhook.modal.run \
  -H "Content-Type: application/json" \
  -d '{
    "blogger_urls": ["https://javipas.com/post1"],
    6 agentes implementados (Issues #6, #7, #3):
  * StyleAnalyzer - Análisis de estilo
  * KeywordExtractor - Extracción de keywords
  * ContentGenerator - Generación y refinamiento
  * CriticAgent - Evaluación de calidad
  * ImageSelectorAgent - Selección de imágenes
  * HTMLBuilder - Conversión Markdown→HTML/JSX [✅ NUEVO]
- ✅ CLI runner avanzado con argparse
- ✅ Tests unitarios del orquestador y agentes (40+ tests)
- ✅ State management y retry logic
- ✅ Web scraper para corpus (Issue #2):
  * BlogScraper con soporte WordPress
  * Extracción limpia de contenido
  * Rate limiting configurable
  * Formato JSON estructurado
  * Tests completos
- ✅ Modal deployment preparado (Issue #5):
  * modal_app.py con funciones serverless
  * Webhook endpoint
  * Documentación completa
- ✅ Documentación completa

**Pendiente:**
- ⏳ Desplegar a Modal (testing real con deployment)
- ⏳ Frontend Next.js (Issue #4)
- ⏳ Replicar CSS de javipas.com (Issue #8)
- ⏳ Deployment a Vercel (documentado en docs/VERCEL_DEPLOYMENT.md)
- 🔮 Migración a modelos HuggingFace (futuro
1. Crear branch desde `develop`
2. Implementar cambios
3. Ejecutar tests
4. Crear PR con descripción clara

## 📋 Roadmap

**Completado:**
- ✅ Estructura base del proyecto
- ✅ Workflow principal con placeholders
- ✅ Configuración TOML
- ✅ Contexto compartido
- ✅ Sistema de orquestación completo (Issue #9)
- ✅ 5 agentes implementados (Issues #6, #7):
  * StyleAnalyzer - Análisis de estilo
  * KeywordExtractor - Extracción de keywords
  * ContentGenerator - Generación y refinamiento
  * CriticAgent - Evaluación de calidad
  * ImageSelectorAgent - Selección de imágenes
- ✅ CLI runner avanzado con argparse
- ✅ Tests unitarios del orquestador
- ✅ Tests de agentes individuales
- ✅ State management y retry logic
- ✅ Web scraper para corpus (Issue #2):
  * BlogScraper con soporte WordPress
  * Extracción limpia de contenido
  * Rate limiting configurable
  * Formato JSON estructurado
  * Tests completos
- ✅ Documentación completa

**Pendiente:**
- ⏳ Agente HTMLBuilder (Issue #3)
- ⏳ Integración con Modal para deployment (Issue #5)
- ⏳ Frontend Next.js (Issue #4)
- ⏳ Replicar CSS de javipas.com (Issue #8)
- ⏳ Deployment a Vercel (documentado en docs/VERCEL_DEPLOYMENT.md)

## 📧 Soporte

Para dudas sobre el backend, contactar al Backend Lead (Persona 1).
