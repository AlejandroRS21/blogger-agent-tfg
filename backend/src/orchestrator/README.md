# Orchestrator Module

> Central orchestration system for the Blogger Agent workflow

## 📋 Overview

El orquestador es el componente central que coordina todos los agentes del sistema. Implementa un pipeline robusto de 7 fases con gestión de errores, reintentos automáticos, y seguimiento de estado.

## 🏗️ Estructura

```
src/orchestrator/
├── __init__.py          # Exports principales
├── main.py              # BloggerOrchestrator (orquestador principal)
├── config.py            # OrchestratorConfig (configuración)
├── state.py             # StateManager y WorkflowState (gestión de estado)
└── runner.py            # CLI ejecutable
```

## 🚀 Uso Rápido

### CLI (Recomendado)

```bash
python -m src.orchestrator.runner \
  --topic "OpenClaw me alucina" \
  --blog-url "https://javipas.com" \
  --output "generated_post.json"
```

### Programático

```python
from src.orchestrator import BloggerOrchestrator, OrchestratorConfig

# Crear configuración
config = OrchestratorConfig.default()

# Inicializar orquestador
orchestrator = BloggerOrchestrator(config=config)

# Ejecutar workflow
result = orchestrator.run(
    topic="El futuro de la IA",
    blogger_urls=["https://javipas.com"],
    output_path="output.json"
)

# Acceder a resultados
print(result['content'])
print(result['keywords'])
```

## 📊 Pipeline de Ejecución

### Fase 1: Análisis de Estilo
**Agente:** `StyleAnalyzer`  
**Output:** `StyleProfile` con tono, voz, estructura, expresiones

### Fase 2: Extracción de Keywords
**Agente:** `KeywordExtractor`  
**Output:** Lista de keywords y expresiones frecuentes

### Fase 3: Generación de Borrador
**Agente:** `ContentGenerator`  
**Output:** Borrador inicial (1500-2500 palabras)

### Fase 4: Crítica (opcional)
**Agente:** `CriticAgent`  
**Output:** Feedback sobre coherencia y estilo

### Fase 5: Refinamiento (opcional)
**Agente:** `ContentGenerator`  
**Output:** Versión refinada basada en feedback

### Fase 6: Construcción HTML
**Agente:** `HTMLBuilder`  
**Output:** Estructura JSON/HTML para rendering

### Fase 7: Selección de Imágenes
**Agente:** `ImageSelectorAgent`  
**Output:** Prompts y ubicaciones de imágenes

## ⚙️ Configuración

### Archivo TOML

```toml
# config/default.toml
[models]
default_model = "gpt-4-turbo-preview"
temperature = 0.7
max_tokens = 2000

[workflow]
max_iterations = 3
enable_critic = true
verbose = true

[content]
min_word_count = 800
max_word_count = 2500
```

### Configuración Programática

```python
config = OrchestratorConfig(
    default_model="gpt-4-turbo-preview",
    max_retries=3,
    enable_critique=True,
    verbose=True,
    openai_api_key=os.getenv('OPENAI_API_KEY')
)

config.validate()  # Valida la configuración
```

## 🛡️ Gestión de Errores

### Reintentos Automáticos

El orquestador implementa reintentos con backoff exponencial:

```python
# Configuración de reintentos
config = OrchestratorConfig(
    max_retries=3,           # 3 intentos
    retry_delay=1.0,         # 1 segundo inicial
    backoff_factor=2.0,      # Duplica el delay
)
```

**Cronograma de reintentos:**
- Intento 1: Inmediato
- Intento 2: 1 segundo después
- Intento 3: 2 segundos después
- Intento 4: 4 segundos después

### Manejo de Fallas

```python
try:
    result = orchestrator.run(topic="Test", blogger_urls=["https://example.com"])
except Exception as e:
    print(f"Workflow failed: {e}")
    # El estado se guarda automáticamente si se especificó output_path
```

## 📈 Seguimiento de Estado

### StateManager

Rastrea el progreso de cada fase:

```python
state = orchestrator.get_state()

# Información del workflow
print(state.workflow_id)
print(state.topic)
print(state.current_phase)

# Resultados intermedios
print(state.style_profile)
print(state.keywords)
print(state.draft_content)

# Errores y warnings
print(state.errors)
print(state.warnings)
```

### Guardar/Cargar Estado

```python
# Guardar automáticamente
orchestrator.run(
    topic="Test",
    blogger_urls=["https://example.com"],
    output_path="state.json"
)

# Cargar estado guardado
from src.orchestrator.state import StateManager
manager = StateManager.load_from_file("state.json")
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest tests/test_orchestrator.py -v

# Test específico
pytest tests/test_orchestrator.py::TestBloggerOrchestrator::test_orchestrator_run_basic -v

# Con coverage
pytest tests/test_orchestrator.py --cov=src.orchestrator --cov-report=html
```

