# Daggr Workflow - Blogger Agent TFG

## 📋 Descripción

Este proyecto usa **Daggr** (herramienta oficial del equipo de Gradio) para la **generación y testing** de posts de blog, mientras que el **frontend Next.js** se encarga de la **visualización y gestión** de los blogs generados.

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA DEL PROYECTO                 │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────┐         ┌─────────────────────┐   │
│  │  FRONTEND (Next.js) │         │  BACKEND (Python)   │   │
│  │  Puerto: 3000       │         │  Puerto: 7860       │   │
│  ├─────────────────────┤         ├─────────────────────┤   │
│  │ • Visualizar blogs  │◄───────►│ • Daggr Workflow    │   │
│  │ • Listar posts      │         │ • 6 Agentes IA      │   │
│  │ • Interfaz usuario  │         │ • Testing visual    │   │
│  │ • Gestión content   │         │ • Debugging flujo   │   │
│  └─────────────────────┘         └─────────────────────┘   │
│         │                                   │                │
│         │                                   │                │
│         └───────────────┬───────────────────┘                │
│                         ▼                                    │
│                 ┌───────────────┐                           │
│                 │  POSTS (JSON) │                           │
│                 │  outputs/     │                           │
│                 └───────────────┘                           │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 ¿Qué es Daggr?

**Daggr** es una librería de Python creada por el equipo de Gradio para:

- ✅ **Visualizar workflows** de IA de forma automática
- ✅ **Inspeccionar outputs** de cada paso del flujo
- ✅ **Re-ejecutar nodos** individuales sin correr todo el pipeline
- ✅ **Modificar inputs** en tiempo real
- ✅ **Persistir estado** entre sesiones
- ✅ **Debugging visual** de pipelines complejos

🔗 **Más info**: https://huggingface.co/blog/daggr

## 🔄 Flujo de 6 Agentes

El workflow de generación de posts sigue este flujo:

```
1️⃣ Style Analyzer
    │
    ├─► Analiza biografía y posts de muestra
    │   Output: Características de estilo (JSON)
    │
    ▼
2️⃣ Keyword Extractor
    │
    ├─► Extrae keywords del tema + estilo
    │   Output: Lista de keywords relevantes
    │
    ▼
3️⃣ Content Generator
    │
    ├─► Genera contenido del post
    │   Output: Contenido en Markdown
    │
    ▼
4️⃣ Critic Agent ◄──┐
    │               │
    ├─► Revisa calidad del contenido
    │   Output: Análisis y sugerencias (JSON)
    │               │
    │               │ Loop de mejora
    │               │ (si score < 8.0)
    └───────────────┘
    │
    ▼
5️⃣ Image Selector
    │
    ├─► Selecciona imágenes relevantes
    │   Output: URLs de imágenes
    │
    ▼
6️⃣ HTML Builder
    │
    ├─► Construye HTML final del post
    │   Output: Post completo (HTML + metadata)
    │
    ▼
📁 outputs/post_{timestamp}.json
```

## 🎯 Uso del Workflow Daggr

### 1. Iniciar el servidor Daggr

```bash
cd backend
.\.venv\Scripts\python.exe daggr_blogger_workflow.py
```

Esto abrirá la interfaz visual en: **http://localhost:7860**

### 2. Configurar los inputs

En la interfaz Daggr verás el primer nodo **Style Analyzer** con 3 campos:

- **Nombre del Blogger**: Ej. "Tech Explorer"
- **Biografía del Blogger**: Descripción del estilo y expertise
- **Posts de Muestra**: Ejemplos de posts previos (uno por línea)

### 3. Ejecutar el workflow

- **Opción 1**: Ejecutar todo el flujo completo (botón "Run All")
- **Opción 2**: Ejecutar nodo por nodo (botón "Run" en cada nodo)

### 4. Inspeccionar resultados

Cada nodo muestra:
- ✅ **Inputs** usados
- ✅ **Outputs** generados
- ✅ **Estado** (pending/running/completed)
- ✅ **Tiempo** de ejecución

