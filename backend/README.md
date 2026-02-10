# Backend - Blogger Agent

Backend Python del sistema multi-agente para mimetizar el estilo de escritura de bloggers.

## 🏗️ Estructura

```
backend/
├── aphra_blogger/
│   ├── workflows/
│   │   ├── __init__.py
│   │   └── blogger_style.py       # Workflow principal
│   ├── config/
│   │   ├── __init__.py
│   │   └── default.toml           # Configuración LLM
│   ├── __init__.py
│   └── context.py                 # Contexto compartido
├── tests/                         # Tests unitarios
├── requirements.txt               # Dependencias Python
├── Dockerfile                     # Imagen Docker
└── README.md                      # Este archivo
```

## 🚀 Setup Local

### Requisitos Previos

- Python 3.11+
- pip o uv
- Variable de entorno `OPENAI_API_KEY` (o `ANTHROPIC_API_KEY`)

### Instalación

1. **Crear entorno virtual:**

```bash
cd backend
python -m venv venv
```

2. **Activar entorno virtual:**

```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. **Instalar dependencias:**

```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno:**

```bash
# Crear archivo .env (no commitear!)
echo "OPENAI_API_KEY=tu-api-key-aqui" > .env
```

### Ejecución

#### Ejecutar workflow directamente:

```bash
cd backend
python -m aphra_blogger.workflows.blogger_style
```

Este comando ejecutará un ejemplo de prueba del workflow.

#### Uso programático:

```python
from aphra_blogger.workflows.blogger_style import BloggerStyleWorkflow

# Inicializar workflow
workflow = BloggerStyleWorkflow()

# Ejecutar con parámetros
result = workflow.run(
    blogger_urls=[
        "https://ejemplo.com/blog/post1",
        "https://ejemplo.com/blog/post2"
    ],
    topic="El futuro de la IA en educación"
)

# Obtener resultados
print(result['final_content'])
print(result['keywords'])
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
# Ejecutar tests
pytest tests/

# Con coverage
pytest --cov=aphra_blogger tests/

# Tests específicos
pytest tests/test_workflow.py -v
```

## 📝 Workflow

El `BloggerStyleWorkflow` sigue este proceso:

1. **Análisis de Estilo** - Analiza URLs del blogger
2. **Extracción de Keywords** - Identifica palabras clave recurrentes
3. **Generación Base** - Crea borrador inicial
4. **Crítica** - Feedback sobre coherencia (opcional)
5. **Refinamiento** - Versión final con estilo aplicado
6. **HTML Builder** - Estructura JSON/HTML
7. **Image Selector** - Prompts para imágenes

## 🔧 Desarrollo

### Linting y formato:

```bash
# Formatear código
black aphra_blogger/

# Linter
ruff check aphra_blogger/
```

### Agregar nuevos agentes:

Los agentes se implementarán en futuras iteraciones en `workflows/agents/`:
- `style_analyzer.py`
- `keyword_extractor.py`
- `content_generator.py`
- `critic.py`
- `html_builder.py`
- `image_selector.py`

## 🌐 Integración con Modal

Para deployment serverless, ver `modal_app.py` (próximamente).

## 📚 Dependencias Principales

- **openai** - Cliente OpenAI API
- **anthropic** - Cliente Anthropic API (opcional)
- **toml** - Parsing de configuración
- **pydantic** - Validación de datos
- **pytest** - Framework de testing

## 🤝 Contribuir

1. Crear branch desde `develop`
2. Implementar cambios
3. Ejecutar tests
4. Crear PR con descripción clara

## 📋 Roadmap

- [x] Estructura base del proyecto
- [x] Workflow principal con placeholders
- [x] Configuración TOML
- [x] Contexto compartido
- [ ] Implementar agentes individuales
- [ ] Tests unitarios completos
- [ ] Integración con Modal
- [ ] CLI runner avanzado

## 📧 Soporte

Para dudas sobre el backend, contactar al Backend Lead (Persona 1).