## 📝 Ejemplos de Uso

### Ejemplo 1: Uso Básico

```bash
python -m src.orchestrator.runner \
  --topic "Claude vs ChatGPT" \
  --blog-url "https://javipas.com"
```

### Ejemplo 2: Múltiples URLs

```bash
python -m src.orchestrator.runner \
  --topic "IA en educación" \
  --blog-url "https://javipas.com" \
  --blog-url "https://javipas.com/category/ia" \
  --output "post.json"
```

### Ejemplo 3: Sin Crítica

```bash
python -m src.orchestrator.runner \
  --topic "Mi tema" \
  --blog-url "https://example.com" \
  --no-critique \
  --quiet
```

### Ejemplo 4: Configuración Custom

```bash
python -m src.orchestrator.runner \
  --topic "Mi tema" \
  --blog-url "https://example.com" \
  --config "my_config.toml" \
  --max-retries 5
```

## 📊 Output Format

El orquestador genera un JSON con la siguiente estructura:

```json
{
  "workflow_id": "abc12345",
  "topic": "OpenClaw me alucina",
  "blogger_urls": ["https://javipas.com"],
  "style_profile": {
    "tone": "conversational, humorous",
    "expressions": ["me alucina", "dicho y hecho"]
  },
  "keywords": ["IA", "OpenClaw", "tecnología"],
  "content": "# OpenClaw me alucina\n\nSé que estoy un poco...",
  "html_structure": {
    "title": "OpenClaw me alucina",
    "sections": [...]
  },
  "image_prompts": [
    {
      "position": "header",
      "prompt": "Professional image about AI",
      "alt_text": "AI illustration"
    }
  ],
  "metadata": {
    "duration": 15.3,
    "phases": {...},
    "errors": [],
    "warnings": []
  }
}
```

## 🔧 Desarrollo

### Agregar Nueva Fase

1. Crear método `_phase_nombre` en `main.py`
2. Llamar desde `run()` en el orden apropiado
3. Actualizar `StateManager` si necesitas nuevos campos

```python
def _phase_mi_nueva_fase(self) -> None:
    """Mi nueva fase."""
    phase_name = "mi_nueva_fase"
    self.state_manager.start_phase(phase_name, "MiAgente")
    
    def ejecutar():
        # Tu lógica aquí
        return resultado
    
    result = self._execute_with_retry(phase_name, "MiAgente", ejecutar)
    self.state_manager.state.mi_resultado = result
    self.state_manager.complete_phase(phase_name, result)
```

### Agregar Nuevo Agente

Los agentes se implementarán en `backend/aphra_blogger/agents/`:

```python
# agents/mi_agente.py
class MiAgente:
    def ejecutar(self, context: dict) -> dict:
        """Lógica del agente."""
        # Implementar aquí
        return resultado
```

Luego integrarlo en el orquestador:

```python
from aphra_blogger.agents.mi_agente import MiAgente

def _phase_mi_fase(self):
    agente = MiAgente()
    result = agente.ejecutar(self.state_manager.state.to_dict())
    # ...
```

## 🐛 Troubleshooting

### Error: "At least one API key must be set"

**Solución:**
```bash
export OPENAI_API_KEY="sk-..."
# O
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Error: "Config file not found"

**Solución:**
```bash
# Verificar ruta
ls backend/aphra_blogger/config/default.toml

# O especificar ruta personalizada
python -m src.orchestrator.runner --config "path/to/config.toml" ...
```

### Workflow muy lento

**Optimización:**
1. Reducir `max_retries` en la config
2. Usar modelos más rápidos (`gpt-3.5-turbo`)
3. Deshabilitar crítica con `--no-critique`

### Logs demasiado verbosos

```bash
python -m src.orchestrator.runner --quiet ...
```

## 🚀 Próximos Pasos

- [ ] Implementar agentes reales (actualmente placeholders)
- [ ] Agregar persistencia de estado en DB
- [ ] Implementar ejecución paralela de fases independientes
- [ ] Webhooks para notificaciones de progreso
- [ ] Dashboard web para monitoreo en tiempo real

## 📚 Referencias

- [ORCHESTRATION_PLAN.md](../../docs/ORCHESTRATION_PLAN.md) - Plan completo de orquestación
- [ARCHITECTURE.md](../../docs/ARCHITECTURE.md) - Arquitectura del sistema
- [API.md](../../docs/API.md) - Especificación de agentes

---

**Última actualización:** 10 Feb 2026  
**Versión:** 0.1.0