### 5. Re-ejecutar con cambios

Puedes:
- Modificar cualquier input
- Re-ejecutar solo un nodo específico
- Ver cómo se propagan los cambios al resto del flujo

## 🔧 Características Avanzadas

### Loop de Mejora (Critic Agent)

El **Critic Agent** evalúa el contenido y puede:
- Sugerir mejoras
- Solicitar regeneración si el score es bajo
- Validar cobertura de keywords

En daggr_blogger_workflow.py puedes configurar:
```python
# Umbral de calidad
MIN_SCORE = 8.0

# Máximo de iteraciones
MAX_ITERATIONS = 3
```

### Persistencia de Estado

Daggr automáticamente guarda:
- ✅ Valores de inputs
- ✅ Outputs generados
- ✅ Posición del canvas
- ✅ Estado de cada nodo

Puedes cerrar y reabrir la interfaz sin perder progreso.

### Hojas de Trabajo (Sheets)

Usa "sheets" para mantener múltiples workflows:
- Sheet 1: Pruebas con estilo formal
- Sheet 2: Pruebas con estilo casual
- Sheet 3: Pruebas con temas técnicos

## 📁 Estructura de Archivos

```
backend/
├── daggr_blogger_workflow.py    # ← Workflow visual con daggr
├── aphra_blogger/               # Agentes de IA
│   ├── workflows/
│   │   └── blogger_style.py     # Orquestador principal
│   └── config/
│       └── default.toml         # Configuración
├── outputs/                     # Posts generados
│   └── post_20260211_*.json
└── requirements.txt             # daggr>=0.7.0
```

## 🔗 Integración Frontend ↔ Backend

### Opción 1: API REST

El frontend Next.js puede llamar a un endpoint que ejecute el workflow:

```typescript
// frontend/app/api/generate-post/route.ts
const response = await fetch('http://localhost:7860/api/generate', {
  method: 'POST',
  body: JSON.stringify({ topic, blogger_name, blogger_bio })
});
```

### Opción 2: Archivos JSON

El backend genera archivos en `outputs/` que el frontend lee:

```typescript
// frontend/lib/posts.ts
const posts = fs.readdirSync('backend/outputs')
  .filter(file => file.startsWith('post_'))
  .map(file => JSON.parse(fs.readFileSync(file)));
```

## 🧪 Testing y Debugging

### Testing Manual con Daggr

Daggr es ideal para:
- ✅ Probar diferentes estilos de blogger
- ✅ Experimentar con temas variados
- ✅ Validar la calidad de cada agente
- ✅ Debugging visual del flujo completo

### Debugging de Nodos

Si un nodo falla:
1. Inspecciona el output del nodo anterior
2. Verifica los inputs del nodo actual
3. Modifica inputs y re-ejecuta solo ese nodo
4. Revisa logs en la consola de Python

### Métricas de Calidad

El workflow genera métricas en cada paso:
- **Style Analyzer**: Características detectadas
- **Keyword Extractor**: Nº de keywords
- **Content Generator**: Longitud del post
- **Critic Agent**: Score de calidad (0-10)
- **Image Selector**: Nº de imágenes
- **HTML Builder**: Tamaño final del HTML

## 🎓 Recursos

- **Daggr Docs**: https://github.com/gradio-app/daggr
- **Blog Post**: https://huggingface.co/blog/daggr
- **Ejemplos**: https://huggingface.co/collections/ysharma/daggr-hf-spaces

## 🚧 Próximos Pasos

### Integración Completa
- [ ] Conectar workflow daggr con orchestrator real
- [ ] Implementar API REST para el frontend
- [ ] Sistema de colas para generaciones múltiples

### Mejoras de Workflow
- [ ] Añadir nodo de SEO optimization
- [ ] Nodo de fact-checking
- [ ] Nodo de traducción multi-idioma

### Producción
- [ ] Deploy en Hugging Face Spaces
- [ ] Sistema de autenticación
- [ ] Rate limiting y caching
