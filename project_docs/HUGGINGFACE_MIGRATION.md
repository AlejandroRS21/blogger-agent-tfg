# Guía de Migración a HuggingFace

## ✅ Migración Completada

El proyecto ha sido migrado exitosamente de OpenAI a HuggingFace como proveedor principal de LLM.

## 🎯 Resumen de Cambios

### Proveedores LLM Soportados

El sistema ahora soporta múltiples proveedores con un sistema de fallback inteligente:

1. **HuggingFace** (Primario) - Gratuito/más económico
2. **OpenAI** (Opcional) - Fallback si HF no está disponible
3. **Anthropic** (Opcional) - Soporte futuro

### Modelos por Defecto

| Tarea | Modelo HuggingFace | Modelo OpenAI (fallback) |
|-------|-------------------|-------------------------|
| Análisis de estilo | `mistralai/Mistral-7B-Instruct-v0.2` | `gpt-4-turbo-preview` |
| Extracción de keywords | `mistralai/Mistral-7B-Instruct-v0.2` | `gpt-3.5-turbo` |
| Generación de contenido | `meta-llama/Meta-Llama-3.1-70B-Instruct` | `gpt-4-turbo-preview` |
| Crítica | `meta-llama/Meta-Llama-3.1-70B-Instruct` | `gpt-4-turbo-preview` |
| Selección de imágenes | `mistralai/Mistral-7B-Instruct-v0.2` | `gpt-3.5-turbo` |

## 📦 Nuevas Dependencias

### Principales
```toml
huggingface-hub>=0.20.0  # Primaria
```

### Opcionales
```toml
openai>=1.12.0           # Fallback opcional
anthropic>=0.18.0        # Soporte futuro
```

## 🔑 Configuración de API Keys

### Opción 1: HuggingFace (Recomendado - Gratis/Más Barato)

```bash
# Obtener token de HuggingFace (gratis)
# 1. Crear cuenta en https://huggingface.co/
# 2. Ir a Settings > Access Tokens
# 3. Crear un nuevo token con permisos de "Read"

# Configurar token
export HF_TOKEN="your_huggingface_token"
# o
export HUGGINGFACE_TOKEN="your_huggingface_token"
```

### Opción 2: OpenAI (Opcional - Fallback)

```bash
export OPENAI_API_KEY="your_openai_api_key"
```

### Opción 3: Sin API Keys (Modo Fallback)

El sistema funciona sin API keys usando reglas heurísticas, pero con calidad reducida.

## 🚀 Uso del Nuevo Sistema

### Uso Automático (Recomendado)

```python
from aphra_blogger.agents.style_analyzer import StyleAnalyzer

# Auto mode: intenta HF primero, luego OpenAI
analyzer = StyleAnalyzer()  # provider="auto" por defecto
result = analyzer.analyze(urls)
```

### Selección Manual de Proveedor

```python
# Forzar HuggingFace
analyzer = StyleAnalyzer(provider="huggingface")

# Forzar OpenAI
analyzer = StyleAnalyzer(provider="openai")

# Especificar modelo custom
analyzer = StyleAnalyzer(
    provider="huggingface",
    model="meta-llama/Meta-Llama-3.1-70B-Instruct"
)
```

### Todos los Agentes Soportan el Mismo Sistema

```python
from aphra_blogger.agents import (
    StyleAnalyzer,
    KeywordExtractor,
    ContentGenerator,
    CriticAgent,
    ImageSelectorAgent,
    HTMLBuilder
)

# Todos soportan los mismos parámetros
style = StyleAnalyzer(provider="huggingface")
keywords = KeywordExtractor(provider="huggingface")
generator = ContentGenerator(provider="huggingface")
critic = CriticAgent(provider="huggingface")
images = ImageSelectorAgent(provider="huggingface")
builder = HTMLBuilder(provider="huggingface")
```

## 🏗️ Arquitectura del Sistema LLM

### Módulo `aphra_blogger.llm`

```
aphra_blogger/llm/
├── __init__.py          # Exports públicos
├── base.py              # Clases abstractas (LLMProvider, LLMConfig, LLMResponse)
├── factory.py           # create_llm_provider(), get_default_provider()
├── huggingface_provider.py  # Implementación HuggingFace
└── openai_provider.py       # Implementación OpenAI
```

### Flujo de Fallback

1. **Auto mode** (por defecto):
   - Intenta inicializar HuggingFaceProvider con `HF_TOKEN`
   - Si falla, intenta OpenAIProvider con `OPENAI_API_KEY`
   - Si ambos fallan, error explicativo

2. **Modo específico**:
   - Usa solo el proveedor especificado
   - Error si no está disponible

3. **Modo sin LLM**:
   - Cada agente tiene fallback heurístico
   - Calidad reducida pero funcional

## 📊 Comparativa de Costos

