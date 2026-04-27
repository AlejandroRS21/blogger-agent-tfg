# Agent Orchestration - Blogger Agent TFG

Este documento define el **Agente de Orquestación**, el cerebro central que coordina el flujo de trabajo entre todos los agentes especializados del proyecto.

---

## 🧠 El Agente Orquestador (Orchestrator Agent)

El Orquestador no realiza tareas de análisis o generación directamente, sino que **gestiona el ciclo de vida del contenido** y asegura que cada agente reciba la información necesaria en el momento adecuado.

### **Responsabilidades Clave:**
1. **Gestión del Flujo**: Inicia y detiene los procesos según el estado actual.
2. **Pasos de Datos**: Transfiere los resultados de un agente como input para el siguiente.
3. **Control de Calidad**: Decide si un resultado es suficiente o si debe re-ejecutarse un agente.
4. **Manejo de Errores**: Gestiona fallos en agentes individuales y decide estrategias de recuperación.
5. **Estado Global**: Mantiene el estado del artículo en desarrollo (Metadata, Texto Base, Imágenes, Estilo).

---

## 🔄 Flujo de Orquestación (Workflow)

El Orquestador sigue este flujo secuencial utilizando **Aphra Workflows**:

### **Fase 1: Análisis (Research Phase)**
1. **Input**: URL del blog o tema específico.
2. **Orquestador llama a**:
   - `StyleAnalyzer` → Devuelve perfil estilístico (tono, voz, estructura).
   - `KeywordExtractor` → Devuelve keywords, expresiones y temáticas.
   - `ResearchAgent` → Contexto adicional y exploración del tema.
3. **Orquestador consolida**: Crea un "Contexto de Estilo" unificado.

### **Fase 2: Generación (Creation Phase)**
1. **Input**: Contexto de Estilo + Tema.
2. **Orquestador llama a**:
   - `ContentGenerator.generate_draft()` → Borrador inicial con estilo mimetizado.
   - `ImageSelectorAgent` → Prompts y ubicaciones para imágenes.

### **Fase 3: Refinamiento (Review Phase)**
1. **Input**: Texto generado.
2. **Orquestador llama a**:
   - `CriticAgent` → Feedback o aprobación.
3. **Decisión**:
   - SI (Aprobado): Pasa a Fase 4.
   - NO (Feedback): Re-ejecuta `ContentGenerator.refine_content()` con el feedback.

### **Fase 4: Publicación (Output Phase)**
1. **Orquestador llama a**:
   - `HTMLBuilder` → Convierte Markdown a HTML/JSX con TOC y meta tags.
2. **Finalización**: Guarda resultado en `outputs/` y notifica éxito.

---

## 🛠️ Implementación

El orquestador se implementa en `src/orchestrator/main.py` como `BloggerOrchestrator`:

```python
# src/orchestrator/main.py
from src.orchestrator.config import OrchestratorConfig
from src.orchestrator.state import OrchestratorState

class BloggerOrchestrator:
    def __init__(self, config: OrchestratorConfig, verbose: bool = False):
        self.config = config
        self.state = OrchestratorState()
    
    def run(self, topic: str, blogger_urls: list[str]) -> dict:
        # 1. Análisis de estilo
        style = self._analyze_style(blogger_urls)
        
        # 2. Extracción de keywords
        keywords = self._extract_keywords(blogger_urls)
        
        # 3. Generación de contenido
        content = self._generate_content(topic, style, keywords)
        
        # 4. Crítica y refinamiento (bucle de feedback)
        content = self._critique_and_refine(content, style)
        
        # 5. Construcción HTML/JSX
        html_output = self._build_html(content)
        
        # 6. Selección de imágenes
        images = self._select_images(content, topic)
        
        return {
            "content": content,
            "html_structure": html_output,
            "images": images,
            "style_profile": style,
            "keywords": keywords,
        }
```

### Agentes del Sistema

| Nombre en Documentación | Archivo | Rol |
|------------------------|---------|-----|
| StyleAnalyzer | `style_analyzer.py` | Análisis de tono, voz y estilo |
| KeywordExtractor | `keyword_extractor.py` | Extracción de keywords y patrones |
| ContentGenerator | `content_generator.py` | Generación de draft + refinamiento |
| CriticAgent | `critic.py` | Revisión y feedback de calidad |
| ImageSelectorAgent | `image_selector.py` | Selección de imágenes y prompts |
| HTMLBuilder | `html_builder.py` | Conversión Markdown→HTML/JSX |
| ResearchAgent | `research_agent.py` | Investigación de temas y contexto |

---

## 📈 Dashboard de Monitoreo

El Orquestador proporciona información de estado para el frontend:

- **Progreso**: % completado del workflow.
- **Estado de Agentes**: Idle, Running, Success, Failed.
- **Logs**: Actividad en tiempo real de lo que cada agente está haciendo.
- **Artifacts**: Vista previa de los resultados intermedios.

---

## 🔧 Ejecución

```bash
# Orquestador completo (7 fases)
cd backend
python -m src.orchestrator.runner \
  --topic "Las mejores prácticas para desarrollar APIs REST con Python" \
  --blog-url "https://javipas.com" \
  --output "post.json"

# Publicación continua
python -m src.orchestrator.runner --continuous --cycles 5
```

---

**Última actualización**: Abril 2026
