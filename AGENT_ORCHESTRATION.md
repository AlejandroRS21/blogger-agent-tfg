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
   - `Agente de Análisis de Tono` -> Devuelve perfil estilístico.
   - `Agente de Análisis de Temáticas` -> Devuelve conceptos clave.
   - `Agente de Palabras Frecuentes` -> Devuelve lista de términos.
3. **Orquestador consolida**: Crea un "Contexto de Estilo" unificado.

### **Fase 2: Generación (Creation Phase)**
1. **Input**: Contexto de Estilo + Tema.
2. **Orquestador llama a**:
   - `Agente Generador de Texto Base` -> Devuelve borrador inicial.
   - `Agente de Mimesis` (Input: Texto Base + Contexto Estilo) -> Devuelve texto mimetizado.
   - `Agente de Selección de Imágenes` -> Devuelve URLs de imágenes.

### **Fase 3: Refinamiento (Review Phase)**
1. **Input**: Texto Mimetizado + Imágenes.
2. **Orquestador llama a**:
   - `Agente Crítico` -> Devuelve feedback o aprobación.
3. **Decisión**: 
   - SI (Aprobado): Pasa a Fase 4.
   - NO (Feedback): Re-ejecuta `Agente de Mimesis` con el feedback.

### **Fase 4: Publicación (Output Phase)**
1. **Orquestador llama a**:
   - `Agente de Estructura Next.js` -> Devuelve HTML/JSX final.
2. **Finalización**: Notifica éxito y guarda el resultado.

---

## 🛠️ Implementación con Aphra

El orquestador se implementa como un **Workflow** de Aphra que conecta los agentes.

### **Estructura del Código (Conceptual)**

```python
# orchestrator/main.py
from aphra import Workflow, Agent, State

class BloggerOrchestrator(Workflow):
    def __init__(self):
        super().__init__("blogger-agent-orchestrator")
        
        # Registro de Agentes
        self.researchers = [
            Agent("tone-analyzer"),
            Agent("topic-extractor"),
            Agent("frequency-analyser")
        ]
        self.creators = [
            Agent("base-writer"),
            Agent("mimicry-expert"),
            Agent("image-selector")
        ]
        self.reviewer = Agent("critic-agent")
        self.builder = Agent("nextjs-builder")

    async def run(self, topic: str):
        # 1. Investigación
        style_context = await self.run_agents_parallel(self.researchers)
        
        # 2. Generación
        draft = await self.creators[0].execute(topic)
        final_text = await self.creators[1].execute(draft, style_context)
        images = await self.creators[2].execute(final_text)
        
        # 3. Revisión (Bucle de feedback)
        is_approved = False
        while not is_approved:
            feedback = await self.reviewer.execute(final_text)
            if feedback.status == "approved":
                is_approved = True
            else:
                final_text = await self.creators[1].execute(final_text, feedback.suggestions)
        
        # 4. Construcción Final
        final_page = await self.builder.execute(final_text, images)
        
        return final_page
```

---

## 🤖 Skills del Orquestador (para Copilot)

Para que Copilot ayude a construir el Orquestador:

```yaml
Skill: Agent Orchestration
Focus:
  - Aphra Workflow state management
  - Parallel vs Sequential agent execution
  - Data mapping between agents
  - Conditional logic and feedback loops
  - Error handling and retries in distributed systems
```

---

## 📈 Dashboard de Monitoreo

El Orquestador debe proporcionar información de estado para el frontend:

- **Progreso**: % completado del workflow.
- **Estado de Agentes**: Idle, Running, Success, Failed.
- **Logs**: Actividad en tiempo real de lo que cada agente está haciendo.
- **Artifacts**: Vista previa de los resultados intermedios.

---

**Última actualización**: 10 de febrero de 2026