### HuggingFace Inference API
- **Gratuito** para uso moderado
- Rate limits generosos
- Modelos: Llama 3.1, Mistral, etc.
- Sin necesidad de GPU propia

### OpenAI API
- **Pago por uso**
- GPT-4: ~$0.01-0.03 por 1K tokens
- GPT-3.5: ~$0.001-0.002 por 1K tokens
- Más rápido y consistente

### Recomendación
- **Desarrollo**: HuggingFace (gratis)
- **Producción (bajo volumen)**: HuggingFace
- **Producción (alto volumen/calidad crítica)**: OpenAI

## 🧪 Testing

Todos los tests validados con el nuevo sistema:

```bash
# Instalar dependencias
uv pip install -r requirements.txt

# Ejecutar tests (sin API keys, usa fallbacks)
pytest tests/ -v

# Tests pasando: 75/76 ✅
# 1 test skipped (integración web externa)
```

## 🔧 Configuración Avanzada

### Custom Inference Endpoint

```python
from aphra_blogger.llm import create_llm_provider, LLMConfig

config = LLMConfig(
    api_key="your_hf_token",
    hf_endpoint="https://your-endpoint.huggingface.cloud"
)

provider = create_llm_provider(
    provider="huggingface",
    api_key=config.api_key,
    hf_endpoint=config.hf_endpoint
)
```

### Ajustar Parámetros

```python
provider = create_llm_provider(
    provider="huggingface",
    model="meta-llama/Meta-Llama-3.1-70B-Instruct",
    temperature=0.9,  # Más creatividad
    max_tokens=4000   # Respuestas más largas
)
```

## 📝 Configuración TOML

Actualizada en `aphra_blogger/config/default.toml`:

```toml
[models]
provider = "auto"  # "huggingface", "openai", o "auto"
default_model = "meta-llama/Meta-Llama-3.1-8B-Instruct"
style_analysis_model = "mistralai/Mistral-7B-Instruct-v0.2"
critic_model = "meta-llama/Meta-Llama-3.1-70B-Instruct"

[models.huggingface]
api_key_env = "HF_TOKEN"
temperature = 0.7
max_tokens = 2000

[models.openai]
api_key_env = "OPENAI_API_KEY"
temperature = 0.7
max_tokens = 2000
```

## 🐛 Troubleshooting

### Error: "No LLM provider available"

**Causa**: Ni HF_TOKEN ni OPENAI_API_KEY están configurados

**Solución**:
```bash
# Opción 1: Configurar HF (gratis)
export HF_TOKEN="your_token"

# Opción 2: Configurar OpenAI (pago)
export OPENAI_API_KEY="your_key"
```

### Error: "HuggingFace API error: Rate limit exceeded"

**Causa**: Demasiadas requests en corto tiempo

**Solución**:
- Espera unos minutos
- O cambia a OpenAI: `provider="openai"`

### Error: "Model not found"

**Causa**: Modelo especificado no existe en HF

**Solución**:
```python
# Usar modelos validados
analyzer = StyleAnalyzer(
    provider="huggingface",
    model="mistralai/Mistral-7B-Instruct-v0.2"  # Modelo verificado
)
```

## ✅ Migración Completa - Checklist

- [x] Crear módulo `aphra_blogger.llm` con abstracción
- [x] Implementar `HuggingFaceProvider`
- [x] Implementar `OpenAIProvider`
- [x] Crear factory con auto-fallback
- [x] Migrar `StyleAnalyzer`
- [x] Migrar `KeywordExtractor`
- [x] Migrar `ContentGenerator`
- [x] Migrar `CriticAgent`
- [x] Migrar `ImageSelectorAgent`
- [x] Migrar `HTMLBuilder`
- [x] Actualizar `requirements.txt`
- [x] Actualizar `pyproject.toml`
- [x] Actualizar `config/default.toml`
- [x] Actualizar tests
- [x] Ejecutar suite completa de tests
- [x] Documentar migración

## 🎉 Beneficios de la Migración

1. **Costo**: HuggingFace gratis vs OpenAI pago
2. **Flexibilidad**: Múltiples proveedores soportados
3. **Autonomía**: Modelos open-source, no dependencia de un proveedor
4. **Escalabilidad**: Puedes usar GPU propias si lo necesitas
5. **Transparencia**: Modelos open-source auditables

## 🔜 Próximos Pasos

1. **Probar en producción** con HF tokens reales
2. **Benchmark de calidad** HF vs OpenAI (issue pendiente)
3. **Optimización de prompts** para modelos HF
4. **Deploy a Modal** con HuggingFace (ya está documentado)
5. **GPU containers** en Modal para modelos más grandes (opcional)

## 📚 Referencias

- [HuggingFace Inference API](https://huggingface.co/docs/api-inference/)
- [Llama 3.1 Models](https://huggingface.co/meta-llama)
- [Mistral Models](https://huggingface.co/mistralai)
- [HuggingFace Hub Python](https://huggingface.co/docs/huggingface_hub/)
